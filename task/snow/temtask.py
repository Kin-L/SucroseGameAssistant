from PyQt5.QtCore import QThread, pyqtSignal
from tools.environment import *
from tools.software import find_hwnd


class Monitor(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui, _num):  # mode true:集成运行 false:独立运行
        super().__init__()
        self.ui = ui
        self.num = _num
        self.trigger = TemTrigger(self)

    def run(self):
        try:
            self.indicate("开始验证战场")
            env.OCR.enable()
            _h = find_hwnd((0, "UnrealWindow", "尘白禁区"))
            if not _h:
                _h = find_hwnd((0, "UnrealWindow", "Snowbreak: Containment Zone"))
                if not _h:
                    self.indicate("未识别到窗口")
                    self.ui.temkill.terminate()
                    self.terminate()
            foreground(_h)
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
                    _t2 = ocr((819, 22, 1087, 124), _sc)[0]
                    if "选择" in _t2:
                        if self.trigger.isRunning():
                            self.trigger.terminate()
                        _sc = scshot()
                        for i in range(3):
                            _tt = ocr(_list1[i], _sc)[0]
                            if "增益" in _tt:
                                continue
                            else:
                                click(_list2[i])
                                wait(800)
                                click_text("确认", (901, 963, 1013, 1036))
                                wait(800)
                                break
                        else:
                            click((329, 829))
                            wait(800)
                            click_text("确认", (901, 963, 1013, 1036))
                            wait(800)
                        _tt2 = find_text("丢弃", (251, 952, 383, 1033))
                        if _tt2:
                            try:
                                click_change((1522, 681), (1506, 950, 1621, 1028))
                                wait(800)
                                click_change((1566, 989), (1506, 950, 1621, 1028))
                                wait(800)
                            except:
                                click_text("丢弃", (251, 952, 383, 1033))
                                wait(1000)
                                click((1458, 777))
                                wait(800)
                        if not self.trigger.isRunning():
                            self.trigger.start()
                    _t3 = ocr((896, 946, 1004, 1018), _sc)[0]
                    if "出" in _t3:
                        if self.trigger.isRunning():
                            self.trigger.terminate()
                        click_text("退出", (896, 946, 1004, 1018))
                        wait_text("难度选择", (73, 8, 328, 92), wait_time=(1000, 30))
                        break
                    wait(500)
        except:
            self.indicate("任务执行异常:尘白禁区", log=False)
            logger.error("任务执行异常：验证战场\n%s" % format_exc())

    def indicate(self, msg: str, mode=2, his=True, log=True):
        self.send.emit(msg, mode, his, log)


class TemTrigger(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui):  # mode true:集成运行 false:独立运行
        super().__init__()
        self.ui = ui

    def run(self):
        while 1:
            press("e")
            wait(800)


class TemKill(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui):  # mode true:集成运行 false:独立运行
        super().__init__()
        self.ui = ui

    def run(self):
        # noinspection PyBroadException
        import keyboard
        keyboard.wait("ctrl+/")
        # noinspection PyBroadException
        try:
            if self.ui.text_monitor.trigger.isRunning():
                self.ui.text_monitor.trigger.terminate()
            if self.ui.text_monitor.isRunning():
                self.ui.text_monitor.terminate()
            self.indicate("停止验证战场任务")
        except Exception:
            self.indicate("关闭线程错误")

    def indicate(self, msg: str, mode=2, his=True, log=True):
        self.send.emit(msg, mode, his, log)
