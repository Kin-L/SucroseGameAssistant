from ui.element.ui_part import Independent
from ui.element.control import *


class MixStack:
    def __init__(self, widget, location):
        # 功能堆叠窗口
        self.stack = Stack(widget, location)
        # 功能堆叠窗口
        self.widget_set = Widget(self.stack, (0, 0, 395, 515))
        self.label_local = Label(self.widget_set, (0, 12, 220, 18), "设置页面：连续任务 运行方式")
        self.line0 = Line(self.widget_set, (0, 41, 395, 3))
        self.independent = Independent(self.widget_set, (0, 50, 350, 70), False)
