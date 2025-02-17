from main.tools.prepare import Prepare
from os import getcwd
from time import localtime
from ctypes import windll
from cpufeature import CPUFeature


class Environment(Prepare):
    def __init__(self, _logger):
        super().__init__(_logger)
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


if __name__ == '__main__':
    path = getcwd()