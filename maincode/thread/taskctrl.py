import keyboard
from time import localtime, sleep
from maincode.main.maingroup import sg
from maincode.mainwindows.main import SGAMain6
from PyQt5.QtCore import QTimer


class SGAMain7(SGAMain6):
    def __init__(self, userui):
        super().__init__(userui)
        self.module.btstart.clicked.connect(lambda: self.TaskStart("current"))
        self.module.btpause.clicked.connect(self.ManualStop)
        self.timerallow = True

    def TaskStart(self, tasktype: str, para=None):
        # print("TaskStart")
        sg.info.TaskError = False
        sg.info.StopFlag = False
        self.timerallow = False
        self.module.statesigh.SetState(0)
        sg.info.OcrPath = sg.mainconfig.OcrPath
        keyboard.remove_all_hotkeys()
        self.module.btstart.setDisabled(True)
        self.module.btstart.hide()
        if tasktype == "current":
            self.infoClear()
            self.infoHead()
            self.SaveConfig()
            para = dict(sg.mainconfig.CurrentConfig)
            para["OtherConfig"] = sg.mainconfig.OtherConfig
            self.NewThread(tasktype, para)
            self.thread.started.connect(self.taskthread.run)
            self.thread.finished.connect(lambda: self.TaskStop(tasktype, para))
            self.taskthread.finish.connect(self.NormalFinish)
            self.thread.start()
            self.infoAdd("开始执行实时任务")
            self.module.btpause.setEnabled(True)
            self.module.btpause.show()
            keyboard.add_hotkey(sg.mainconfig.StopKeys, self.ManualStop)
        elif tasktype == "timed":
            self.infoClear()
            self.infoHead()
            self.infoAdd("准备开始...")
            para["OtherConfig"] = sg.mainconfig.OtherConfig
            self.NewThread(tasktype, para)
            self.thread.started.connect(self.taskthread.run)
            self.thread.finished.connect(lambda: self.TaskStop(tasktype, para))
            self.taskthread.finish.connect(self.NormalFinish)
            self.thread.start()
            name = para["ConfigName"]
            self.infoAdd(f"开始执行定时任务：{name}")
            self.module.btpause.setEnabled(True)
            self.module.btpause.show()
            keyboard.add_hotkey(sg.mainconfig.StopKeys, self.ManualStop)
        elif tasktype == "update":
            self.infoHead()
            self.infoAdd("准备开始...")
            para["OtherConfig"] = sg.mainconfig.OtherConfig
            self.NewThread(tasktype, para)
            self.thread.started.connect(self.taskthread.run)
            self.thread.finished.connect(lambda: self.TaskStop(tasktype, para))
            self.taskthread.finish.connect(self.NormalFinish)
            self.thread.start()
            self.infoAdd("开始更新")

    def TaskStop(self, tasktype: str, para=None):
        sg.info.StopFlag = None
        self.window.foreground()
        if sg.info.TaskError:
            self.module.statesigh.SetState(2)
        self.infoAdd("任务结束")
        self.infoEnd()
        self.module.btstart.setEnabled(True)
        self.module.btstart.show()
        self.module.btpause.setEnabled(True)
        self.module.btpause.hide()
        keyboard.remove_all_hotkeys()
        keyboard.add_hotkey("ctrl+s", self.SaveConfig)
        if tasktype == "timed":
            sleeptime = 46 - localtime()[5]
            self.sleeptime = sleeptime if sleeptime > 0 else 0
        elif tasktype == "update":
            self.overall.btcheckupdate.setEnabled(True)
        self.timerallow = True

    def ManualStop(self):
        self.module.btpause.setDisabled(True)
        self.infoAdd("手动终止,等待结束")
        keyboard.remove_all_hotkeys()
        sg.info.StopFlag = True
        self.module.statesigh.SetState(1)
        self.thread.quit()
        self.thread.wait(),  # 可选：等待线程结束
        self.module.btpause.hide()
        self.taskthread.deleteLater()
        self.thread.deleteLater()

    def NormalFinish(self):
        self.module.btpause.setDisabled(True)
        keyboard.remove_all_hotkeys()
        self.thread.quit()
        self.thread.wait(),  # 可选：等待线程结束
        self.module.btpause.hide()
        self.taskthread.deleteLater()
        self.thread.deleteLater()
