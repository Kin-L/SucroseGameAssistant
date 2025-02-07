from ui.element.control import *


class SnowList:
    def __init__(self, widget, location):
        # 功能列表窗口
        scroll = ScrollArea(widget, location)
        scroll.setFrameShape(QtWidgets.QFrame.Shape(0))
        # 设置控件
        self.label_snow = Label(scroll, (75, 10, 80, 20), "尘白禁区", 18)
        setpath = "assets/main_window/ui/set.png"
        self.set_snow = PicButton(scroll, (180, 10, 22, 22), setpath, (22, 22))

        self.check_fight = Check(scroll, (15, 50, 140, 22), "感知扫荡")
        self.check_daily = Check(scroll, (15, 95, 140, 22), "日常周常")
        self.check_mail = Check(scroll, (15, 140, 140, 22), "领取邮件")
        self.check_roll = Check(scroll, (15, 185, 140, 22), "共鸣记录")

        self.set_fight = PicButton(scroll, (180, 50, 22, 22), setpath, (22, 22))
        self.set_daily = PicButton(scroll, (180, 95, 22, 22), setpath, (22, 22))
        self.set_mail = PicButton(scroll, (180, 140, 22, 22), setpath, (22, 22))
        self.set_roll = PicButton(scroll, (180, 185, 22, 22), setpath, (22, 22))

        self.button_start = Button(scroll, (70, 225, 80, 35), "启动游戏")

        self.button_switch = Swicher(scroll, (30, 470, 100, 35))
        self.button_switch.setOffText("小开关未开启")
        self.button_switch.setOnText("小开关已开启")

        # 临时功能
        self.button_tem = Button(scroll, (70, 280, 120, 35), "开始验证战场")
        self.combo_tem = Combobox(scroll, (70, 320, 120, 32))
        self.combo_tem.addItems(["简单", "普通", "困难", "险恶"])
        self.button_tem.setToolTip('请进入验证战场页面，自行配置好队伍和buff，辰星放一号位')
        self.button_tem.installEventFilter(
            ToolTipFilter(self.button_tem,
                          showDelay=200,
                          position=ToolTipPosition.TOP))

