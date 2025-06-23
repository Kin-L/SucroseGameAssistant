from ..overall.main import SGAMain3
from maincode.main.maingroup import sg
from PyQt5.QtCore import QTime
from .function import timer_delete
from maincode.tools.main import GetTracebackInfo, logger


class SGAMain4(SGAMain3):
    def __init__(self, userui):
        super().__init__(userui)
        if self.loadui:
            _tw = self.overall.timer.wdtime
            tl = ["<未选择>"] + list(sg.subconfig.GetFilesT()[1])
            _tw.text0.addItems(tl)
            _tw.text1.addItems(tl)
            _tw.text2.addItems(tl)
            _tw.text3.addItems(tl)
            _tw.text4.addItems(tl)
            _tw.text5.addItems(tl)
            _tw.text6.addItems(tl)
            _tw.text7.addItems(tl)
            _tw.text8.addItems(tl)
            _tw.text9.addItems(tl)
            self.SetConfig(sg.mainconfig.TimerConfig.model_dump())
            self.overall.timer.btdelete.clicked.connect(self.DeleteTimer)

    def DeleteTimer(self):
        self.infoHead()
        try:
            timer_delete()
            self.infoAdd("取消SGA自启/唤醒行为", False)
        except Exception as e:
            _str = GetTracebackInfo(e) + "操作异常：取消SGA自启/唤醒行为"
            logger.error(_str)
            self.infoAdd("操作异常：取消SGA自启/唤醒行为", False)
        self.infoEnd()

    def SetConfig(self, config: dict):
        _tw = self.overall.timer.wdtime
        _list = config['Execute']
        _tw.execute0.setCurrentIndex(_list[0])
        _tw.execute1.setCurrentIndex(_list[1])
        _tw.execute2.setCurrentIndex(_list[2])
        _tw.execute3.setCurrentIndex(_list[3])
        _tw.execute4.setCurrentIndex(_list[4])
        _tw.execute5.setCurrentIndex(_list[5])
        _tw.execute6.setCurrentIndex(_list[6])
        _tw.execute7.setCurrentIndex(_list[7])
        _tw.execute8.setCurrentIndex(_list[8])
        _tw.execute9.setCurrentIndex(_list[9])
        _list = config['Time']
        _tw.timer0.setTime(QTime(*_list[0]))
        _tw.timer1.setTime(QTime(*_list[1]))
        _tw.timer2.setTime(QTime(*_list[2]))
        _tw.timer3.setTime(QTime(*_list[3]))
        _tw.timer4.setTime(QTime(*_list[4]))
        _tw.timer5.setTime(QTime(*_list[5]))
        _tw.timer6.setTime(QTime(*_list[6]))
        _tw.timer7.setTime(QTime(*_list[7]))
        _tw.timer8.setTime(QTime(*_list[8]))
        _tw.timer9.setTime(QTime(*_list[9]))
        _list = list(map(lambda x: -1 if not x else list(sg.subconfig.GetFilesT()[0]).index(x), config['ConfigKeys']))
        _tw.text0.setCurrentIndex(_list[0] + 1)
        _tw.text1.setCurrentIndex(_list[1] + 1)
        _tw.text2.setCurrentIndex(_list[2] + 1)
        _tw.text3.setCurrentIndex(_list[3] + 1)
        _tw.text4.setCurrentIndex(_list[4] + 1)
        _tw.text5.setCurrentIndex(_list[5] + 1)
        _tw.text6.setCurrentIndex(_list[6] + 1)
        _tw.text7.setCurrentIndex(_list[7] + 1)
        _tw.text8.setCurrentIndex(_list[8] + 1)
        _tw.text9.setCurrentIndex(_list[9] + 1)
        _list = config['Awake']
        _tw.awake0.setChecked(_list[0])
        _tw.awake1.setChecked(_list[1])
        _tw.awake2.setChecked(_list[2])
        _tw.awake3.setChecked(_list[3])
        _tw.awake4.setChecked(_list[4])
        _tw.awake5.setChecked(_list[5])
        _tw.awake6.setChecked(_list[6])
        _tw.awake7.setChecked(_list[7])
        _tw.awake8.setChecked(_list[8])
        _tw.awake9.setChecked(_list[9])

    def CollectConfig(self):
        _tw = self.overall.timer.wdtime
        _dict = dict()
        _dict['Execute'] = [
            _tw.execute0.currentIndex(),
            _tw.execute1.currentIndex(),
            _tw.execute2.currentIndex(),
            _tw.execute3.currentIndex(),
            _tw.execute4.currentIndex(),
            _tw.execute5.currentIndex(),
            _tw.execute6.currentIndex(),
            _tw.execute7.currentIndex(),
            _tw.execute8.currentIndex(),
            _tw.execute9.currentIndex(), ]
        qtime0 = _tw.timer0.getTime()
        qtime1 = _tw.timer1.getTime()
        qtime2 = _tw.timer2.getTime()
        qtime3 = _tw.timer3.getTime()
        qtime4 = _tw.timer4.getTime()
        qtime5 = _tw.timer5.getTime()
        qtime6 = _tw.timer6.getTime()
        qtime7 = _tw.timer7.getTime()
        qtime8 = _tw.timer8.getTime()
        qtime9 = _tw.timer9.getTime()

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
            _tw.text0.currentIndex() - 1,
            _tw.text1.currentIndex() - 1,
            _tw.text2.currentIndex() - 1,
            _tw.text3.currentIndex() - 1,
            _tw.text4.currentIndex() - 1,
            _tw.text5.currentIndex() - 1,
            _tw.text6.currentIndex() - 1,
            _tw.text7.currentIndex() - 1,
            _tw.text8.currentIndex() - 1,
            _tw.text9.currentIndex() - 1, ]
        _dict['ConfigKeys'] = list(map(lambda x: "" if x < 0 else sg.subconfig.GetFilesT()[0][x], _list))
        _dict['Awake'] = [
            _tw.awake0.isChecked(),
            _tw.awake1.isChecked(),
            _tw.awake2.isChecked(),
            _tw.awake3.isChecked(),
            _tw.awake4.isChecked(),
            _tw.awake5.isChecked(),
            _tw.awake6.isChecked(),
            _tw.awake7.isChecked(),
            _tw.awake8.isChecked(),
            _tw.awake9.isChecked(), ]
        return _dict
