from psutil import process_iter
from win10toast import ToastNotifier
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER, windll
from comtypes import CLSCTX_ALL
from typing import Union
from win32api import MessageBox
import sys
from traceback import format_exc
from win32con import MB_OK
from maincode.tools.logger import Logger
from pyuac import isUserAdmin
from subprocess import run as sprun
import pygetwindow as gw
from time import sleep
from win32gui import ClientToScreen, GetClientRect


def CmdRun(_str: str):
    sprun(_str, shell=True)


# 从exe名称获取pid
def GetPid(name: str) -> int:
    for proc in process_iter():
        # noinspection PyBroadException
        try:
            if proc.name() == name:
                return proc.pid
        except Exception:
            continue
    return 0


# 关闭进程
def killprocess(_process: Union[int, str]):
    if isinstance(_process, int):
        # 根据pid杀死进程
        CmdRun('taskill /f /pid %s' % _process)
    elif isinstance(_process, str):
        # 根据进程名杀死进程
        pro = 'taskill /f /im %s' % _process
        CmdRun(pro)
    else:
        raise ValueError(f"close异常传输值：{_process}")


# windows提示
def WindowsNotify(title: str, massage: str):
    try:
        toaster = ToastNotifier()
        toaster.show_toast(title,
                           massage,
                           icon_path="resources/main/SGA/title.ico",
                           duration=5,
                           threaded=True)
    except:
        ...

# 查询静音状态
def GetMute() -> bool:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume.GetMute()


# 熄屏
def ScreenOff() -> None:
    power_off = 2
    windll.user32.PostMessageW(0xffff, 0x0112, 0xF170, power_off)
    shell32 = windll.LoadLibrary("shell32.dll")
    shell32.ShellExecuteW(None, 'open', 'rundll32.exe', 'USER32', '', 5)


def GetTracebackInfo(e) -> str:
    return str(e) + "\n" + format_exc()


def GetTracebackValue() -> (str, str):
    _, _, exc_traceback = sys.exc_info()
    frame = exc_traceback.tb_frame
    return frame.f_locals, frame.f_globals


def SendMessageBox(_str) -> None:
    MessageBox(0, _str, "砂糖代理", MB_OK)

    
def CheckAdmin():
    if not isUserAdmin():
        _str = "请手动使用管理员权限启动\n"\
               "可参考视频给予默认管理员权限启动：\n"\
               "https://www.bilibili.com/video/BV18kKAeYE2t"
        SendMessageBox(_str)
        return False
    return True


def foreground(self, num=20):
    for _ in range(num):
        if self.isActive:
            return
        else:
            try:
                if self.isMinimized:
                    self.restore()
                self.activate()
            except:
                ...
        sleep(0.5)
    raise TimeoutError


def GetHwnd(self):
    return self._hWnd


def GetWindow(para, accurate=False):  # 标题, 句柄
    if isinstance(para, str):
        windows = gw.getWindowsWithTitle(para)
        if not windows:
            return None
        else:
            if accurate:
                for win in windows:
                    if para == win.title:
                        window = win
                        break
                else:
                    return None
            else:
                window = windows[0]
    elif isinstance(para, int):
        windows = gw.getWindowsWithTitle("")

        for win in windows:
            if para == win._hWnd:
                window = win
                break
        else:
            return None
    else:
        return None
    hwnd = window._hWnd
    gw.Win32Window.foreground = foreground
    gw.Win32Window.GetHwnd = GetHwnd
    x1, y1 = ClientToScreen(hwnd, (0, 0))
    _, _, w, h = GetClientRect(hwnd)
    window.rect = x1, y1, w + x1, h + y1
    return window


def VersionsCompare(version1: str, version2: str) -> int:
    def split_version(v: str):
        components = []
        for item in v.split('.'):
            try:
                components.append(int(item))
            except ValueError:
                components.append(item)
        return components
    v1_parts = split_version(version1)
    v2_parts = split_version(version2)
    for v1, v2 in zip(v1_parts, v2_parts):
        if v1 != v2:
            return -1 if v1 < v2 else 1
    if len(v1_parts) != len(v2_parts):
        return -1 if len(v1_parts) < len(v2_parts) else 1
    return -1 if version1 < version2 else (1 if version1 > version2 else 0)


logger = Logger().getlogger()


def sgatry(func):
    def wrapper(*args, **kwargs):
        """包装函数的文档字符串"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            _str = GetTracebackInfo(e)
            logger.error(_str)
    return wrapper


if __name__ == '__main__':
    pass
