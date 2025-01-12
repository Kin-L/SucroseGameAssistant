# -*- coding: utf-8 -*-
import time
from PyQt5.QtCore import QThread, pyqtSignal
from tools.environment import *
import keyboard
clicker_mouse_list = ["LCLICK", "RCLICK", "MCLICK"]
from win32api import mouse_event, keybd_event
click_map = {"LCLICK": (2, 4), "RCLICK": (8, 16), "MCLICK": (32, 64)}
key_map = {
        "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57,
        'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 117, 'F7': 118, 'F8': 119,
        'F9': 120, 'F10': 121, 'F11': 122, 'F12': 123, 'F13': 124, 'F14': 125, 'F15': 126, 'F16': 127,
        "A": 65, "B": 66, "C": 67, "D": 68, "E": 69, "F": 70, "G": 71, "H": 72, "I": 73, "J": 74,
        "K": 75, "L": 76, "M": 77, "N": 78, "O": 79, "P": 80, "Q": 81, "R": 82, "S": 83, "T": 84,
        "U": 85, "V": 86, "W": 87, "X": 88, "Y": 89, "Z": 90,
        'BACKSPACE': 8, 'TAB': 9, 'TABLE': 9, 'CLEAR': 12,
        'ENTER': 13, 'SHIFT': 16, 'CTRL': 17,
        'CONTROL': 17, 'ALT': 18, 'ALTER': 18, 'PAUSE': 19, 'BREAK': 19, 'CAPSLK': 20, 'CAPSLOCK': 20, 'ESC': 27,
        'SPACE': 32, 'SPACEBAR': 32, 'PGUP': 33, 'PAGEUP': 33, 'PGDN': 34, 'PAGEDOWN': 34, 'END': 35, 'HOME': 36,
        'LEFT': 37, 'UP': 38, 'RIGHT': 39, 'DOWN': 40, 'SELECT': 41, 'PRTSC': 42, 'PRINTSCREEN': 42, 'SYSRQ': 42,
        'SYSTEMREQUEST': 42, 'EXECUTE': 43, 'SNAPSHOT': 44, 'INSERT': 45, 'DELETE': 46, 'HELP': 47, 'WIN': 91,
        'WINDOWS': 91, 'NMLK': 144, "VOLUMEMUTE": 173,
        'NUMLK': 144, 'NUMLOCK': 144, 'SCRLK': 145,
        '[': 219, ']': 221, '+': 107, '-': 109, '~': 192, '`': 192, "/": 191,
        ',': 188, '.': 190, "\\": 220, "'": 222, ";": 186, "*": 106}


class Clicker(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.interval = None
        self.mode_clicker = None
        self.clicker_list = []

    def run(self):
        self.mode_clicker = self.task["ClickerMode"]
        self.clicker_list = self.task["clickerkey"].strip(" ").upper().split("+")
        if self.mode_clicker == "连点模式":  # 连点模式
            self.interval = float(self.task["interval"])
            cf = False
            for i in self.clicker_list:
                i.strip(" ")
                if i in clicker_mouse_list:
                    cf = True
            _t = self.interval / 1000
            if cf:
                _n1, _n2 = click_map[self.clicker_list[0]]
                while 1:
                    mouse_event(_n1, 0, 0)
                    sleep(0.01)
                    mouse_event(_n2, 0, 0)
                    sleep(_t)
            else:
                if len(self.clicker_list) == 1:
                    key_num = key_map[self.clicker_list[0].upper()]
                    while 1:
                        keybd_event(key_num, 0, 0, 0)
                        keybd_event(key_num, 0, 2, 0)
                        sleep(_t)
                elif len(self.clicker_list) == 2:
                    key_num0 = key_map[self.clicker_list[0].upper()]
                    key_num1 = key_map[self.clicker_list[1].upper()]
                    while 1:
                        keybd_event(key_num0, 0, 0, 0)
                        keybd_event(key_num1, 0, 0, 0)
                        keybd_event(key_num1, 0, 2, 0)
                        keybd_event(key_num0, 0, 2, 0)
                        sleep(_t)
                elif len(self.clicker_list) == 3:
                    key_num0 = key_map[self.clicker_list[0].upper()]
                    key_num1 = key_map[self.clicker_list[1].upper()]
                    key_num2 = key_map[self.clicker_list[2].upper()]
                    while 1:
                        keybd_event(key_num0, 0, 0, 0)
                        keybd_event(key_num1, 0, 0, 0)
                        keybd_event(key_num2, 0, 0, 0)
                        keybd_event(key_num2, 0, 2, 0)
                        keybd_event(key_num1, 0, 2, 0)
                        keybd_event(key_num0, 0, 2, 0)
                        sleep(_t)
        elif self.mode_clicker == "按下模式":  # 按下模式
            for i in self.clicker_list:
                if i in clicker_mouse_list:
                    clickdown(i)
                else:
                    keydown(i)
        elif self.mode_clicker == "脚本模式":  # 脚本模式
            if self.task["runnum"] < 1:
                while 1:
                    self.sc_run()
            else:
                for i in range(self.task["runnum"]):
                    self.sc_run()
        keyboard.wait()

    def sc_run(self):
        sc_list = self.task["script"]
        for func, value in sc_list:
            eval(func)(value)

