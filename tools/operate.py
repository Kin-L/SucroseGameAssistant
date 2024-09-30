from tools.image import *
from tools.keymouse import *


class Operate(KeyMouse, Image):
    def click_text(self, target: str, zone="ALL", pos=None,
                   wait_time=(800, 10), once=False, template: str = ""):
        if once:
            _list = self.ocr(zone, template, 1)
            result = str_find(target, _list)
            if result:
                self.click(result)
                return True
            else:
                return False
        else:
            while 1:
                for i in range(wait_time[1]):
                    _list = self.ocr(zone, template, 1)
                    result = str_find(target, _list)
                    if result:
                        if pos:
                            self.click(pos)
                        else:
                            self.click(result)
                        sleep(wait_time[0] / 1000)
                        _list = self.ocr(zone, template, 1)
                        result = str_find(target, _list)
                        if not result:
                            return True
                    sleep(wait_time[0] / 1000)
                if self.soft.isforeground():
                    raise RuntimeError("识别超时")
                else:
                    self.soft.foreground()
                    self.logger.info("切换顶层窗口")

    def click_pic(self, target, zone="ALL", sim: float = 0.6, pos=None,
                  wait_time=(800, 10), once=False, template: str = ""):
        if once:
            xy, _sim = self.find_pic(target, zone, template)
            if _sim >= sim:
                self.click(xy)
                return True
            else:
                return False
        else:
            if isinstance(target, ndarray):
                _target = target
            elif target:
                if not isfile(target):
                    print("error: findpic 参数 small_pic 为无效路径。")
                    raise ValueError("error: findpic 参数 small_pic 为无效路径。")
                else:
                    _target = imread(target)
            else:
                print("error: findpic 参数 small_pic 为无效路径。")
                raise ValueError("error: findpic 参数 small_pic 为无效路径。")
            while 1:
                for i in range(wait_time[1]):
                    p, s = self.find_pic(_target, zone, template)
                    if s >= sim:
                        if pos:
                            self.click(pos)
                        else:
                            self.click(p)
                        sleep(wait_time[0] / 1000)
                        p, s = self.find_pic(_target, zone, template)
                        if s < sim:
                            return True
                    sleep(wait_time[0] / 1000)
                if self.soft.isforeground():
                    raise RuntimeError("识别超时")
                else:
                    self.soft.foreground()
                    self.logger.info("切换顶层窗口")

    def press_text(self, key, target: str, zone="ALL",
                   wait_time=(800, 10), once=False, template: str = ""):
        if once:
            _list = self.ocr(zone, template, 1)
            result = str_find(target, _list)
            if result:
                self.click(result)
                return True
            else:
                return False
        else:
            while 1:
                for i in range(wait_time[1]):
                    _list = self.ocr(zone, template, 1)
                    result = str_find(target, _list)
                    if result:
                        self.press(key)
                        sleep(wait_time[0] / 1000)
                        _list = self.ocr(zone, template, 1)
                        result = str_find(target, _list)
                        if not result:
                            return True
                    sleep(wait_time[0] / 1000)
                if self.soft.isforeground():
                    raise RuntimeError("识别超时")
                else:
                    self.soft.foreground()
                    self.logger.info("切换顶层窗口")

    def press_pic(self, key, target, zone="ALL", sim: float = 0.6,
                  wait_time=(800, 10), once=False, template: str = ""):
        if once:
            xy, _sim = self.find_pic(target, zone, template)
            if _sim >= sim:
                self.click(xy)
                return True
            else:
                return False
        else:
            if isinstance(target, ndarray):
                _target = target
            elif target:
                if not isfile(target):
                    print("error: findpic 参数 small_pic 为无效路径。")
                    raise ValueError("error: findpic 参数 small_pic 为无效路径。")
                else:
                    _target = imread(target)
            else:
                print("error: findpic 参数 small_pic 为无效路径。")
                raise ValueError("error: findpic 参数 small_pic 为无效路径。")
            while 1:
                for i in range(wait_time[1]):
                    p, s = self.find_pic(_target, zone, template)
                    if s >= sim:
                        self.press(key)
                        sleep(wait_time[0] / 1000)
                        p, s = self.find_pic(_target, zone, template)
                        if s < sim:
                            return True
                    sleep(wait_time[0] / 1000)
                if self.soft.isforeground():
                    raise RuntimeError("识别超时")
                else:
                    self.soft.foreground()
                    self.logger.info("切换顶层窗口")
