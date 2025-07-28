import time
import keyboard
from PyQt5.QtCore import QThread
from maincode.tools.myclass import SGAStop


def snowRogue(self):
    _list = self.ctler.ocr(mode=1)
    result = self.ctler.StrFind("难度选择", _list)
    if not result:
        self.send("请先进入验证战场界面")
        return
    else:
        self.send("开始验证战场")
    self.trigger = TemTrigger()
    try:
        while 1:
            xy_list = [(383, 400), (767, 404), (1161, 427), (1541, 443)]
            try:
                self.ctler.clickChange(xy_list[self.para["roguediff"]], zone=(102, 22, 301, 84))
            except TimeoutError:
                _list = self.ctler.ocr(mode=1)
                if self.ctler.StrFind("难度选择", _list):
                    self.send("今日悖论迷宫次数已消耗殆尽")
                    self.send("验证战场结束")
                    return
                else:
                    raise TimeoutError
            self.ctler.clickChange(target="开始", zone=(1694, 944, 1885, 1051))
            self.ctler.wait(1)
            _list = self.ctler.ocr(mode=1)
            if self.ctler.StrFind("确定", _list):
                self.ctler.clickChange(target="确定", zone=(1365, 719, 1580, 816))
            self.ctler.wait(3)
            _list1 = [(106, 781, 597, 881),
                      (804, 799, 1113, 850),
                      (1428, 800, 1745, 852)]
            _list2 = [(329, 829), (972, 822), (1561, 826)]
            while 1:
                _sc = self.ctler.screenshot()
                _t1 = self.ctler.ocr((33, 65, 146, 122), _sc)[0]
                if "波" in _t1:
                    if not self.trigger.isRunning():
                        self.trigger.Stop = False
                        self.trigger.start()
                _t2 = self.ctler.ocr((901, 963, 1013, 1036), _sc)[0]
                if "确认" in _t2:
                    self.trigger.Stop = True
                    self.trigger.quit()
                    self.ctler.wait(0.3)
                    _sc = self.ctler.screenshot()
                    pos = (329, 829)
                    for p, i in zip(_list2, _list1):
                        if not self.ctler.ocr(i, _sc)[0]:
                            pos = p
                            break
                    while 1:
                        self.ctler.click(pos)
                        self.ctler.wait(0.3)
                        self.ctler.click((965, 1008))
                        self.ctler.wait(0.5)
                        _t3 = self.ctler.ocr((231, 955, 1053, 1050))[0]
                        if "确认" in _t3:
                            continue
                        elif "丢弃" in _t3:
                            self.ctler.click((1298, 677))
                            self.ctler.wait(0.3)
                            try:
                                self.ctler.clickChange((1566, 988), zone=(1503, 955, 1623, 1019))
                            except:
                                self.ctler.click((311, 993))
                                self.ctler.wait(0.3)
                                self.ctler.clickChange(target="确定", zone=(1356, 733, 1552, 800))
                            break
                        else:
                            break
                elif "退出" in _t2:
                    self.trigger.Stop = True
                    self.trigger.quit()
                    self.ctler.clickChange(target="退出", zone=(896, 946, 1004, 1018))
                    self.ctler.waitTo(target="选", zone=(73, 8, 328, 92), wait=(1, 30))
                    break
                else:
                    self.ctler.wait(0.5)
    except SGAStop or TimeoutError:
        if self.trigger.isRunning():
            self.trigger.Stop = True
            self.trigger.quit()
            self.trigger.wait()
        raise SGAStop


class TemTrigger(QThread):

    def __init__(self):  # mode true:集成运行 false:独立运行
        super().__init__()
        from maincode.tools.controller.main import ctler
        self.ctler = ctler
        self.Stop = False

    def run(self):
        while not self.Stop:
            keyboard.send("e")
            time.sleep(0.8)
