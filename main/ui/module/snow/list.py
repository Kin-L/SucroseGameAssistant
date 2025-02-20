from main.ui.control import (PicButton, Button, Check,
                             Combobox, ScrollArea, QtWidgets,
                             Label, tips, Swicher)


class SnowList:
    def __init__(self, widget):
        # 功能列表窗口
        self.scroll = ScrollArea(widget, (0, 0, 215, 515))
        self.scroll.setFrameShape(QtWidgets.QFrame.Shape(0))
        # 设置控件
        setpath = "assets/main_window/ui/set.png"
        self.set_snow = PicButton(self.scroll, (180, 10, 22, 22), setpath, (22, 22))

        self.check_fight = Check(self.scroll, (15, 50, 140, 22), "感知扫荡")
        self.check_daily = Check(self.scroll, (15, 95, 140, 22), "日常周常")
        self.check_mail = Check(self.scroll, (15, 140, 140, 22), "领取邮件")
        self.check_roll = Check(self.scroll, (15, 185, 140, 22), "共鸣记录")

        self.set_fight = PicButton(self.scroll, (180, 50, 22, 22), setpath, (22, 22))
        self.set_daily = PicButton(self.scroll, (180, 95, 22, 22), setpath, (22, 22))
        self.set_mail = PicButton(self.scroll, (180, 140, 22, 22), setpath, (22, 22))
        self.set_roll = PicButton(self.scroll, (180, 185, 22, 22), setpath, (22, 22))

        self.button_start = Button(self.scroll, (70, 225, 80, 35), "启动游戏")
        tips(self.button_start, '快捷启动游戏，不执行任务')

        self.button_switch = Swicher(self.scroll, (30, 470, 100, 35))
        self.button_switch.setOffText("小开关未开启")
        self.button_switch.setOnText("小开关已开启")
        tips(self.button_switch, '使用西山居启动器，需要将游戏安装在启动器目录下')

        # 临时功能
        self.button_tem = Button(self.scroll, (70, 280, 120, 35), "开始临时任务")
        self.combo_tem = Combobox(self.scroll, (70, 320, 120, 32))
        self.combo_tem.addItems(["简单", "普通", "困难", "险恶", "异星守护"])
        _text = ('请进入验证战场页面，自行配置好队伍和buff\n'
                 '辰星放一号位，选够三个队友推荐辰星幽潮豹豹\n'
                 '异星守护自行进入页面，配置队友')
        tips(self.button_tem, _text)
