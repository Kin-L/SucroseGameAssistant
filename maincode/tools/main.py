import psutil
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
    logger.info(f"执行命令: {_str}")
    sprun(_str, shell=True)


# 从exe名称获取pid
def GetPid(name: str) -> int:
    for proc in psutil.process_iter():
        try:
            if proc.name() == name:
                return proc.pid
        except Exception as e:
            logger.warning(f"获取进程PID时异常: {e}")
            continue
    return 0


# 关闭进程
def killprocess(_process: Union[int, str]):
    if isinstance(_process, int):
        _pid = _process
    elif isinstance(_process, str):
        _pid = GetPid(_process)
    else:
        raise ValueError(f"close异常传输值：{_process}")
    try:
        process = psutil.Process(_pid)
        process.terminate()
        gone, still_alive = psutil.wait_procs([process], timeout=5)
        if still_alive:
            process.kill()
            logger.warning(f"强制杀死进程 PID: {_pid}")
        else:
            logger.info(f"成功终止进程 PID: {_pid}")
        return 0
    except psutil.NoSuchProcess:
        logger.error(f"进程不存在 PID: {_pid}")
        return 1
    except psutil.AccessDenied:
        logger.error(f"无权限终止进程 PID: {_pid}")
        return 2


# windows提示
def WindowsNotify(title: str, massage: str):
    try:
        toaster = ToastNotifier()
        toaster.show_toast(title,
                           massage,
                           icon_path="resources/main/SGA/title.ico",
                           duration=5,
                           threaded=True)
    except Exception as e:
        logger.error(f"通知失败: {e}")


# 查询静音状态
def GetMute() -> bool:
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        return bool(volume.GetMute())
    except Exception as e:
        logger.error(f"查询静音状态(GetMute)异常: {GetTracebackInfo(e)}")
        return False


# 熄屏
def ScreenOff() -> None:
    try:
        power_off = 2
        windll.user32.PostMessageW(0xffff, 0x0112, 0xF170, power_off)
        shell32 = windll.LoadLibrary("shell32.dll")
        shell32.ShellExecuteW(None, 'open', 'rundll32.exe', 'USER32', '', 5)
    except Exception as e:
        logger.error(f"熄屏(ScreenOff)异常: {GetTracebackInfo(e)}")


def GetTracebackInfo(e) -> str:
    return str(e) + "\n" + format_exc()


def GetTracebackValue() -> (str, str):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if exc_traceback is None:
        return {}, {}
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


def foreground(self, num=20, timeout=0.2):
    for _ in range(num):
        if getattr(self, 'isActive', False):
            return True
        else:
            if _:
                sleep(timeout)
            try:
                if getattr(self, 'isMinimized', False):
                    self.restore()
                self.activate()
            except Exception as e:
                logger.warning(f"窗口激活失败: {e}")
            sleep(timeout)
    logger.error("foreground 超时")
    return False


def GetHwnd(self):
    return self._hWnd


def GetWindow(para, accurate=False):  # 标题, 句柄
    if isinstance(para, str):
        windows = gw.getWindowsWithTitle(para)
        if not windows:
            return None
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
        try:
            window = gw.Win32Window(para)
        except Exception:
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
    from packaging.version import parse
    v1 = parse(version1)
    v2 = parse(version2)
    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0


logger = Logger().getlogger()


if __name__ == '__main__':
    pass
