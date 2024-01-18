from .timer.main import Timer
from ui.element.control import *


class Overall:
    def __init__(self, stack):
        self.widget = Widget()
        stack.addWidget(self.widget)
        Label(self.widget, (0, 0, 80, 40), "全局设置", 18)
        Line(self.widget, (0, 43, 620, 3))
        self.timer = Timer(self.widget, (0, 60, 620, 300))
        Line(self.widget, (0, 300, 620, 3))
        self.auto_update = Check(self.widget, (0, 310, 120, 40), "自动检查更新")
        self.button_update = Button(self.widget, (130, 315, 100, 30), "检查并更新")
        self.version = self.get_ver()
        Label(self.widget, (245, 310, 1200, 40), f"版本号 {self.version}", 14)

    @staticmethod
    def get_ver():
        t = open("assets/main_window/version.txt", 'r', encoding='utf-8')
        return t.readline().rstrip("\n")
