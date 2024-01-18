# -*- coding:gbk -*-
from ui.element.control import *


class KleinList:
    def __init__(self, widget, location):
        # 功能列表窗口
        scroll = ScrollArea(widget, location)
        scroll.setFrameShape(QtWidgets.QFrame.Shape(0))
        # 设置控件
        self.label_klein = Label(scroll, (75, 10, 80, 20), "环行旅舍", 18)
        setpath = "assets/main_window/ui/set.png"
        self.set_klein = PicButton(scroll, (180, 10, 22, 22), setpath, (22, 22))

        self.check_fight = Check(scroll, (15, 50, 140, 22), "作战/重游")
        self.check_disp = Check(scroll, (15, 95, 140, 22), "线下采购")
        self.check_review = Check(scroll, (15, 140, 140, 22), "战术回顾")
        self.check_market = Check(scroll, (15, 185, 140, 22), "集市领取")
        self.check_recruit = Check(scroll, (15, 230, 140, 22), "舍友访募")
        self.check_reward = Check(scroll, (15, 275, 140, 22), "今日工作")
        self.check_network = Check(scroll, (15, 320, 140, 22), "卡门商网")
        self.check_mail = Check(scroll, (15, 365, 140, 22), "领取邮件")
        self.check_roll = Check(scroll, (15, 410, 140, 22), "抽卡历史")

        self.set_fight = PicButton(scroll, (180, 50, 22, 22), setpath, (22, 22))
        self.set_disp = PicButton(scroll, (180, 95, 22, 22), setpath, (22, 22))
        self.set_review = PicButton(scroll, (180, 140, 22, 22), setpath, (22, 22))
        self.set_market = PicButton(scroll, (180, 185, 22, 22), setpath, (22, 22))
        self.set_recruit = PicButton(scroll, (180, 230, 22, 22), setpath, (22, 22))
        self.set_reward = PicButton(scroll, (180, 275, 22, 22), setpath, (22, 22))
        self.set_network = PicButton(scroll, (180, 320, 22, 22), setpath, (22, 22))
        self.set_mail = PicButton(scroll, (180, 365, 22, 22), setpath, (22, 22))
        self.set_roll = PicButton(scroll, (180, 410, 22, 22), setpath, (22, 22))