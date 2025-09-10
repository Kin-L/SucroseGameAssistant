from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER, windll
from comtypes import CLSCTX_ALL
from maincode.tools.core.logger import logger
from subprocess import run as sprun
from maincode.tools.system.notification import GetTracebackInfo


def CmdRun(_str: str):
    logger.info(f"执行命令: {_str}")
    sprun(_str, shell=True)


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


if __name__ == '__main__':
    pass
