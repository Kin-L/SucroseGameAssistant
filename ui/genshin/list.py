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

        #文本
        self.check_way0 = Label(self.widget, (50, 50, 140, 22), "运行方式")
        self.check_team = Check(self.widget, (15, 95, 140, 22), "切换队伍")
        self.check_disp = Check(self.widget, (15, 140, 140, 22), "探索派遣")
        self.check_trans = Check(self.widget, (15, 185, 140, 22), "参量质变仪")
        self.check_fly = Check(self.widget, (15, 230, 140, 22), "自动晶蝶")
        self.check_pot = Check(self.widget, (15, 275, 140, 22), "尘歌壶")
        self.check_mail = Check(self.widget, (15, 320, 140, 22), "领取邮件")
        self.check_tree = Check(self.widget, (15, 365, 140, 22), "自动伐木")
        self.check_daily = Check(self.widget, (15, 410, 140, 22), "体力日常")
        self.check_pass = Check(self.widget, (15, 455, 140, 22), "领取纪行")

        #齿轮按钮
        self.set_way0 = PicButton(self.widget, (180, 50, 22, 22), setpath, (22, 22))
        self.set_team = PicButton(self.widget, (180, 95, 22, 22), setpath, (22, 22))
        self.set_disp = PicButton(self.widget, (180, 140, 22, 22), setpath, (22, 22))
        self.set_trans = PicButton(self.widget, (180, 185, 22, 22), setpath, (22, 22))
        self.set_fly = PicButton(self.widget, (180, 230, 22, 22), setpath, (22, 22))
        self.set_pot = PicButton(self.widget, (180, 275, 22, 22), setpath, (22, 22))
        self.set_mail = PicButton(self.widget, (180, 320, 22, 22), setpath, (22, 22))
        self.set_tree = PicButton(self.widget, (180, 365, 22, 22), setpath, (22, 22))
        self.set_daily = PicButton(self.widget, (180, 410, 22, 22), setpath, (22, 22))
        self.set_pass = PicButton(self.widget, (180, 455, 22, 22), setpath, (22, 22))
