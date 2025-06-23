from maincode.tools.controls import (Button, Widget, Label,
                                     Combobox, Check, tips,
                                     ScrollArea, Timepicker)


class TimerWidgets(Widget):
    def __init__(self, widget, location: (int, int, int, int)):
        super().__init__(widget, location)
        # 时间条目控制
        self.lbitemchange = Label(self, (0, 0, 100, 30), "定时任务：")
        self.btdelete = Button(self, (540, 0, 80, 30), "清除定时")
        tips(self.btdelete, "取消SGA自启和唤醒行为")

        # 时间条目标签
        self.lbexecute = Label(self, (35, 30, 50, 30), "执行")
        self.lbtimer = Label(self, (205, 30, 50, 30), "定时")
        self.lbtext = Label(self, (415, 30, 80, 30), "配置选择")
        self.lbawake = Label(self, (565, 30, 60, 30), "唤醒")
        # 时间条目列表
        self.sratime = ScrollArea(self, (0, 65, 620, 120))
        self.wdtime = TimerWidget(self, (0, 0, 620, 120))
        self.sratime.setWidget(self.wdtime)
        # self.wdtime.SetConfig(self.TimerConfig.model_dump())


class TimerWidget(Widget):
    def __init__(self, widget: Widget, loc):
        super().__init__(widget, loc)
        self.setFixedHeight(400)
        # self.scroll_time_item.setFrameShape(QtWidgets.QFrame.Shape(0))
        # 时间条目按钮
        self.execute0 = Combobox(self, (5, 5, 90, 30))
        self.execute1 = Combobox(self, (5, 45, 90, 30))
        self.execute2 = Combobox(self, (5, 85, 90, 30))
        self.execute3 = Combobox(self, (5, 125, 90, 30))
        self.execute4 = Combobox(self, (5, 165, 90, 30))
        self.execute5 = Combobox(self, (5, 205, 90, 30))
        self.execute6 = Combobox(self, (5, 245, 90, 30))
        self.execute7 = Combobox(self, (5, 285, 90, 30))
        self.execute8 = Combobox(self, (5, 325, 90, 30))
        self.execute9 = Combobox(self, (5, 365, 90, 30))
        _list = ["禁用", "每日", "周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        self.execute0.addItems(_list)
        self.execute1.addItems(_list)
        self.execute2.addItems(_list)
        self.execute3.addItems(_list)
        self.execute4.addItems(_list)
        self.execute5.addItems(_list)
        self.execute6.addItems(_list)
        self.execute7.addItems(_list)
        self.execute8.addItems(_list)
        self.execute9.addItems(_list)

        self.timer0 = Timepicker(self, (100, 5, 50, 30))
        self.timer1 = Timepicker(self, (100, 45, 50, 30))
        self.timer2 = Timepicker(self, (100, 85, 50, 30))
        self.timer3 = Timepicker(self, (100, 125, 50, 30))
        self.timer4 = Timepicker(self, (100, 165, 50, 30))
        self.timer5 = Timepicker(self, (100, 205, 50, 30))
        self.timer6 = Timepicker(self, (100, 245, 50, 30))
        self.timer7 = Timepicker(self, (100, 285, 50, 30))
        self.timer8 = Timepicker(self, (100, 320, 50, 30))
        self.timer9 = Timepicker(self, (100, 360, 50, 30))

        self.text0 = Combobox(self, (345, 5, 210, 30))
        self.text1 = Combobox(self, (345, 45, 210, 30))
        self.text2 = Combobox(self, (345, 85, 210, 30))
        self.text3 = Combobox(self, (345, 125, 210, 30))
        self.text4 = Combobox(self, (345, 165, 210, 30))
        self.text5 = Combobox(self, (345, 205, 210, 30))
        self.text6 = Combobox(self, (345, 245, 210, 30))
        self.text7 = Combobox(self, (345, 285, 210, 30))
        self.text8 = Combobox(self, (345, 325, 210, 30))
        self.text9 = Combobox(self, (345, 365, 210, 30))

        _str = " "
        self.awake0 = Check(self, (570, 5, 30, 30), _str)
        self.awake1 = Check(self, (570, 45, 30, 30), _str)
        self.awake2 = Check(self, (570, 85, 30, 30), _str)
        self.awake3 = Check(self, (570, 125, 30, 30), _str)
        self.awake4 = Check(self, (570, 165, 30, 30), _str)
        self.awake5 = Check(self, (570, 205, 30, 30), _str)
        self.awake6 = Check(self, (570, 245, 30, 30), _str)
        self.awake7 = Check(self, (570, 285, 30, 30), _str)
        self.awake8 = Check(self, (570, 325, 30, 30), _str)
        self.awake9 = Check(self, (570, 365, 30, 30), _str)
