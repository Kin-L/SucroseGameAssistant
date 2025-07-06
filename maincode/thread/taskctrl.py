import keyboard
from time import localtime, sleep
from maincode.main.maingroup import sg
from maincode.mainwindows.main import SGAMain6
from maincode.tools.main import CmdRun, GetMute, ScreenOff, GetTracebackInfo, logger
import sys


class SGAMain7(SGAMain6):
    def __init__(self, userui):
        super().__init__(userui)
        if userui:
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
            para["current_mute"] = GetMute()
            self.NewThread(tasktype, para)
            self.thread.finished.connect(lambda: self.TaskStop(tasktype, para))
            # self.taskthread.finish.connect(self.NormalFinish)
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
            para["current_mute"] = GetMute()
            self.NewThread(tasktype, para)
            self.thread.finished.connect(lambda: self.TaskStop(tasktype, para))
            self.thread.start()
            name = para["ConfigName"]
            self.infoAdd(f"开始执行定时任务：{name}")
            self.module.btpause.setEnabled(True)
            self.module.btpause.show()
            keyboard.add_hotkey(sg.mainconfig.StopKeys, self.ManualStop)
        elif tasktype == "update":
            self.infoHead()
            self.infoAdd("准备开始...")
            self.NewThread(tasktype, para)
            self.thread.finished.connect(lambda: self.TaskStop(tasktype, para))
            self.thread.start()

    def TaskStop(self, tasktype: str, para=None):
        self.window.foreground()
        if sg.info.TaskError:
            self.module.statesigh.SetState(2)
        self.infoEnd()
        keyboard.remove_all_hotkeys()
        keyboard.add_hotkey("ctrl+s", self.SaveConfig)
        self.module.btstart.setEnabled(True)
        self.module.btstart.show()
        self.module.btpause.setEnabled(True)
        self.module.btpause.hide()
        self.timerallow = True
        if tasktype == "timed":
            sleeptime = 46 - localtime()[5]
            self.sleeptime = sleeptime if sleeptime > 0 else 0
        elif tasktype == "update":
            self.overall.btcheckupdate.setEnabled(True)
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
                CmdRun("start "" /d \"resources/main/script\" screen_off.vbs")
                sys.exit(0)
            else:
                self.infoAdd("SGA等待 电脑熄屏")
                ScreenOff()
        elif para["Finished"] == 2:
            if para["SGAClose"]:
                self.infoAdd("SGA关闭 电脑睡眠")
                CmdRun("start "" /d \"resources/main/script\" sleep.vbs")
                sys.exit(0)
            else:
                self.infoAdd("SGA等待 电脑睡眠")
                CmdRun("start "" /d \"resources/main/script\" sleep.vbs")
        else:
            if para["SGAClose"]:
                self.infoAdd("SGA关闭 电脑无操作")
                sys.exit(0)
            else:
                self.infoAdd("SGA等待 电脑无操作")

    def ManualStop(self):
        self.module.btpause.setDisabled(True)
        self.infoAdd("手动终止,等待结束")
        keyboard.remove_all_hotkeys()
        sg.info.StopFlag = True
        self.module.statesigh.SetState(1)
        try:
            self.thread.quit()
            self.thread.wait(),  # 可选：等待线程结束
            self.module.btpause.hide()
            self.taskthread.deleteLater()
            self.thread.deleteLater()
        except:
            ...

    def NormalFinish(self):
        self.module.btpause.setDisabled(True)
        keyboard.remove_all_hotkeys()
        self.thread.quit()
        self.thread.wait(),  # 可选：等待线程结束
        self.module.btpause.hide()
        self.taskthread.deleteLater()
        self.thread.deleteLater()
