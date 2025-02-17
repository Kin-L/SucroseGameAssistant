from win32gui import (FindWindow, EnumWindows, GetClassName,
                      GetWindowText, IsIconic, ShowWindow,
                      SetForegroundWindow, GetForegroundWindow)
from win32con import SW_RESTORE
from pyuac import isUserAdmin
from time import sleep
from win32api import MessageBox
from win32con import MB_OK
from main.tools.logger import logger


class Prepare:
    def __init__(self):
        self.logger = logger
        self.hwnd = 0

    # 获取管理员权限
    def check_user_admin(self):
        if isUserAdmin():
            self.logger.info("管理员权限启动")
        else:
            self.logger.info("非管理员权限启动，退出")
            self.send_messagebox("请手动使用管理员权限启动\n"
                                 "可参考视频给予默认管理员权限启动：\n"
                                 "https://www.bilibili.com/video/BV18kKAeYE2t")
            exit(1)

    @staticmethod
    def send_messagebox(_str):
        MessageBox(0, _str, "砂糖代理", MB_OK)

    def find_hwnd(self, mode_cls_tit):
        mode, cls, tit = mode_cls_tit
        if mode:
            self.hwnd = FindWindow(cls, tit)
            return self.hwnd
        else:
            hwnd_list = []
            EnumWindows(lambda _hwnd, _hwnd_list: _hwnd_list.append(_hwnd), hwnd_list)
            for hwnd in hwnd_list:
                # noinspection PyBroadException
                try:
                    class_name = GetClassName(hwnd)
                    title = GetWindowText(hwnd)
                    if cls in class_name and tit in title:
                        self.hwnd = hwnd
                        return hwnd
                except Exception:
                    continue
            self.logger.info(f"未找到窗口句柄：{mode, cls, tit}")
            return 0

    def foreground(self):
        for i in range(10):
            current_hwnd = GetForegroundWindow()
            if current_hwnd == self.hwnd:
                self.logger.debug(f"SGA窗口唤起成功")
                return True
            if IsIconic(self.hwnd):
                ShowWindow(self.hwnd, SW_RESTORE)
                sleep(0.2)
            if current_hwnd != self.hwnd:
                # noinspection PyBroadException
                try:
                    SetForegroundWindow(self.hwnd)
                except Exception:
                    self.logger.debug(f"SGA窗口唤起异常：SetForegroundWindow")
                sleep(0.2)
        self.logger.debug(f"SGA窗口唤起失败")
        return False
            