from sgacode.ui.control import (Button, Widget, Label,
                                Combobox, Check,
                                ScrollArea, Timepicker)
from sgacode.tools.sgagroup import sg
from PyQt5.QtCore import QTime


class TimerWindow(Widget):
    def __init__(self, widget, location: (int, int, int, int)):
        super().__init__(widget, location)
        # 时间条目控制
        self.lbitemchange = Label(self, (0, 0, 100, 30), "定时任务：")
        self.btdelete = Button(self, (540, 0, 80, 30), "清除定时")
        # 时间条目标签
        self.lbexecute = Label(self, (35, 30, 50, 30), "执行")
        self.lbtimer = Label(self, (205, 30, 50, 30), "定时")
        self.lbtext = Label(self, (415, 30, 80, 30), "配置选择")
        self.lbawake = Label(self, (565, 30, 60, 30), "唤醒")
        # 时间条目列表
        self.sratime = ScrollArea(self, (0, 65, 620, 120))
        self.wdtime = TimerWidget(self, (0, 0, 620, 120))
        self.sratime.setWidget(self.wdtime)
        self.wdtime.SetConfig(sg.mainconfig['TimerConfig'])


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
        tl = ["<未选择>"] + list(sg.subconfig.GetFileListT()[2])
        self.text0.addItems(tl)
        self.text1.addItems(tl)
        self.text2.addItems(tl)
        self.text3.addItems(tl)
        self.text4.addItems(tl)
        self.text5.addItems(tl)
        self.text6.addItems(tl)
        self.text7.addItems(tl)
        self.text8.addItems(tl)
        self.text9.addItems(tl)

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

    def SetConfig(self, config: dict):
        _list = config['Execute']
        self.execute0.setCurrentIndex(_list[0])
        self.execute1.setCurrentIndex(_list[1])
        self.execute2.setCurrentIndex(_list[2])
        self.execute3.setCurrentIndex(_list[3])
        self.execute4.setCurrentIndex(_list[4])
        self.execute5.setCurrentIndex(_list[5])
        self.execute6.setCurrentIndex(_list[6])
        self.execute7.setCurrentIndex(_list[7])
        self.execute8.setCurrentIndex(_list[8])
        self.execute9.setCurrentIndex(_list[9])
        _list = config['Time']
        self.timer0.setTime(QTime(*_list[0]))
        self.timer1.setTime(QTime(*_list[1]))
        self.timer2.setTime(QTime(*_list[2]))
        self.timer3.setTime(QTime(*_list[3]))
        self.timer4.setTime(QTime(*_list[4]))
        self.timer5.setTime(QTime(*_list[5]))
        self.timer6.setTime(QTime(*_list[6]))
        self.timer7.setTime(QTime(*_list[7]))
        self.timer8.setTime(QTime(*_list[8]))
        self.timer9.setTime(QTime(*_list[9]))
        _list = list(map(lambda x: -1 if not x else list(sg.subconfig.GetFileListT()[0]).index(x), config['Name']))
        self.text0.setCurrentIndex(_list[0]+1)
        self.text1.setCurrentIndex(_list[1]+1)
        self.text2.setCurrentIndex(_list[2]+1)
        self.text3.setCurrentIndex(_list[3]+1)
        self.text4.setCurrentIndex(_list[4]+1)
        self.text5.setCurrentIndex(_list[5]+1)
        self.text6.setCurrentIndex(_list[6]+1)
        self.text7.setCurrentIndex(_list[7]+1)
        self.text8.setCurrentIndex(_list[8]+1)
        self.text9.setCurrentIndex(_list[9]+1)
        _list = config['Awake']
        self.awake0.setChecked(_list[0])
        self.awake1.setChecked(_list[1])
        self.awake2.setChecked(_list[2])
        self.awake3.setChecked(_list[3])
        self.awake4.setChecked(_list[4])
        self.awake5.setChecked(_list[5])
        self.awake6.setChecked(_list[6])
        self.awake7.setChecked(_list[7])
        self.awake8.setChecked(_list[8])
        self.awake9.setChecked(_list[9])

    def CollectConfig(self):
        _dict = dict()
        _dict['Execute'] = [
            self.execute0.currentIndex(),
            self.execute1.currentIndex(),
            self.execute2.currentIndex(),
            self.execute3.currentIndex(),
            self.execute4.currentIndex(),
            self.execute5.currentIndex(),
            self.execute6.currentIndex(),
            self.execute7.currentIndex(),
            self.execute8.currentIndex(),
            self.execute9.currentIndex(), ]
        qtime0 = self.timer0.getTime()
        qtime1 = self.timer1.getTime()
        qtime2 = self.timer2.getTime()
        qtime3 = self.timer3.getTime()
        qtime4 = self.timer4.getTime()
        qtime5 = self.timer5.getTime()
        qtime6 = self.timer6.getTime()
        qtime7 = self.timer7.getTime()
        qtime8 = self.timer8.getTime()
        qtime9 = self.timer9.getTime()

        _dict['Time'] = [
            [qtime0.hour(), qtime0.minute()],
            [qtime1.hour(), qtime1.minute()],
            [qtime2.hour(), qtime2.minute()],
            [qtime3.hour(), qtime3.minute()],
            [qtime4.hour(), qtime4.minute()],
            [qtime5.hour(), qtime5.minute()],
            [qtime6.hour(), qtime6.minute()],
            [qtime7.hour(), qtime7.minute()],
            [qtime8.hour(), qtime8.minute()],
            [qtime9.hour(), qtime9.minute()], ]
        _list = [
            self.text0.currentIndex()-1,
            self.text1.currentIndex()-1,
            self.text2.currentIndex()-1,
            self.text3.currentIndex()-1,
            self.text4.currentIndex()-1,
            self.text5.currentIndex()-1,
            self.text6.currentIndex()-1,
            self.text7.currentIndex()-1,
            self.text8.currentIndex()-1,
            self.text9.currentIndex()-1, ]
        _dict['Name'] = list(map(lambda x: "" if x < 0 else sg.subconfig.GetFileListT()[0][x], _list))
        _dict['Awake'] = [
            self.awake0.isChecked(),
            self.awake1.isChecked(),
            self.awake2.isChecked(),
            self.awake3.isChecked(),
            self.awake4.isChecked(),
            self.awake5.isChecked(),
            self.awake6.isChecked(),
            self.awake7.isChecked(),
            self.awake8.isChecked(),
            self.awake9.isChecked(), ]
        return _dict
