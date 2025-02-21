from os import getcwd
from time import localtime
from ctypes import windll
from cpufeature import CPUFeature
from win32api import MessageBox
from win32con import MB_OK, SW_RESTORE
from win32gui import (FindWindow, EnumWindows, GetClassName,
                      GetWindowText, IsIconic, ShowWindow,
                      SetForegroundWindow, GetForegroundWindow)
from time import sleep
from main.tools.logger import logger


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
        # 获取电脑缩放和分辨率
        self.resolution_origin = None
        self.resolution_now = None
        self.zoom_desktop = None
        self.get_resolution_zoom()
        self.state = {}

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

    def get_resolution_zoom(self):
        user32 = windll.user32
        now_wid = user32.GetSystemMetrics(0)
        now_hig = user32.GetSystemMetrics(1)
        user32.SetProcessDPIAware()
        ori_wid = user32.GetSystemMetrics(0)
        ori_hig = user32.GetSystemMetrics(1)
        self.resolution_origin = (ori_wid, ori_hig)
        self.resolution_now = (now_wid, now_hig)
        self.zoom_desktop = round(ori_wid / now_wid, 2)


class SGAEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.version = ""
        self.current_work_path = ""
        self.main_config = {}
        self.timer = {}
        self.update = False
        self.lock = True
        self.config = ""
        self.current = {}
        self.launch = {}
        self.wait_time = 1
        self.current_mute = None
        self.now_config = {}
        self.setting = 1
        self.config_name = []
        self.config_type = []
        self.name = []
        self.prefix = []
        self.load = []


env = SGAEnvironment()

if __name__ == '__main__':
    path = getcwd()
