from maincode.mainwindows.mainwidgets.main import SGAMain1
from PyQt5.QtCore import QTimer, QThread
from maincode.thread.task import SGAMainThread


class SGAMain2(SGAMain1):
    def __init__(self, userui):
        super().__init__(userui)
        from .maingroup import sg
        self.SG = sg
        if self.loadui:
            self.SG.infoHead.connect(self.infoHead)
            self.SG.infoAdd.connect(self.infoAdd)
            self.SG.infoEnd.connect(self.infoEnd)
        self.SG.Load()
        self.timer = QTimer(self)
        self.sleeptime = 0

    def NewThread(self, tasktype, para):
        try:
            self.thread.deleteLater()
        except:
            ...
        self.thread = SGAMainThread(tasktype, para)
        # self.thread = QThread()
        # self.taskthread.moveToThread(self.thread)
        self.thread.infoHead.connect(self.infoHead)
        self.thread.infoAdd.connect(self.infoAdd)
        self.thread.infoEnd.connect(self.infoEnd)
