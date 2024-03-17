from tools.image import *
from tools.keymouse import *


class Operate(KeyMouse, Image):
    def click_text(self, target: str, zone="ALL",
                   search_path: str = "", delete_flag: int = 1):
        _list = self.ocr(zone, search_path, 1, delete_flag)
        for t in _list:
            if target in t[0]:
                xy = self.center(t[1])
                self.click(xy)
                return True
        return False

    def click_pic(self, target: str, sim: float = 0.6, zone="ALL",
                  search_path: str = "", delete_flag: int = 1):
        xy, _sim = self.find_pic(target, zone, search_path, delete_flag)
        if _sim >= sim:
            self.click(xy)
            return True
        else:
            return False


