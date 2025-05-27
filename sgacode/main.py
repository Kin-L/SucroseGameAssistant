from time import sleep, strftime, localtime
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from sgacode.tools.main import (logger, GetHwnd,
                                CheckAdmin, SendMessageBox,
                                GetTracebackInfo, foreground)
from sgacode.ui.main import SGAMainWidget, SGAQMainWindow
from sys import argv
import keyboard
from typing import List
from sgacode.moduleclass import ModuleClass
from sgacode.tools.sgagroup import sg
import os


class MainWindow(SGAQMainWindow):
    def __init__(self, useui: bool):
        super().__init__()

        # 主窗口初始化，加载封面等待窗口
        if useui:
            self.SMW = SGAMainWidget(self)
            self.setCentralWidget(self.SMW)
            self.InfoBox = self.SMW.infobox

        # 识别模组
        self.Instances: List[ModuleClass] = []  # 存储所有实例化的模组类
        self.ReadModules()

        # 配置信息加载
        sg.LoadConfig([i.Config for i in self.Instances])
        if useui:
            self.SMW.InitSetWidgets([i.Widget for i in self.Instances])
            if sg.mainconfig.configmsg:
                self.infoAdd(sg.mainconfig.configmsg, False)
            else:
                self.infoAdd("成功加载已保存配置", False)
        # 主线程加载
        from sgacode.thread import SGAMainThread
        self.SMT = SGAMainThread(self.thread)
        if useui:
            self.LoadMainConnect()  # 加载状态链接
        # self.thread.start()

    def ReadModules(self):
        from sgacode.ui.module.mix import MixClass
        self.Instances += [MixClass()]

    def EnterMainWindows(self):
        self.infoEnd()
        self.loading.hide()
        self.loading.lower()

    def LoadMainConnect(self):
        self.SMT.infoAdd.connect(self.infoAdd)
        self.SMT.infoHead.connect(self.infoHead)
        self.SMT.infoEnd.connect(self.infoEnd)
        self.SMW.btsetting.toggled.connect(self.SMW.changeob)
        from webbrowser import open as weopen
        self.SMW.overall.btgithub.clicked.connect(lambda: weopen("https://github.com/Kin-L/SucroseGameAssistant"))
        self.SMW.overall.btgitee.clicked.connect(lambda: weopen("https://gitee.com/huixinghen/SucroseGameAssistant"))
        self.SMW.overall.btbilibili.clicked.connect(lambda: weopen("https://space.bilibili.com/406315493"))
        self.SMW.overall.btrunhistory.clicked.connect(lambda: os.startfile("personal/logs"))
        self.SMW.overall.btupdatehistory.clicked.connect(lambda: os.startfile("update_history.txt"))
        self.SMW.overall.fileselect.clicked.connect(self.SMW.overall.SelectOCRPath)
        from pathlib import Path as libPath
        self.SMW.bthistory.clicked.connect(
            lambda: os.startfile(
                max([f for f in libPath("personal/logs").iterdir() if f.is_file()],
                    key=lambda f: f.stat().st_ctime)))
        self.SMW.module.btconfiglock.clicked.connect(lambda: self.SMW.setlock(False))
        self.SMW.module.btconfigunlock.clicked.connect(lambda: self.SMW.setlock(True))
        self.SMW.module.boxmodule.currentIndexChanged.connect(self.SMW.module.skmodule.setCurrentIndex)
        self.SMW.module.btconfigadd.clicked.connect(self.SMW.module.configadd)
        self.SMW.module.btconfigdelete.clicked.connect(self.SMW.module.configdelete)
        self.SMW.module.ecbconfig.currentTextChanged.connect(self.SMW.module.configrename)
        self.SMW.module.ecbconfig.currentIndexChanged.connect(self.SMW.configchange)
        keyboard.add_hotkey("ctrl+s", self.SaveConfig)

    def infoAdd(self, msg: str = "", addtime=True):
        if addtime:
            addstr = strftime("%H:%M:%S ", localtime())
        else:
            addstr = "  "
        msg.strip("\n")
        if "\n" in msg:
            if addtime:
                addstr += ("\n" + msg).replace("\n", "\n  ")
            else:
                addstr = ("\n" + msg).replace("\n", "\n  ").strip("\n")
        else:
            addstr += msg
        self.InfoBox.append(addstr)
        self.InfoBox.ensureCursorVisible()

    def infoHead(self):
        today = strftime("%Y-%m-%d", localtime())
        if today != logger.date:
            logger.new_handler(today)
        now_time = strftime("%Y-%m-%d", localtime())
        self.InfoBox.append(now_time)

    def infoEnd(self):
        self.InfoBox.append("------------------------------")
        self.InfoBox.ensureCursorVisible()

    def infoClear(self):
        self.InfoBox.clear()

    def TaskStart(self):
        sg.SetTriggerFlag(True)
        self.infoClear()
        self.infoHead()
        self.infoAdd("等待开始...")
        while 1:
            if sg.GetRunning():
                break
            sleep(0.5)
        self.infoAdd("开始执行实时任务")
        keyboard.add_hotkey(sg.mainconfig['StopKeys'], self.TaskStop)

    def TaskStop(self):
        keyboard.remove_all_hotkeys()
        sg.SetTriggerFlag(False)
        self.infoAdd("尝试手动终止")
        self.infoAdd("等待结束...")
        while 1:
            if sg.GetRunning():
                sleep(0.5)
            else:
                break
        self.infoAdd("手动终止任务")

    def SaveConfig(self):
        self.SMW.SaveConfig()
        sg.mainconfig.savemain()
        sg.mainconfig.savebackup()

    def closeEvent(self, event):
        self.SaveConfig()
        super().closeEvent(event)


def SGA(useui: bool = True):
    try:
        CheckAdmin()
        hwnd = GetHwnd(True, "Qt5152QWindowIcon", "砂糖代理")
        if hwnd:
            foreground(hwnd)
            # exit(0)
        else:
            from sgacode.tools.sgagroup import sg
            print("")
            logger.info("================SGA开始启动================")
            # 唤醒屏幕
            keyboard.send("numlock")
            sleep(0.01)
            keyboard.send("numlock")
            sg.logger_environment_info()
            # SGA窗口初始化
            QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
            QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
            QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
            application = QApplication(argv)
            sqmw = MainWindow(useui)
            if useui:
                sqmw.EnterMainWindows()
            application.exec_()
            logger.info("==================SGA关闭=================\n\n")
    except Exception as e:
        _str = GetTracebackInfo(e) + "\nSGA加载失败"
        logger.critical(_str)
        SendMessageBox(_str)
        # exit(1)


if __name__ == "__main__":
    pass
