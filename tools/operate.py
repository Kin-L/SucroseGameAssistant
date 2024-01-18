from tools.image import *
from tools.keymouse import *


class Operate(KeyMouse, Image):
    def click_text(self, target: str, zone="ALL",
                   search_path: str = "", delete_flag: int = 1):
        _list = self.ocr(zone, search_path, 1, delete_flag)
        print(_list)
        for t in _list:
            if target in t[0]:
                x, y = self.center(t[1])
                self.click(x, y)
                return True
        return False

    def click_pic(self, target: str, sim: float = 0.6, zone="ALL",
                  search_path: str = "", delete_flag: int = 1):
        (x, y), _sim = self.find_pic(target, zone, search_path, delete_flag)
        if _sim >= sim:
            self.click(x, y)
            return True
        else:
            return False
