from time import localtime
from cpufeature import CPUFeature
from win32api import MessageBox
from win32con import MB_OK, SW_RESTORE
from win32gui import (FindWindow, EnumWindows, GetClassName,
                      GetWindowText, IsIconic, ShowWindow,
                      SetForegroundWindow, GetForegroundWindow)
from time import sleep
from main.tools.logger import logger
from os import getcwd


class Environment:
    def __init__(self):
        self.logger = logger
        self.hwnd = 0
        # 记录SGA本次启动时间
        self.start_time = localtime()
        # 记录并检查SGA本次工作目录
        self.workdir = getcwd()
        if " " in self.workdir:
            self.send_messagebox("SGA安装目录请勿带空格")
        self.cpu_feature = CPUFeature["AVX2"]
        # 获取电脑显示器信息
        self.monitors = []
        self.getmonitors()
        self.platform = self.get_platform()

    @staticmethod
    def send_messagebox(_str):
        MessageBox(0, _str, "砂糖代理", MB_OK)

    def find_hwnd(self, mode_cls_tit):
        mode, cls, tit = mode_cls_tit
        if mode:
            self.hwnd = FindWindow(cls, tit)
            return self.hwnd
        else:
            hwnd_list = []
            EnumWindows(lambda _hwnd, _hwnd_list: _hwnd_list.append(_hwnd), hwnd_list)
            for hwnd in hwnd_list:
                # noinspection PyBroadException
                try:
                    class_name = GetClassName(hwnd)
                    title = GetWindowText(hwnd)
                    if cls in class_name and tit in title:
                        self.hwnd = hwnd
                        return hwnd
                except Exception:
                    continue
            self.logger.info(f"未找到窗口句柄：{mode, cls, tit}")
            return 0

    def foreground(self):
        for i in range(10):
            current_hwnd = GetForegroundWindow()
            if current_hwnd == self.hwnd:
                self.logger.debug(f"SGA窗口唤起成功")
                return True
            if IsIconic(self.hwnd):
                ShowWindow(self.hwnd, SW_RESTORE)
                sleep(0.2)
            if current_hwnd != self.hwnd:
                # noinspection PyBroadException
                try:
                    SetForegroundWindow(self.hwnd)
                except Exception:
                    self.logger.debug(f"SGA窗口唤起异常：SetForegroundWindow")
                sleep(0.2)
        self.logger.debug(f"SGA窗口唤起失败")
        return False

    def getmonitors(self):
        from screeninfo import get_monitors
        for i, monitor in enumerate(get_monitors(), start=1):
            self.monitors += [[i, (monitor.width, monitor.height),
                              (monitor.x, monitor.y)]]

    @staticmethod
    def get_platform():
        import platform
        system = platform.system()
        release = platform.release()
        version = platform.version()
        if system == "Windows":
            if release == "10":
                build_number = int(version.split('.')[2])  # 获取构建版本号
                if build_number >= 22000:
                    return "Windows 11"
                else:
                    return "Windows 10"
            elif release == "7":
                return "Windows 7"
            else:
                return f"Windows-未知版本:{release}-Version: {version}）"
        else:
            return system
