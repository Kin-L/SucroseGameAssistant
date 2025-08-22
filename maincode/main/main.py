from maincode.mainwindows.mainwidgets.main import SGAMain1
from PyQt5.QtCore import QTimer, QThread
from maincode.thread.task import SGAMainThread
from maincode.tools.main import logger


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
        logger.info(self.SG.info.GetEnvironmentInfoStr())
        self.timer = QTimer(self)
        self.sleeptime = 0

    def NewThread(self, tasktype, para):
        self.thread = QThread()
        self.worker = SGAMainThread(tasktype, para)

        # 将工作对象移动到线程中
        self.worker.moveToThread(self.thread)
        # self.thread = QThread()
        # self.taskthread.moveToThread(self.thread)
        self.worker.infoHead.connect(self.infoHead)
        self.worker.infoAdd.connect(self.infoAdd)
        self.worker.infoEnd.connect(self.infoEnd)

