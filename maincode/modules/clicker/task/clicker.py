# -*- coding: utf-8 -*-
import time
from PyQt5.QtCore import QThread, pyqtSignal
from tools.environment import *
import keyboard
from win32api import mouse_event, keybd_event

# 鼠标按键映射
CLICK_MAP = {
    "LCLICK": (2, 4),  # 左键：按下/释放
    "RCLICK": (8, 16),  # 右键：按下/释放
    "MCLICK": (32, 64)  # 中键：按下/释放
}

# 键盘按键映射
KEY_MAP = {
    "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57,
    'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 117, 'F7': 118, 'F8': 119,
    'F9': 120, 'F10': 121, 'F11': 122, 'F12': 123,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90,
    'BACKSPACE': 8, 'TAB': 9, 'ENTER': 13, 'SHIFT': 16, 'CTRL': 17, 'ALT': 18,
    'PAUSE': 19, 'CAPSLOCK': 20, 'ESC': 27, 'SPACE': 32,
    'PAGEUP': 33, 'PAGEDOWN': 34, 'END': 35, 'HOME': 36,
    'LEFT': 37, 'UP': 38, 'RIGHT': 39, 'DOWN': 40, 'PRINTSCREEN': 42,
    'INSERT': 45, 'DELETE': 46, 'WIN': 91, 'NUMLOCK': 144,
    '[': 219, ']': 221, '+': 107, '-': 109, '~': 192, '`': 192, "/": 191
}

# 鼠标按键列表
CLICKER_MOUSE_LIST = ["LCLICK", "RCLICK", "MCLICK"]


class Clicker(QThread):
    """点击器线程类，处理不同模式的点击操作"""
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.interval = 0.01  # 默认间隔时间
        self.mode_clicker = ""
        self.clicker_list = []
        self.running = False  # 运行状态标记

    def run(self):
        """线程主方法，根据不同模式执行点击操作"""
        self.running = True
        try:
            self.mode_clicker = self.task["ClickerMode"]
            self.clicker_list = [key.strip().upper() for key in self.task["clickerkey"].split("+") if key.strip()]

            if self.mode_clicker == "连点模式":
                self._handle_click_mode()
            elif self.mode_clicker == "按下模式":
                self._handle_hold_mode()
            elif self.mode_clicker == "脚本模式":
                self._handle_script_mode()
        finally:
            self.running = False

    def _handle_click_mode(self):
        """处理连点模式"""
        try:
            self.interval = float(self.task["interval"]) / 1000  # 转换为秒
            if self.interval <= 0:
                self.interval = 0.01  # 最小间隔保护
        except (ValueError, TypeError):
            self.interval = 0.01  # 异常处理默认值

        # 检查是否包含鼠标按键
        has_mouse = any(key in CLICKER_MOUSE_LIST for key in self.clicker_list)

        if has_mouse and len(self.clicker_list) == 1:
            # 鼠标连点处理
            down_event, up_event = CLICK_MAP[self.clicker_list[0]]
            while self.running:
                mouse_event(down_event, 0, 0)
                time.sleep(0.01)  # 按键按下时间
                mouse_event(up_event, 0, 0)
                time.sleep(self.interval)
        else:
            # 键盘连点处理
            key_codes = [KEY_MAP[key] for key in self.clicker_list if key in KEY_MAP]
            if not key_codes:
                return

            while self.running:
                # 按下所有键
                for code in key_codes:
                    keybd_event(code, 0, 0, 0)
                time.sleep(0.01)  # 按键按下时间

                # 释放所有键（反向释放避免冲突）
                for code in reversed(key_codes):
                    keybd_event(code, 0, 2, 0)
                time.sleep(self.interval)

    def _handle_hold_mode(self):
        """处理按下模式（持续按住）"""
        # 记录已按下的键用于释放
        pressed_keys = []
        pressed_mouse = []

        try:
            # 按下所有指定键
            for key in self.clicker_list:
                if key in CLICKER_MOUSE_LIST:
                    down_event = CLICK_MAP[key][0]
                    mouse_event(down_event, 0, 0)
                    pressed_mouse.append(key)
                elif key in KEY_MAP:
                    keybd_event(KEY_MAP[key], 0, 0, 0)
                    pressed_keys.append(key)

            # 保持按下状态直到线程停止
            while self.running:
                time.sleep(0.1)
        finally:
            # 确保释放所有按键
            for key in pressed_mouse:
                mouse_event(CLICK_MAP[key][1], 0, 0)
            for key in pressed_keys:
                keybd_event(KEY_MAP[key], 0, 2, 0)

    def _handle_script_mode(self):
        """处理脚本模式"""
        run_count = self.task.get("runnum", 0)
        script = self.task.get("script", [])

        if not script:
            return

        # 循环执行脚本
        if run_count < 1:  # 无限循环
            while self.running:
                self._execute_script(script)
        else:  # 有限次数循环
            for _ in range(run_count):
                if not self.running:
                    break
                self._execute_script(script)

    def _execute_script(self, script):
        """执行单轮脚本"""
        for func, value in script:
            if not self.running:
                break

            try:
                if func == "clickdown" and value.upper() in CLICKER_MOUSE_LIST:
                    mouse_event(CLICK_MAP[value.upper()][0], 0, 0)
                elif func == "clickup" and value.upper() in CLICKER_MOUSE_LIST:
                    mouse_event(CLICK_MAP[value.upper()][1], 0, 0)
                elif func == "keydown" and value.upper() in KEY_MAP:
                    keybd_event(KEY_MAP[value.upper()], 0, 0, 0)
                elif func == "keyup" and value.upper() in KEY_MAP:
                    keybd_event(KEY_MAP[value.upper()], 0, 2, 0)
                elif func == "moveto" and isinstance(value, tuple) and len(value) == 2:
                    # 假设moveto实现（需要补充）
                    pass
                elif func == "wait" and isinstance(value, int):
                    time.sleep(value / 1000)  # 转换为秒
            except Exception as e:
                self.send(f"脚本执行错误: {str(e)}", 0, False, False)
                break

    def stop(self):
        """停止点击器线程"""
        self.running = False
        self.wait()  # 等待线程结束