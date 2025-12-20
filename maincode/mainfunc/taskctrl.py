import sys

import keyboard
from time import localtime
from maincode.config.configctrl import scc
from maincode.tools.core.constant import spr
from maincode.tools.system.other import CmdRun, GetMute, ScreenOff
from maincode.tools.system.notification import GetTracebackInfo
from maincode.tools.core.logger import logger
from PyQt5.QtWidgets import QApplication
from maincode.tools.system.process import GetPid, killprocess
from maincode.mainthread import SGAMainThread
from PyQt5.QtCore import QThread


def TaskStart(self, tasktype: str, para: dict = None):
    if para is None:
        para = dict()
    try:
        while v := GetPid("PaddleOCR-json.exe"):
            killprocess(v)
        scc.info.TaskError = False
        scc.info.StopFlag = False
        self.timerallow = False
        scc.info.OcrPath = scc.mc.OcrPath
        if "-hideui" not in sys.argv:
            self.module.widget.statesigh.SetState(0)
            self.module.widget.btstart.setDisabled(True)
            self.module.widget.btstart.hide()
            self.mainwidget.infoClear()
        if tasktype == "current":
            self.infoHead()
            self.SaveConfig()
            para.update(dict(scc.mc.CurrentConfig))
            para["OtherConfig"] = scc.mc.OtherConfig
            para["current_mute"] = GetMute() if para.get("Mute", False) else None
            self.NewThread(tasktype, para)
            self.infoAdd("开始执行实时任务")
            if "-hideui" not in sys.argv:
                self.module.widget.btpause.setEnabled(True)
                self.module.widget.btpause.show()
            keyboard.add_hotkey(scc.mc.StopKeys, self.ManualStop)
        elif tasktype == "timed":
            self.infoHead()
            self.infoAdd("准备开始...")
            para["OtherConfig"] = scc.mc.OtherConfig
            para["current_mute"] = GetMute() if para.get("Mute", False) else None
            self.NewThread(tasktype, para)
            name = para["ConfigName"]
            self.infoAdd(f"开始执行定时任务：{name}")
            if "-hideui" not in sys.argv:
                self.module.widget.btpause.setEnabled(True)
                self.module.widget.btpause.show()
            keyboard.add_hotkey(scc.mc.StopKeys, self.ManualStop)
        elif tasktype == "update":
            self.infoHead()
            self.infoAdd("准备开始...")
            self.NewThread(tasktype, para)
        elif tasktype == "subconfig":
            _ck = para.get("ck", None)
            _num = para.get("num", None)
            if _num is None:
                if _ck.isdigit() and (item := scc.sc.FindItem(_ck)):
                    _num = item[-1]
                else:
                    self.infoAdd(f"输入的子设置无效：'ck'：{_ck}")
                    return
            _config = scc.ReadSubFile(_num)
            self.infoHead()
            self.SaveConfig()
            para.update(dict(_config))
            para["OtherConfig"] = scc.mc.OtherConfig
            para["current_mute"] = GetMute() if para.get("Mute", False) else None
            self.NewThread(tasktype, para)
            name = para["ConfigName"]
            self.infoAdd(f"开始执行指定任务：{name}")
            if "-hideui" not in sys.argv:
                self.module.widget.btpause.setEnabled(True)
                self.module.widget.btpause.show()
            keyboard.add_hotkey(scc.mc.StopKeys, self.ManualStop)

    except Exception as e:
        _str = GetTracebackInfo(e) + "准备开始流程异常"
        logger.error(_str)
        self.infoAdd(f"准备开始流程异常")


def TaskStop(self, tasktype: str, para=None):
    try:
        if scc.info.TaskError and ("-hideui" not in sys.argv):
            self.window.foreground()
            self.module.widget.statesigh.SetState(2)
        self.infoEnd()
        self.timerallow = True
        if "-hideui" not in sys.argv:
            self.module.widget.btstart.setEnabled(True)
            self.module.widget.btstart.show()
            self.module.widget.btpause.setEnabled(True)
            self.module.widget.btpause.hide()
        keyboard.remove_hotkey(scc.mc.StopKeys)
        if tasktype == "timed":
            sleeptime = 61 - localtime()[5]
            self.sleeptime = sleeptime if sleeptime > 0 else 0
        elif tasktype == "update":
            if "-hideui" not in sys.argv:
                self.overall.widget.btcheckupdate.setEnabled(True)
            return
        if para.get("Mute", False) and (GetMute() != para["current_mute"]):
            keyboard.send('volume mute')
        # 结束
        if scc.info.StopFlag:
            para["Finished"] = 0
            para["SGAClose"] = False
        scc.info.StopFlag = None
        self.handle_finished_action(para)
    except Exception as e:
        _str = GetTracebackInfo(e) + "终止流程异常"
        logger.error(_str)
        self.infoAdd(f"终止流程异常")


def handle_finished_action(self, para):
    """处理任务完成后的操作"""
    action_map = {
        1: ("SGA关闭 电脑熄屏", "SGA等待 电脑熄屏", "screen_off.vbs"),
        2: ("SGA关闭 电脑睡眠", "SGA等待 电脑睡眠", "sleep.vbs"),
    }
    finished = para.get("Finished", 0)
    close = para.get("SGAClose", False)
    if finished in action_map:
        close_msg, wait_msg, script = action_map[finished]
        if close:
            self.infoAdd(close_msg)
            self.infoEnd()
            CmdRun(f"start \"\" /d \"{spr.SGAScriptDir}\" {script}")
            app = QApplication.instance()
            if app:
                app.quit()
        else:
            self.infoAdd(wait_msg)
            self.infoEnd()
            if finished == 1:
                ScreenOff()
            else:
                CmdRun(f"start \"\" /d \"{spr.SGAScriptDir}\" {script}")
    else:
        if close:
            self.infoAdd("SGA关闭 电脑无操作")
            self.infoEnd()
            app = QApplication.instance()
            if app:
                app.quit()
        else:
            self.infoAdd("SGA等待 电脑无操作")
            self.infoEnd()


def ManualStop(self):
    try:
        if not self.timerallow:

            self.infoAdd("手动终止,等待结束...")
            self.timerallow = True
            scc.info.StopFlag = True
            if "-hideui" not in sys.argv:
                self.module.widget.btpause.setDisabled(True)
                self.module.widget.statesigh.SetState(1)
                self.module.widget.btpause.hide()
            try:
                if hasattr(self, 'threadpool'):
                    self.threadpool.quit()
                    self.threadpool.wait()
                    self.threadpool.deleteLater()
            except Exception as e:
                logger.error(f"手动终止线程异常: {GetTracebackInfo(e)}")
    except Exception as e:
        _str = GetTracebackInfo(e) + "手动终止流程异常"
        logger.error(_str)
        self.infoAdd(f"手动终止流程异常")


def NewThread(self, tasktype, para):
    self.threadpool = QThread()
    self.worker = SGAMainThread(tasktype, para)
    # 将工作对象移动到线程中
    self.worker.moveToThread(self.threadpool)
    self.worker.infoHead.connect(self.infoHead)
    self.worker.infoAdd.connect(self.infoAdd)
    self.worker.infoEnd.connect(self.infoEnd)
    self.threadpool.started.connect(self.worker.run)
    self.worker.finished.connect(self.threadpool.quit)
    self.worker.finished.connect(self.worker.deleteLater)
    self.threadpool.finished.connect(lambda: self.TaskStop(tasktype, para))
    self.threadpool.finished.connect(self.threadpool.deleteLater)
    self.threadpool.start()
