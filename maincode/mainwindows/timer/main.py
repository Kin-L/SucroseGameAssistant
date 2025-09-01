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
            getattr(_tw, f"text{i}").addItems(tl)
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
            getattr(_tw, f"execute{i}").setCurrentIndex(_list0[i])
            getattr(_tw, f"timer{i}").setTime(QTime(*_list1[i]))
            getattr(_tw, f"text{i}").setCurrentIndex(_list2[i] + 1)
            getattr(_tw, f"awake{i}").setChecked(_list3[i])

    def CollectConfig(self):
        _tw = self.widgets.wdtime
        _dict = dict()

        _dict['Execute'] = [getattr(_tw, f"execute{i}").currentIndex() for i in range(10)]
        _dict['Time'] = [[getattr(_tw, f'timer{i}').getTime().hour(),
                          getattr(_tw, f'timer{i}').getTime().minute()]
                         for i in range(10)]
        _list = [getattr(_tw, f'text{i}').currentIndex() - 1 for i in range(10)]
        _dict['ConfigKeys'] = list(map(lambda x: "" if x < 0 else sg.subconfig.GetFilesT()[0][x], _list))
        _dict['Awake'] = [getattr(_tw, f'awake{i}').isChecked() for i in range(10)]
        return _dict
