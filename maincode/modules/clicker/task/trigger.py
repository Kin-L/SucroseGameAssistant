# -*- coding: utf-8 -*-
import keyboard
from .clicker import Clicker, CLICKER_MOUSE_LIST
import pynput
from PyQt5.QtCore import QThread, pyqtSignal

# 触发键映射表
TRIGGER_MAP = {
    "LCLICK": 'LEFT', "RCLICK": 'RIGHT', "MCLICK": 'MIDDLE',
    'X1CLICK': 'X1', 'X2CLICK': 'X2',
    "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57,
    'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 117, 'F7': 118, 'F8': 119,
    'F9': 120, 'F10': 121, 'F11': 122, 'F12': 123,
    "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
    "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
    "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90,
    "BACKSPACE": "BACKSPACE", "TAB": "TAB",
    "LEFT ALT": "ALT_L", "LEFT SHIFT": "SHIFT", "LEFT CTRL": "CTRL_L",
    "RIGHT ALT": "ALT_GR", "RIGHT SHIFT": "SHIFT_R", "RIGHT CTRL": "CTRL_R",
    "PAUSE": "MEDIA_PLAY_PAUSE", "CAPSLOCK": "CAPS_LOCK", "ESC": "ESC",
    "SPACE": "SPACE", "PAGEUP": "PAGEUP", "PAGEDOWN": "PAGEDOWN",
    "LEFT": "LEFT", "UP": "UP", "RIGHT": "RIGHT", "DOWN": "DOWN",
    "PRINTSCREEN": "PRINT_SCREEN",
    "INSERT": "INSERT", "DELETE": "DELETE", "WIN": "CMD",
    "NUMLOCK": "NUM_LOCK",
    '[': 219, ']': 221, '+': 107, '-': 109, '~': 192, '`': 192, "/": 111
}

# 鼠标触发键列表
TRIGGER_MOUSE_LIST = ["LCLICK", "RCLICK", "MCLICK", 'X1CLICK', 'X2CLICK']


class Trigger(QThread):
    """触发器线程类，处理触发键监听和点击器控制"""
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.mode_trigger = task.get("TriggerMode", "长按模式")
        self.trigger_click = None  # 鼠标触发键
        self.trigger_modify = None  # 修饰键
        self.mouse_listener = None  # 鼠标监听器
        self.keyboard_listener = None  # 键盘监听器
        self.clicker = Clicker(task)  # 点击器实例
        self.running = False  # 运行状态标记

    def run(self):
        """线程主方法，初始化监听器"""
        self.running = True
        try:
            trigger_key = self.task.get("triggerkey", "").strip()
            if not trigger_key:
                self.send.emit("触发键不能为空", 0, False, False)
                return

            # 解析触发键
            trigger_list = [key.strip().upper() for key in trigger_key.split("+") if key.strip()]
            self._parse_trigger_keys(trigger_list)

            # 根据触发键类型启动相应监听器
            if self.trigger_click:
                self._start_mouse_listener()
            else:
                self._start_keyboard_listener(trigger_key)
        finally:
            self.running = False

    def _parse_trigger_keys(self, trigger_list):
        """解析触发键列表，区分鼠标键和修饰键"""
        for key in trigger_list:
            if key in TRIGGER_MOUSE_LIST:
                self.trigger_click = key
                # 提取修饰键（排除鼠标键的其他键）
                self.trigger_modify = next(
                    (k for k in trigger_list if k != self.trigger_click and k not in TRIGGER_MOUSE_LIST),
                    None
                )
                break

    def _start_mouse_listener(self):
        """启动鼠标监听器"""
        trigger_button = TRIGGER_MAP[self.trigger_click].lower()

        # 根据触发模式和是否有修饰键选择回调函数
        if self.trigger_modify:
            callback = self._on_click_with_modifier
        else:
            callback = self._on_click_without_modifier

        # 启动鼠标监听
        self.mouse_listener = pynput.mouse.Listener(on_click=callback)
        self.mouse_listener.start()

        # 保持线程运行
        while self.running and self.mouse_listener.is_alive():
            self.msleep(100)

    def _start_keyboard_listener(self, trigger_key):
        """启动键盘监听器"""
        if self.mode_trigger == "长按模式":
            # 长按模式：按下时启动，释放时停止
            def on_press(event):
                if keyboard.is_pressed(trigger_key) and not self.clicker.running:
                    self.clicker.start()

            def on_release(event):
                if not keyboard.is_pressed(trigger_key) and self.clicker.running:
                    self.clicker.stop()

            self.keyboard_listener = keyboard.on_press(on_press)
            keyboard.on_release_key(trigger_key.split("+")[-1], on_release)
        else:
            # 短按模式：切换点击器状态
            def toggle_clicker():
                if self.clicker.running:
                    self.clicker.stop()
                else:
                    self.clicker.start()

            # 循环等待按键触发
            while self.running:
                keyboard.wait(trigger_key)
                toggle_clicker()
                # 防止快速重复触发
                time.sleep(0.1)

    def _on_click_with_modifier(self, x, y, button, pressed):
        """带修饰键的鼠标点击回调"""
        if button.name.lower() != TRIGGER_MAP[self.trigger_click].lower():
            return

        # 检查修饰键是否按下
        modifier_pressed = keyboard.is_pressed(self.trigger_modify) if self.trigger_modify else True

        if modifier_pressed:
            if self.mode_trigger == "长按模式":
                if pressed and not self.clicker.running:
                    self.clicker.start()
                elif not pressed and self.clicker.running:
                    self.clicker.stop()
            else:  # 短按模式
                if pressed:
                    if self.clicker.running:
                        self.clicker.stop()
                    else:
                        self.clicker.start()

    def _on_click_without_modifier(self, x, y, button, pressed):
        """无修饰键的鼠标点击回调"""
        if button.name.lower() != TRIGGER_MAP[self.trigger_click].lower():
            return

        if self.mode_trigger == "长按模式":
            if pressed and not self.clicker.running:
                self.clicker.start()
            elif not pressed and self.clicker.running:
                self.clicker.stop()
        else:  # 短按模式
            if pressed:
                if self.clicker.running:
                    self.clicker.stop()
                else:
                    self.clicker.start()

    def kill(self):
        """停止触发器和点击器"""
        self.running = False
        # 停止点击器
        if self.clicker.running:
            self.clicker.stop()
        # 停止鼠标监听器
        if self.mouse_listener and self.mouse_listener.is_alive():
            self.mouse_listener.stop()
        # 停止键盘监听器
        if self.keyboard_listener:
            keyboard.unhook(self.keyboard_listener)
        # 等待线程结束
        self.wait()