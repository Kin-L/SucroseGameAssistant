from psutil import process_iter
from win10toast import ToastNotifier
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER, windll
from comtypes import CLSCTX_ALL
from typing import Union
from win32api import MessageBox
import sys
from traceback import format_exc
from win32con import MB_OK, SW_RESTORE
from sgacode.tools.logger import Logger
from win32gui import (FindWindow, EnumWindows, GetClassName,
                      GetWindowText, IsIconic, ShowWindow,
                      SetForegroundWindow, GetForegroundWindow)
from pyuac import isUserAdmin
from time import sleep
from subprocess import run as sprun


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
def WindowsNotify(title: str, massage: str) -> None:
    toaster = ToastNotifier()
    toaster.show_toast(title,
                       massage,
                       icon_path="assets/main_window/ui/ico/SGA.ico",
                       duration=5,
                       threaded=True)


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


def GetHwnd(_mode: bool, _class: Union[str, None], _title: Union[str, None]) -> int:
    """
    :param _mode: 获取方法 True 精确查找 False 扫描
    :param _class: 类 str
    :param _title: 标题 str
    :return: 句柄 int 未找到时返回 0
    """
    if _mode:
        return FindWindow(_class, _title)
    else:
        if _class is None:
            _class = ""
        if _title is None:
            _title = ""
        hwnd_list = []
        EnumWindows(lambda _hwnd, _hwnd_list: _hwnd_list.append(_hwnd), hwnd_list)
        for hwnd in hwnd_list:
            # noinspection PyBroadException
            try:
                cls = GetClassName(hwnd)
                tit = GetWindowText(hwnd)
                if _class in cls and _title in tit:
                    return hwnd
            except Exception:
                continue
        return 0
    
    
def CheckAdmin():
    if not isUserAdmin():
        _str = "请手动使用管理员权限启动\n"\
               "可参考视频给予默认管理员权限启动：\n"\
               "https://www.bilibili.com/video/BV18kKAeYE2t"
        SendMessageBox(_str)
        input("222")
        exit(1)


def foreground(_hwnd: int) -> bool:
    if not _hwnd:
        return False
    for i in range(10):
        current_hwnd = GetForegroundWindow()
        if current_hwnd == _hwnd:
            return True
        if IsIconic(_hwnd):
            ShowWindow(_hwnd, SW_RESTORE)
            sleep(0.2)
        if current_hwnd != _hwnd:
            # noinspection PyBroadException
            try:
                SetForegroundWindow(_hwnd)
            except Exception:
                pass
            sleep(0.2)
    return False


def DictListType(_dict):
    return {key: type(key) for key, value in _dict.items()}


logger = Logger().getlogger()
if __name__ == '__main__':
    pass
