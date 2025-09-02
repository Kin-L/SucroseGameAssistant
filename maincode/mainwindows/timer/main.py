from .widget import TimerWidgets
from maincode.config.maingroup import sg
from PyQt5.QtCore import QTime
from .function import timer_delete
from maincode.tools.main import GetTracebackInfo, logger
from maincode.mainwindows.mainwindow import SGAQMainWindow


class SGATimer:
    def __init__(self, wighet, location, SQMW: SGAQMainWindow):
        self.infoHead = SQMW.infoHead
        self.infoAdd = SQMW.infoAdd
        self.infoEnd = SQMW.infoEnd
        self.widgets = TimerWidgets(wighet, location)

        _tw = self.widgets.wdtime
        tl = ["<未选择>"] + list(sg.subconfig.GetFilesT()[1])
        for i in range(10):
            _tw.texts[i].addItems(tl)
        self.SetConfig(sg.mainconfig.TimerConfig.model_dump())
        self.widgets.btdelete.clicked.connect(self.DeleteTimer)

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
        _tw = self.widgets.wdtime
        _list0 = config['Execute']
        _list1 = config['Time']
        _list2 = list(map(lambda x: -1 if not x else list(sg.subconfig.GetFilesT()[0]).index(x), config['ConfigKeys']))
        _list3 = config['Awake']
        for i in range(10):
            _tw.executes[i].setCurrentIndex(_list0[i])
            _tw.timers[i].setTime(QTime(*_list1[i]))
            _tw.texts[i].setCurrentIndex(_list2[i] + 1)
            _tw.awakes[i].setChecked(_list3[i])

    def CollectConfig(self):
        _tw = self.widgets.wdtime
        config_dict = {
            'Execute': [],
            'Time': [],
            'ConfigKeys': [],
            'Awake': []
        }
        text_indices = []
        for i in range(10):
            config_dict['Execute'].append(_tw.executes[i].currentIndex())
            config_dict['Time'].append([_tw.timers[i].getTime().hour(), _tw.timers[i].getTime().minute()])
            text_indices.append(_tw.texts[i].currentIndex() - 1)
            config_dict['Awake'].append(_tw.awakes[i].isChecked())
        config_dict['ConfigKeys'] = list(map(lambda x: "" if x < 0 else sg.subconfig.GetFilesT()[0][x], text_indices))
        return config_dict
