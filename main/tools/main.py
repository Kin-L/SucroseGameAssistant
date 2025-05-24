from subprocess import run as cmd_run
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


# 从exe名称获取pid
def getpid(name: str) -> int:
    for proc in process_iter():
        # noinspection PyBroadException
        try:
            if proc.name() == name:
                return proc.pid
        except Exception:
            continue
    return 0


# 关闭进程
def killprocess(_process: Union[int, str]) -> None:
    if isinstance(_process, int):
        # 根据pid杀死进程
        cmd_run('taskill /f /pid %s' % _process)
    elif isinstance(_process, str):
        # 根据进程名杀死进程
        pro = 'taskill /f /im %s' % _process
        cmd_run(pro)
    else:
        raise ValueError(f"close异常传输值：{_process}")


# windows提示
def notify(title: str, massage: str) -> None:
    toaster = ToastNotifier()
    toaster.show_toast(title,
                       massage,
                       icon_path="assets/main_window/ui/ico/SGA.ico",
                       duration=5,
                       threaded=True)


# 查询静音状态
def get_mute() -> bool:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    return volume.GetMute()


# 熄屏
def screen_off() -> None:
    power_off = 2
    windll.user32.PostMessageW(0xffff, 0x0112, 0xF170, power_off)
    shell32 = windll.LoadLibrary("shell32.dll")
    shell32.ShellExecuteW(None, 'open', 'rundll32.exe', 'USER32', '', 5)


def gettracebackinfo(e) -> str:
    return str(e) + format_exc()


def gettracebackvalue() -> (str, str):
    _, _, exc_traceback = sys.exc_info()
    frame = exc_traceback.tb_frame
    return frame.f_locals, frame.f_globals


def sendmessagebox(_str) -> None:
    MessageBox(0, _str, "砂糖代理", MB_OK)

logger = Logger().getlogger()