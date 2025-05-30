import keyboard
from PyQt5.QtCore import QThread, pyqtSignal
from tools.environment import *
from tools.software import find_hwnd


class Monitor(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui, _num):
        super().__init__()
        self.ui = ui
        self.num = _num
        self.trigger = TemTrigger(self)

    def run(self):
        try:
            self.indicate("开始临时任务")
            keyboard.add_hotkey("ctrl+/", self.stop)
            env.OCR.enable()
            p1 = (0, "UnrealWindow", "尘白禁区")
            p2 = (0, "UnrealWindow", "Snowbreak: Containment Zone")
            _h = find_hwnd(p1)
            if not _h:
                _h = find_hwnd(p2)
                if not _h:
                    self.indicate("未识别到窗口")
                    env.OCR.disable()
                    raise SGAStop
                else:
                    _p = p2
            else:
                _p = p1
            env.set_soft(self.ui.set.line_start.text(), _p)
            env.soft.hwnd = _h
            env.soft.run()
            env.soft.compile_resolution = (1920, 1080)
            env.mode(3)
            env.soft.foreground()
            if self.num == 4:
                while 1:
                    _sc = scshot()
                    _t1 = ocr((1392, 96, 1517, 150), _sc)[0]
                    if "关卡" in _t1:
                        click((1738, 997))
                        wait(3000)
                    else:
                        click((955, 507))
                        wait(500)
                        click((961, 991))
                        wait(500)
                        continue
            _list = ocr(mode=1)
            result = str_find("试用队员", _list)
            if result:
                click_change((1752, 988), (1613, 946, 1766, 1014))
                wait(500)
            else:
                result = str_find("难度选择", _list)
                if result:
                    pass
                else:
                    self.indicate("请先进入验证战场界面")
                    self.ui.temkill.terminate()
                    self.terminate()

            while 1:
                xy_list = [(383, 400), (767, 404), (1161, 427), (1541, 443)]
                click_change(xy_list[self.num], (102, 22, 301, 84))
                wait(500)
                click_text("开始", (1694, 944, 1885, 1051))
                wait(3000)
                _list1 = [(106, 781, 597, 881),
                          (702, 771, 1238, 898),
                          (1358, 790, 1794, 878)]
                _list2 = [(329, 829), (972, 822), (1561, 826)]
                while 1:
                    _sc = scshot()
                    _t1 = ocr((33, 65, 146, 122), _sc)[0]
                    if "波" in _t1:
                        if not self.trigger.isRunning():
                            self.trigger.start()
                    _t2 = ocr((901, 963, 1013, 1036), _sc)[0]
                    if "确认" in _t2:
                        if self.trigger.isRunning():
                            self.trigger.terminate()
                        while 1:
                            click((329, 829))
                            wait(600)
                            click((965, 1008))
                            wait(800)
                            _sc = scshot()
                            _t3 = ocr((231, 955, 1053, 1050), _sc)[0]
                            if "确认" in _t3:
                                continue
                            elif "丢弃" in _t3:
                                click_text("丢弃", (251, 952, 383, 1033))
                                wait(1000)
                                click_text("确定", (1384, 717, 1534, 807))
                                wait(800)
                            else:
                                break
                        if not self.trigger.isRunning():
                            self.trigger.start()
                    elif "退出" in _t2:
                        if self.trigger.isRunning():
                            self.trigger.terminate()
                        click_text("退出", (896, 946, 1004, 1018))
                        wait_text("选", (73, 8, 328, 92), wait_time=(1000, 30))
                        break
                    wait(500)
        except SGAStop:
            sgs.set_state(None)
        except:
            self.indicate("任务执行异常:尘白禁区", log=False)
            logger.error("任务执行异常：验证战场\n%s" % format_exc())
        self.indicate("停止临时任务")

    def indicate(self, msg: str, mode=2, his=True, log=True):
        self.send.emit(msg, mode, his, log)

    def stop(self):
        env.OCR.disable()
        sgs.set_state(False)
        keyboard.remove_all_hotkeys()


class TemTrigger(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui):  # mode true:集成运行 false:独立运行
        super().__init__()
        self.ui = ui

    def run(self):
        try:
            while 1:
                press("e")
                wait(800)
        except SGAStop:
            pass
