# -*- coding: utf-8 -*-
import keyboard
from .clicker import *
import pynput
trigger_map = {"LCLICK": 'LEFT', "RCLICK": 'RIGHT', "MCLICK": 'MIDDLE',
               'X1CLICK': 'X1', 'X2CLICK': 'X2',
               "0": 48, "1": 49, "2": 50, "3": 51, "4": 52, "5": 53, "6": 54, "7": 55, "8": 56, "9": 57,
               'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 'F6': 117, 'F7': 118, 'F8': 119,
               'F9': 120, 'F10': 121, 'F11': 122, 'F12': 123, 'F13': 124, 'F14': 125, 'F15': 126, 'F16': 127,
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
trigger_mouse_list = ["LCLICK", "RCLICK", "MCLICK", 'X1CLICK', 'X2CLICK']


class Trigger(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, task):
        super().__init__()
        self.task = task
        self.mode_trigger = None
        self.trigger_click = None
        self.trigger_modify = None
        self.mouse_event = None
        self.keyboard_event = None
        self.keyboard_listener = None
        self.mouse_listener = None
        self.clicker = Clicker(task)

        self.trigger_start_click = None
        self.trigger_stop_click = None
        self.trigger_switch_click = None

    def on_click1(self, x, y, button, pressed):
        if [button.name, pressed] == self.trigger_start_click:
            if keyboard.is_pressed(self.trigger_modify):
                self.clicker.start()
        elif [button.name, pressed] == self.trigger_stop_click:
            if self.clicker.isRunning():
                self.clicker.kill()

    def on_click2(self, x, y, button, pressed):
        if [button.name, pressed] == self.trigger_switch_click:
            if keyboard.is_pressed(self.trigger_modify):
                if self.clicker.isRunning():
                    self.clicker.kill()
                else:
                    self.clicker.start()

    def on_click3(self, x, y, button, pressed):
        if [button.name, pressed] == self.trigger_start_click:
            self.clicker.start()
        elif [button.name, pressed] == self.trigger_stop_click:
            if self.clicker.isRunning():
                self.clicker.kill()

    def on_click4(self, x, y, button, pressed):
        if [button.name, pressed] == self.trigger_switch_click:
            if self.clicker.isRunning():
                self.clicker.kill()
            else:
                self.clicker.start()

    def switcher(self):
        if self.clicker.isRunning():
            self.clicker.kill()
        else:
            self.clicker.start()

    def run(self):
        trigger_list = self.task["triggerkey"].strip(" ").upper().split("+")
        print(trigger_list)
        for i in trigger_list:
            i.strip(" ")
            if i in trigger_mouse_list:
                self.trigger_click = i
        if self.trigger_click:
            trigger_list.remove(self.trigger_click)
            if trigger_list:
                self.trigger_modify = trigger_list[0]
            else:
                self.trigger_modify = ""
        self.mode_trigger = self.task["TriggerMode"]
        print(self.trigger_click)
        if self.trigger_click:
            if self.trigger_modify:
                if self.mode_trigger == "长按模式":
                    self.trigger_start_click = [trigger_map[self.trigger_click].lower(), True]
                    self.trigger_stop_click = [trigger_map[self.trigger_click].lower(), False]
                    self.mouse_listener = pynput.mouse.Listener(on_click=self.on_click1)
                    self.mouse_listener.start()
                else:
                    self.trigger_switch_click = [trigger_map[self.trigger_click].lower(), True]
                    self.mouse_listener = pynput.mouse.Listener(on_click=self.on_click2)
                    self.mouse_listener.start()
            else:
                if self.mode_trigger == "长按模式":
                    self.trigger_start_click = [trigger_map[self.trigger_click].lower(), True]
                    self.trigger_stop_click = [trigger_map[self.trigger_click].lower(), False]
                    self.mouse_listener = pynput.mouse.Listener(on_click=self.on_click3)
                    self.mouse_listener.start()
                else:
                    self.trigger_switch_click = [trigger_map[self.trigger_click].lower(), True]
                    self.mouse_listener = pynput.mouse.Listener(on_click=self.on_click4)
                    self.mouse_listener.start()
            keyboard.wait()
        else:
            trigger_key = self.task["triggerkey"]
            if self.mode_trigger == "长按模式":  # 长按
                def on_release_callback(event):
                    if self.clicker.isRunning():
                        self.clicker.kill()

                trigger_key_list = trigger_key.strip(" ").upper().split("+")
                finalkey = trigger_key_list[-1].strip(" ")
                keyboard.on_release_key(finalkey, on_release_callback)
                while 1:
                    keyboard.wait(trigger_key)
                    self.clicker.start()
            else:  # 短按
                keyboard.on_release_key(trigger_key, self.switcher)
                keyboard.wait()

    def kill(self):
        if self.trigger_click:
            if self.mouse_listener.running:
                self.mouse_listener.stop()
        if self.clicker.isRunning():
            self.clicker.kill()
        self.terminate()
