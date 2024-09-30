# import pywintypes
from win32api import mouse_event, SetCursorPos, keybd_event
from win32con import KEYEVENTF_KEYUP
from .system import *
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
        'WINDOWS': 91, 'NMLK': 144,
        'NUMLK': 144, 'NUMLOCK': 144, 'SCRLK': 145,
        '[': 219, ']': 221, '+': 107, '-': 109, '~': 192, '`': 192, "/": 111}


class KeyMouse(System):
    def move(self, xy):
        x, y = xy
        SetCursorPos(self.axis_change(x, y))

    def click(self, xy):
        x, y = xy
        if (x, y) != (0, 0):
            x, y = self.axis_change(x, y)
            SetCursorPos((x, y))
        mouse_event(2, x, y)
        mouse_event(4, x, y)

    def drag(self, pos, mov):
        xp, yp = self.axis_change(pos[0], pos[1])
        xv, yv = self.axis_zoom(mov[0], mov[1])
        SetCursorPos((xp, yp))
        from pyautogui import dragRel
        dragRel(xv, yv, duration=1, button='left')

    def roll(self, xy, num):
        x, y = xy
        x, y = self.axis_change(x, y)
        SetCursorPos((x, y))
        self.wait(0.1)
        if num > 0:
            u = 1
        else:
            u = -1
            num = -1 * num
        for i in range(num):
            mouse_event(0x0800, 0, 0, 120 * u, 0)
            self.wait(0.01)

    def roll_h(self, xy, num):
        x, y = xy
        x, y = self.axis_change(x, y)
        SetCursorPos((x, y))
        self.wait(0.1)
        if num > 0:
            u = 1
        else:
            u = -1
            num = -1 * num
        for i in range(num):
            mouse_event(0x01000, 0, 0, -120 * u, 0)
            self.wait(0.01)

    @staticmethod
    def press(key):
        key_num = key_map[key.upper()]
        keybd_event(key_num, 0, 0, 0)
        keybd_event(key_num, 0, KEYEVENTF_KEYUP, 0)

    @staticmethod
    def keydown(key):
        key_num = key_map[key.upper()]
        keybd_event(key_num, 0, 0, 0)

    @staticmethod
    def keyup(key):
        key_num = key_map[key.upper()]
        keybd_event(key_num, 0, KEYEVENTF_KEYUP, 0)

    @staticmethod
    def key_add(key1, key2):
        key_num1 = key_map[key1.upper()]
        key_num2 = key_map[key2.upper()]
        keybd_event(key_num1, 0, 0, 0)  # ctrl按下
        keybd_event(key_num2, 0, 0, 0)  # a按下
        keybd_event(key_num2, 0, 0, 0)  # a抬起
        keybd_event(key_num1, 0, 0, 0)  # ctrl抬起

    @staticmethod
    def wait(t):
        sleep(t / 1000)


if __name__ == '__main__':
    pass
