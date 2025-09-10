import sys
from traceback import format_exc

from pyuac import isUserAdmin
from win10toast import ToastNotifier
from win32api import MessageBox
from win32con import MB_OK

from maincode.tools.core.constant import spr
from maincode.tools.core.logger import logger


# windows提示
def WindowsNotify(title: str, massage: str):
    try:
        toaster = ToastNotifier()
        toaster.show_toast(title,
                           massage,
                           icon_path=spr.SGAICO,
                           duration=5,
                           threaded=True)
    except Exception as e:
        logger.error(f"通知失败: {e}")


def SendMessageBox(_str) -> None:
    MessageBox(0, _str, "砂糖代理", MB_OK)


def GetTracebackInfo(e) -> str:
    return str(e) + "\n" + format_exc()


def GetTracebackValue() -> (str, str):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if exc_traceback is None:
        return {}, {}
    frame = exc_traceback.tb_frame
    return frame.f_locals, frame.f_globals


def CheckAdmin():
    if not isUserAdmin():
        _str = "请手动使用管理员权限启动\n"\
               "可参考视频给予默认管理员权限启动：\n"\
               "https://www.bilibili.com/video/BV18kKAeYE2t"
        SendMessageBox(_str)
        return False
    return True
