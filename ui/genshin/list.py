# -*- coding:gbk -*-
from ui.element.control import *


class GenshinList:
    def __init__(self, widget, location):
        # 功能列表窗口
        scroll = ScrollArea(widget, location)
        scroll.setFrameShape(QtWidgets.QFrame.Shape(0))
        self.widget = Widget(scroll, (0, 0, 215, 515))
        # 设置控件
        self.label_genshin = Label(self.widget, (95, 10, 92, 20), "原神", 18)
        setpath = "assets/main_window/ui/set.png"
        self.set_genshin = PicButton(self.widget, (180, 10, 22, 22), setpath, (22, 22))

        self.check_team = Check(self.widget, (15, 50, 140, 22), "切换队伍")
        self.check_disp = Check(self.widget, (15, 95, 140, 22), "探索派遣")
        self.check_trans = Check(self.widget, (15, 140, 140, 22), "参量质变仪")
        self.check_fly = Check(self.widget, (15, 185, 140, 22), "自动晶蝶")
        self.check_comp = Check(self.widget, (15, 230, 140, 22), "浓缩树脂")
        self.check_pot = Check(self.widget, (15, 275, 140, 22), "尘歌壶")
        self.check_mail = Check(self.widget, (15, 320, 140, 22), "领取邮件")
        self.check_tree = Check(self.widget, (15, 365, 140, 22), "自动伐木")
        self.check_domain = Check(self.widget, (15, 410, 140, 22), "自动秘境")

        self.set_team = PicButton(self.widget, (180, 50, 22, 22), setpath, (22, 22))
        self.set_disp = PicButton(self.widget, (180, 95, 22, 22), setpath, (22, 22))
        self.set_trans = PicButton(self.widget, (180, 140, 22, 22), setpath, (22, 22))
        self.set_fly = PicButton(self.widget, (180, 185, 22, 22), setpath, (22, 22))
        self.set_comp = PicButton(self.widget, (180, 230, 22, 22), setpath, (22, 22))
        self.set_pot = PicButton(self.widget, (180, 275, 22, 22), setpath, (22, 22))
        self.set_mail = PicButton(self.widget, (180, 320, 22, 22), setpath, (22, 22))
        self.set_tree = PicButton(self.widget, (180, 365, 22, 22), setpath, (22, 22))
        self.set_domain = PicButton(self.widget, (180, 410, 22, 22), setpath, (22, 22))
