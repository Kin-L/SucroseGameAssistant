from time import sleep
import pygetwindow as gw
from win32gui import ClientToScreen, GetClientRect
from maincode.tools.core.logger import logger


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
