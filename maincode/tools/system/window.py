from time import sleep
import pygetwindow as gw
from maincode.tools.core.logger import logger
import win32gui
from typing import Optional


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
    x1, y1 = win32gui.ClientToScreen(hwnd, (0, 0))
    _, _, w, h = win32gui.GetClientRect(hwnd)
    window.rect = x1, y1, w + x1, h + y1
    return window


def find_window_by_title(window_title: str, exact_match: bool = True) -> Optional[int]:
    """
    根据窗口标题查找窗口句柄

    参数:
        window_title: 窗口标题
        exact_match: 是否精确匹配

    返回:
        窗口句柄 (HWND)，如果未找到返回 None
    """

    def enum_windows_callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if exact_match:
                if title == window_title:
                    windows.append(hwnd)
            else:
                if window_title in title:
                    windows.append(hwnd)
        return True

    windows = []
    win32gui.EnumWindows(enum_windows_callback, windows)

    return windows[0] if windows else None
