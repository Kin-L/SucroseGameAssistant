from sgacode.ui.control import (Button, Widget, Label,
                                PicButton, Combobox, Check,
                                ScrollArea, Timepicker)


class TimerWindow(Widget):
    def __init__(self, widget, location: (int, int, int, int)):
        super().__init__(widget, location)
        self.timeitem = 3
        # 时间条目控制
        self.lbitemchange = Label(self, (0, 0, 100, 30), "时间条目增减")
        
        addpath = r"resources/main/button/add.png"
        deducepath = r"resources/main/button/reduce.png"
        applypath = r"resources/main/button/save.png"
        sizetp = (20, 20) 
        self.pbadd = PicButton(self, (110, 0, 30, 30), addpath, sizetp)
        self.pbdeduce = PicButton(self, (150, 0, 30, 30), deducepath, sizetp)
        self.pbapply = PicButton(self, (190, 0, 30, 30), applypath, sizetp)
        self.btdelete = Button(self, (540, 0, 80, 30), "清除定时")
        # 时间条目标签
        self.lbexecute = Label(self, (35, 30, 50, 30), "执行")
        self.lbtimer = Label(self, (205, 30, 50, 30), "定时")
        self.lbtext = Label(self, (415, 30, 80, 30), "配置选择")
        self.lbawake = Label(self, (565, 30, 60, 30), "唤醒")
        # 时间条目列表
        self.sratime = ScrollArea(self, (0, 65, 620, 120))
        self.wdtime = Widget(self, (0, 0, 620, 120))
        _wdt = self.wdtime
        self.sratime.setWidget(_wdt)
        self.wdtime.setFixedHeight(120)
        # self.scroll_time_item.setFrameShape(QtWidgets.QFrame.Shape(0))
        # 时间条目按钮
        _wdt.execute0 = Combobox(_wdt, (5, 5, 90, 30))
        _wdt.execute1 = Combobox(_wdt, (5, 45, 90, 30))
        _wdt.execute2 = Combobox(_wdt, (5, 85, 90, 30))
        _wdt.execute3 = Combobox(_wdt, (5, 125, 90, 30))
        _wdt.execute4 = Combobox(_wdt, (5, 165, 90, 30))
        _wdt.execute5 = Combobox(_wdt, (5, 205, 90, 30))
        _wdt.execute6 = Combobox(_wdt, (5, 245, 90, 30))
        _wdt.execute7 = Combobox(_wdt, (5, 285, 90, 30))
        _wdt.execute8 = Combobox(_wdt, (5, 325, 90, 30))
        _wdt.execute9 = Combobox(_wdt, (5, 365, 90, 30))
        _list = ["禁用", "每日", "周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        _wdt.execute0.addItems(_list)
        _wdt.execute1.addItems(_list)
        _wdt.execute2.addItems(_list)
        _wdt.execute3.addItems(_list)
        _wdt.execute4.addItems(_list)
        _wdt.execute5.addItems(_list)
        _wdt.execute6.addItems(_list)
        _wdt.execute7.addItems(_list)
        _wdt.execute8.addItems(_list)
        _wdt.execute9.addItems(_list)

        _wdt.timer0 = Timepicker(_wdt, (100, 5, 50, 30))
        _wdt.timer1 = Timepicker(_wdt, (100, 45, 50, 30))
        _wdt.timer2 = Timepicker(_wdt, (100, 85, 50, 30))
        _wdt.timer3 = Timepicker(_wdt, (100, 125, 50, 30))
        _wdt.timer4 = Timepicker(_wdt, (100, 165, 50, 30))
        _wdt.timer5 = Timepicker(_wdt, (100, 205, 50, 30))
        _wdt.timer6 = Timepicker(_wdt, (100, 245, 50, 30))
        _wdt.timer7 = Timepicker(_wdt, (100, 285, 50, 30))
        _wdt.timer8 = Timepicker(_wdt, (100, 320, 50, 30))
        _wdt.timer9 = Timepicker(_wdt, (100, 360, 50, 30))

        _wdt.text0 = Combobox(_wdt, (345, 5, 210, 30))
        _wdt.text1 = Combobox(_wdt, (345, 45, 210, 30))
        _wdt.text2 = Combobox(_wdt, (345, 85, 210, 30))
        _wdt.text3 = Combobox(_wdt, (345, 125, 210, 30))
        _wdt.text4 = Combobox(_wdt, (345, 165, 210, 30))
        _wdt.text5 = Combobox(_wdt, (345, 205, 210, 30))
        _wdt.text6 = Combobox(_wdt, (345, 245, 210, 30))
        _wdt.text7 = Combobox(_wdt, (345, 285, 210, 30))
        _wdt.text8 = Combobox(_wdt, (345, 325, 210, 30))
        _wdt.text9 = Combobox(_wdt, (345, 365, 210, 30))
        
        _str = " "
        _wdt.awake0 = Check(_wdt, (570, 5, 30, 30), _str)
        _wdt.awake1 = Check(_wdt, (570, 45, 30, 30), _str)
        _wdt.awake2 = Check(_wdt, (570, 85, 30, 30), _str)
        _wdt.awake3 = Check(_wdt, (570, 125, 30, 30), _str)
        _wdt.awake4 = Check(_wdt, (570, 165, 30, 30), _str)
        _wdt.awake5 = Check(_wdt, (570, 205, 30, 30), _str)
        _wdt.awake6 = Check(_wdt, (570, 245, 30, 30), _str)
        _wdt.awake7 = Check(_wdt, (570, 285, 30, 30), _str)
        _wdt.awake8 = Check(_wdt, (570, 325, 30, 30), _str)
        _wdt.awake9 = Check(_wdt, (570, 365, 30, 30), _str)

        _str = "<未选择>"
        _wdt.text0.addItem(_str)
        _wdt.text1.addItem(_str)
        _wdt.text2.addItem(_str)
        _wdt.text3.addItem(_str)
        _wdt.text4.addItem(_str)
        _wdt.text5.addItem(_str)
        _wdt.text6.addItem(_str)
        _wdt.text7.addItem(_str)
        _wdt.text8.addItem(_str)
        _wdt.text9.addItem(_str)
