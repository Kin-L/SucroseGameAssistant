import keyboard
from time import localtime
from maincode.main.maingroup import sg
from maincode.mainwindows.main import SGAMainWindow
from maincode.tools.main import CmdRun, GetMute, ScreenOff, logger, GetTracebackInfo
from PyQt5.QtWidgets import QApplication
from maincode.tools.main import killprocess, GetPid
from .task import SGAMainThread
from PyQt5.QtCore import QThread
from maincode.tools.constant import spr


def TaskStart(self: SGAMainWindow, tasktype: str, para: dict = None):
    if para is None:
        para = dict()
    try:
        while v := GetPid("PaddleOCR-json.exe"):
            killprocess(v)
        # print("TaskStart")
        sg.info.TaskError = False
        sg.info.StopFlag = False
        self.timerallow = False
        self.module.statesigh.SetState(0)
        sg.info.OcrPath = sg.mainconfig.OcrPath
        self.module.btstart.setDisabled(True)
        self.module.btstart.hide()
        if tasktype == "current":
            self.infoClear()
            self.infoHead()
            self.SaveConfig()
            para.update(dict(sg.mainconfig.CurrentConfig))
            para["OtherConfig"] = sg.mainconfig.OtherConfig
            para["current_mute"] = GetMute()
            self.NewThread(tasktype, para)
            self.infoAdd("开始执行实时任务")
            self.module.btpause.setEnabled(True)
            self.module.btpause.show()
            keyboard.add_hotkey(sg.mainconfig.StopKeys, self.module.btpause.click)
        elif tasktype == "timed":
            self.infoClear()
            self.infoHead()
            self.infoAdd("准备开始...")
            para["OtherConfig"] = sg.mainconfig.OtherConfig
            para["current_mute"] = GetMute()
            self.NewThread(tasktype, para)
            name = para["ConfigName"]
            self.infoAdd(f"开始执行定时任务：{name}")
            self.module.btpause.setEnabled(True)
            self.module.btpause.show()
            keyboard.add_hotkey(sg.mainconfig.StopKeys, self.module.btpause.click)
        elif tasktype == "update":
            self.infoHead()
            self.infoAdd("准备开始...")
            self.NewThread(tasktype, para)
    except Exception as e:
        _str = GetTracebackInfo(e) + "准备开始流程异常"
        logger.error(_str)
        self.infoAdd(f"准备开始流程异常")


def TaskStop(self: SGAMainWindow, tasktype: str, para=None):
    try:
        self.window.foreground()
        if sg.info.TaskError:
            self.module.statesigh.SetState(2)
        self.infoEnd()
        self.timerallow = True
        self.module.btstart.setEnabled(True)
        self.module.btstart.show()
        self.module.btpause.setEnabled(True)
        self.module.btpause.hide()
        if tasktype == "timed":
            sleeptime = 61 - localtime()[5]
            self.sleeptime = sleeptime if sleeptime > 0 else 0
            keyboard.remove_all_hotkeys()
        elif tasktype == "update":
            self.widget.btcheckupdate.setEnabled(True)
            keyboard.remove_all_hotkeys()
            return
        if para["Mute"] and (GetMute() != para["current_mute"]):
            keyboard.send('volume mute')
        # 结束
        if sg.info.StopFlag:
            para["Finished"] = 0
            para["SGAClose"] = False
        sg.info.StopFlag = None
        if para["Finished"] == 1:
            if para["SGAClose"]:
                self.infoAdd("SGA关闭 电脑熄屏")
                self.infoEnd()
                CmdRun("start "" /d \"resources/main/script\" screen_off.vbs")
                app = QApplication.instance()
                if app:
                    app.quit()
            else:
                self.infoAdd("SGA等待 电脑熄屏")
                self.infoEnd()
                ScreenOff()
        elif para["Finished"] == 2:
            if para["SGAClose"]:
                self.infoAdd("SGA关闭 电脑睡眠")
                self.infoEnd()
                CmdRun("start "" /d \"resources/main/script\" sleep.vbs")
                app = QApplication.instance()
                if app:
                    app.quit()
            else:
                self.infoAdd("SGA等待 电脑睡眠")
                self.infoEnd()
                CmdRun("start "" /d \"resources/main/script\" sleep.vbs")
        else:
            if para["SGAClose"]:
                self.infoAdd("SGA关闭 电脑无操作")
                self.infoEnd()
                app = QApplication.instance()
                if app:
                    app.quit()
            else:
                self.infoAdd("SGA等待 电脑无操作")
                self.infoEnd()
    except Exception as e:
        _str = GetTracebackInfo(e) + "终止流程异常"
        logger.error(_str)
        self.infoAdd(f"终止流程异常")


def ManualStop(self):
    try:
        if not self.timerallow:
            self.module.btpause.setDisabled(True)
            self.infoAdd("手动终止,等待结束...")
            self.timerallow = True
            sg.info.StopFlag = True
            self.module.statesigh.SetState(1)
            try:
                self.worker.quit()
                self.worker.wait()  # 可选：等待线程结束
                self.module.btpause.hide()
                self.worker.deleteLater()
                self.thread.quit()
                self.thread.wait()
                self.thread.deleteLater()
            except:
                ...
    except Exception as e:
        _str = GetTracebackInfo(e) + "手动终止流程异常"
        logger.error(_str)
        self.infoAdd(f"手动终止流程异常")


def NewThread(self: SGAMainWindow, tasktype, para):
    self.thread = QThread()
    self.worker = SGAMainThread(tasktype, para)

    # 将工作对象移动到线程中
    self.worker.moveToThread(self.thread)
    # self.thread = QThread()
    # self.taskthread.moveToThread(self.thread)
    self.worker.infoHead.connect(self.infoHead)
    self.worker.infoAdd.connect(self.infoAdd)
    self.worker.infoEnd.connect(self.infoEnd)
    self.thread.started.connect(self.worker.run)
    self.worker.finished.connect(self.thread.quit)
    self.worker.finished.connect(self.worker.deleteLater)
    self.thread.finished.connect(lambda: TaskStop(tasktype, para))
    self.thread.finished.connect(self.thread.deleteLater)
    self.thread.start()


SGAMainWindow.TaskStart = TaskStart
SGAMainWindow.TaskStop = TaskStop
SGAMainWindow.ManualStop = ManualStop
