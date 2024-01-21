# -*- coding:gbk -*-
from pyautogui import press as papress
from sys import exit
from pyuac import isUserAdmin, runAsAdmin
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import windll
from win10toast import ToastNotifier
from subprocess import run
from win32api import MessageBox
from win32con import MB_OK
from win32gui import SetForegroundWindow, SetWindowPos
# pyuic5 -o SGA_demo.py SGA_demo.ui
import win32com


# windows提示
def notify(title, massage):
    toaster = ToastNotifier()
    toaster.show_toast(title, massage,
                       icon_path="assets/main_window/ui/ico/SGA.ico",
                       duration=5,
                       threaded=True)


def message_box(text):
    MessageBox(0, text, "砂糖代理", MB_OK)


# 查询静音状态
def get_mute():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume.GetMute()


# 切换静音状态
def change_mute():
    papress('volumemute')


# 熄屏
def screen_off():
    power_off = 2
    windll.user32.PostMessageW(0xffff, 0x0112, 0xF170, power_off)
    shell32 = windll.LoadLibrary("shell32.dll")
    shell32.ShellExecuteW(None, 'open', 'rundll32.exe', 'USER32', '', 5)


# cmd运行
def cmd_run(cmd_str):
    run(cmd_str, shell=True)


# 获取电脑缩放和分辨率
def get_resolution_zoom():
    from ctypes import windll
    user32 = windll.user32
    now_wid = user32.GetSystemMetrics(0)
    now_hig = user32.GetSystemMetrics(1)
    user32.SetProcessDPIAware()
    ori_wid = user32.GetSystemMetrics(0)
    ori_hig = user32.GetSystemMetrics(1)
    return (ori_wid, ori_hig), (now_wid, now_hig), round(ori_wid / now_wid, 2)

def check_path(str):
    return str.replace("\\", "/").replace("//", "/").strip("\"")

def foreground(hwnd):
    try:
        SetForegroundWindow(hwnd)
        return True
    except:
        try:
            SetWindowPos(hwnd)
            return True
        except:
            return False
        
class System:
    def __init__(self):
        # 启用日志
        from tools.logger.log import Logger
        self.logger = Logger().get_logger()
        # 参数初设
        self.OCR = None
        self.workdir = None
        self.resolution_compile = None
        self.frame, self.zoom = None, None
        self.soft = type[classmethod]
        # 获取缩放前后分辨率，缩放比例
        self.resolution_origin = None
        self.resolution_now = None
        self.zoom_desktop = None

    def set_soft(self, path=None, mode_cls_tit=list[0, None, None]):
        from .software import Software
        self.soft = Software(self.resolution_compile)
        _pb = path is None
        _pc = mode_cls_tit[1:] == (None, None)
        if _pb and _pc:
            print("set_soft 无效设置。")
        else:
            if not _pb:
                self.soft.set_path(path)
            self.soft.set_hwnd_find(mode_cls_tit[0], mode_cls_tit[1], mode_cls_tit[2])

    # 基准分辨率
    def set_compile(self, wide, high):
        self.resolution_compile = (wide, high)

    def get_workdir(self):
        from os import getcwd
        self.workdir = getcwd()

    # 获取管理员权限
    def get_user_admin(self):
        if isUserAdmin():
            self.logger.debug("管理员权限启动")
        else:
            self.logger.debug("非管理员权限启动,尝试获取管理员权限")
            runAsAdmin(wait=False)
            if isUserAdmin():
                self.logger.debug("成功获取管理员权限")
            else:
                self.logger.debug("获取管理员权限失败")
                self.logger.debug("退出")
                exit(1)

    # 坐标轴缩放
    def axis_zoom(self, x, y):
        if self.zoom != 1:
            x, y = int(x * self.zoom), int(y * self.zoom)
        return x, y

    # 坐标轴移动
    def axis_translation(self, x, y):
        if self.frame != (0, 0):
            x, y = x + self.frame[0], y + self.frame[1]
        return x, y

    # 坐标轴缩放并移动
    def axis_change(self, x, y):
        if self.zoom != 1:
            x, y = int(x * self.zoom), int(y * self.zoom)
        if self.frame != (0, 0):
            x, y = x + self.frame[0], y + self.frame[1]
        return x, y


if __name__ == '__main__':
    pass
    # frame, zoom, Ocr, logger = None, None, None, None
    # env = Environment(1920, 1080)
    # env.soft.set_hwnd_find(True, ("UnityWndClass", "原神"))
