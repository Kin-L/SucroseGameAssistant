# -*- coding:gbk -*-
from ui.element.control import *


class MixList:
    def __init__(self, widget, location):  # 0, 0, 215, 515
        # 功能列表窗口
        self.scroll = ScrollArea(widget, location)
        self.scroll.setFrameShape(QtWidgets.QFrame.Shape(0))
        self.widget = Widget(self.scroll, (0, 0, 215, 515))
        self.widget.setMinimumSize(215, 515)
        self.scroll.setWidget(self.widget)
        self.scroll.setFrameShape(QtWidgets.QFrame.Shape(0))
        # 运行列表窗口
        self.label_continuous = Label(self.widget, (75, 10, 80, 20), "连续任务", 18)
        self.combobox_mix_config0 = Combobox(self.widget, (0, 50, 210, 30))
        self.combobox_mix_config1 = Combobox(self.widget, (0, 90, 210, 30))
        self.combobox_mix_config2 = Combobox(self.widget, (0, 130, 210, 30))
        self.combobox_mix_config3 = Combobox(self.widget, (0, 170, 210, 30))
        self.combobox_mix_config4 = Combobox(self.widget, (0, 210, 210, 30))
