# import pywintypes
import keyboard
import pyautogui
from time import sleep
from maincode.tools.myclass import CtrlBase, ADBController


class KeyMouse(CtrlBase, ADBController):
    def click(self, pos=None, key="left"):
        """
        :param pos: (x, y)
        :param key: "left" "right" "middle"
        :return:
        """
        self.checkrun()
        pos = (None, None) if pos is None else self.convert(pos)
        pyautogui.click(*pos, button=key)

    def clickdown(self, pos=None, key="left"):
        self.checkrun()
        pyautogui.mouseDown(*(None, None) if pos is None else self.convert(pos), button=key)

    def clickup(self, pos=None, key="left"):
        self.checkrun()
        pyautogui.mouseUp(*(None, None) if pos is None else self.convert(pos), button=key)
    
    def moveto(self, pos):
        self.checkrun(), pyautogui.moveTo(*self.convert(pos))
    
    def move(self, pos):
        self.checkrun(), pyautogui.moveRel(*self.convertVector(pos))
    
    def roll(self, pos, num, hori=False):
        self.checkrun()
        self.moveto(pos)
        self.wait(0.2)
        if hori:
            pyautogui.hscroll(num)
        else:
            pyautogui.vscroll(num)
        
    def dragto(self, pos, button='left', duration=0.8):
        self.checkrun()
        pyautogui.dragTo(*self.convert(pos), duration=duration, button=button)

    def dragrel(self, vec, button='left', duration=0.8):
        self.checkrun()
        pyautogui.dragRel(*self.convertVector(vec), duration=duration, button=button)

    def press(self, _key):
        self.checkrun(), keyboard.send(_key)

    def keydown(self, _key):
        self.checkrun(), keyboard.press(_key)

    def keyup(self, _key):
        self.checkrun(), keyboard.release(_key)

    def wait(self, t):  # 单位秒
        a, b = divmod(t, 1)
        a = int(a)
        for i in [1] * a + [b] if b else [1] * a:
            self.checkrun()
            sleep(i)

    def tap(self, para, duration_ms=100):
        """
        :param para: tuple: 坐标(0, 0) str：功能键 "KEYCODE_BACK" "KEYCODE_HOME" "KEYCODE_APP_SWITCH"
        :param duration_ms: 持续时间
        :return:
        """
        self.checkrun()
        if isinstance(para, tuple):
            x, y = self.convert(para)
            if duration_ms <= 100:
                self._exec_shell_command(f"input tap {x} {y}")
            else:
                self._exec_shell_command(f"input swipe {x} {y} {x} {y} {duration_ms}")
        elif isinstance(para, str):
            self._exec_shell_command(f"input keyevent {para}")

    def swip(self, pos1, pos2, duration_ms=500):
        self.checkrun()
        x1, y1 = self.convert(pos1)
        x2, y2 = self.convert(pos2)
        self._exec_shell_command(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")


if __name__ == '__main__':
    pass
