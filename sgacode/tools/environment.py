from time import localtime
from cpufeature import CPUFeature
from traceback import format_exc
from win32con import SW_RESTORE
from win32gui import (IsIconic, ShowWindow,
                      SetForegroundWindow, GetForegroundWindow)
from time import sleep
from os import getcwd


class Environment:
    version: str = "3.X"

    def __init__(self, _logger):
        self.logger = _logger
        self.hwnd: int = 0  # SGA窗口句柄
        self.monitors: list = []  # 电脑显示器信息
        self.platform: str = ""  # 系统平台信息
        self.taskrunning = None
        self.start_time = localtime()  # 记录SGA本次启动时间
        self.workdir = getcwd()  # 记录并检查SGA本次工作目录
        self.cpu_feature = CPUFeature["AVX2"]
        self.getmonitors()
        self.getplatform()
        self.value: dict = {}
        self.mainconfig: dict = {}

    def getmonitors(self) -> None:
        from screeninfo import get_monitors
        for i, monitor in enumerate(get_monitors(), start=1):
            self.monitors += [[i, (monitor.width, monitor.height), (monitor.x, monitor.y)]]

    def getplatform(self) -> None:
        import platform
        system = platform.system()
        release = platform.release()
        version = platform.version()
        if system == "Windows":
            if release == "10":
                build_number = int(version.split('.')[2])  # 获取构建版本号
                self.platform = "Windows 11" if build_number >= 22000 else "Windows 10"
            elif release == "7":
                self.platform = "Windows 7"
            else:
                self.platform = f"Windows-未知版本:{release}-Version: {version}）"
        else:
            self.platform = system

    def foreground(self) -> bool:
        if not self.hwnd:
            self.logger.debug("Environment.hwnd 未初始化")
            return False
        for i in range(10):
            current_hwnd = GetForegroundWindow()
            if current_hwnd == self.hwnd:
                self.logger.info("SGA窗口唤起成功")
                return True
            if IsIconic(self.hwnd):
                ShowWindow(self.hwnd, SW_RESTORE)
                sleep(0.2)
            if current_hwnd != self.hwnd:
                try:
                    SetForegroundWindow(self.hwnd)
                except Exception as e:
                    self.logger.debug(str(e) + format_exc() + "\nSGA窗口唤起异常：SetForegroundWindow")
                sleep(0.2)
        self.logger.info("SGA窗口唤起失败")
        return False

    def logger_environment_info(self):
        _str = (f"\n运行环境:\n"
                f"  工作目录:{self.workdir}\n"
                f"  CPUFeature:{self.cpu_feature}\n"
                f"  系统:{self.platform}\n"
                f"显示器:")
        for i, (w, h), (x, y) in self.monitors:
            _str += f"\n  编号:{i} 分辨率:{w}×{h} 位置:{x},{y}"
        self.logger.info(_str)


if __name__ == '__main__':
    pass
