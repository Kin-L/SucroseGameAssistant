from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from sys import argv
from typing import Optional
from sgacode.ui.control import (Line, Stack, Widget, ModuleStackPage,
                                PicButton, InfoBox, OverallButton,
                                palette)
from sgacode.ui.overall.main import OverallWindow
from sgacode.ui.module.main import ModuleWindow
from typing import List
from sgacode.tools.sgagroup import sg
import json


class SGAMainWidget(Widget):
    def __init__(self, _widget: QMainWindow):
        super().__init__(_widget)
        self.sksetting = Stack(self, (5, 0, 625, 575))
        Line(self, (5, 38, 625, 3))
        # 全局/模块 设置按钮
        self.btsetting = OverallButton(self)
        self.obstate = False

        # 历史信息按钮
        historypath = r"resources/main/button/history.png"
        savepath = r"resources/main/button/save.png"
        sizetp = (25, 25)
        self.bthistory = PicButton(self, (555, 0, 35, 35), historypath, sizetp)
        self.btconfigsave = PicButton(self, (515, 0, 35, 35), savepath, sizetp)
        # 指示信息窗口
        self.infobox = InfoBox(self)
        self.overall: Optional[OverallWindow] = None
        self.module: Optional[ModuleWindow] = None
        self.modules: Optional[List[ModuleStackPage]] = None
        self.moduleloadlist: List[bool] = []

    def InitSetWidgets(self, widgets: List[ModuleStackPage]):
        self.overall = OverallWindow()  # 加载主设置
        self.sksetting.addWidget(self.overall)
        self.module = ModuleWindow()
        self.sksetting.addWidget(self.module)
        self.sksetting.setCurrentIndex(1)
        self.modules = widgets
        self.moduleloadlist = [False] * len(widgets)
        for i in widgets:
            self.module.skmodule.addWidget(i)
        # 加载设置
        mc = sg.mainconfig
        self.overall.leocrpath.setText(mc['OcrPath'])
        self.overall.lekeyboard.setText(mc['StopKeys'])
        self.overall.ckautoupdate.setChecked(mc["AutoUpdate"])
        self.setlock(mc['ConfigLock'])

        configkey = mc['ConfigKey']
        filekeys = sg.subconfig.GetFileListT()[1]
        seq = filekeys.index(configkey) if configkey in filekeys else 0
        self.module.ecbconfig.setCurrentIndex(seq)
        subconfig = mc['CurrentConfig']
        self.LoadModuleSet(subconfig)

    def LoadModuleSet(self, config: dict):
        _, _, modulekeys, iconpaths = sg.subconfig.GetSignListT()
        seq = list(modulekeys).index(config['ModuleKey'])
        self.module.boxmodule.setCurrentIndex(seq)
        self.module.skmodule.setCurrentIndex(seq)
        self.module.picicon.setIcon(iconpaths[seq])
        if not self.moduleloadlist[seq]:
            self.modules[seq].LoadWindow()
            self.moduleloadlist[seq] = True
        self.modules[seq].SetWindow(config)

    def changeob(self):
        if self.obstate:
            self.sksetting.setCurrentIndex(1)
            self.obstate = False
        else:
            self.sksetting.setCurrentIndex(0)
            self.obstate = True

    def setlock(self, lock: bool):
        if lock:
            self.module.btconfiglock.show()
            self.module.btconfigunlock.hide()
            self.module.btconfigdelete.hide()
            self.module.btconfigadd.show()
            self.configchange()
        else:
            self.module.btconfiglock.hide()
            self.module.btconfigunlock.show()
            self.module.btconfigdelete.show()
            self.module.btconfigadd.hide()
        sg.mainconfig['ConfigLock'] = lock

    def configchange(self):
        num = self.module.boxmodule.currentIndex()
        flt = sg.subconfig.GetFileListT()
        ck = list(flt[0])[num]
        sg.mainconfig['ConfigKey'] = ck
        if sg.mainconfig['ConfigLock']:
            name = flt[2][num]
            with open(f"personal/config/{ck}{name}.json", 'r', encoding='utf-8') as c:
                _config = json.load(c)
            if sg.subconfig.CheckConfig(_config):
                self.LoadModuleSet(_config)

    def SaveConfig(self):
        sg.mainconfig['TimerConfig'] = self.overall.timer.wdtime.CollectConfig()
        num = self.module.boxmodule.currentIndex()
        mk = sg.subconfig.FindSignList(num)[2]
        subconfig = self.modules[num].CollectConfig()
        subconfig['ModuleKey'] = mk
        subconfig['ConfigKey'] = ""
        subconfig['ConfigName'] = "默认配置"
        sg.mainconfig['CurrentConfig'] = subconfig


class SGAQMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("mainwindow")
        # 窗口大小
        self.resize(910, 580)
        # 窗口名
        self.setWindowTitle("砂糖代理")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        # 窗口锁定大小
        self.setFixedSize(self.width(), self.height())
        # 窗口图标
        self.setWindowIcon(QIcon('resources/main/SGA/title.png'))
        self.setPalette(palette)
        self.thread = QThread()   # 线程初始化
        self.loading = LoadWidget(self)
        self.show()
        # 窗口显现
        from sgacode.tools.main import GetHwnd
        sg.info.hwnd = GetHwnd(True, "Qt5152QWindowIcon", "砂糖代理")
        if len(argv) <= 1:
            sg.foreground()
        elif argv[1] != "True":
            sg.foreground()

    def closeEvent(self, event):
        if self.thread.isRunning():
            self.thread.quit()
            self.thread.wait()
        super().closeEvent(event)


class LoadWidget(QWidget):
    def __init__(self, _widget: QMainWindow):
        super().__init__(_widget)
        self.setGeometry(0, 0, 910, 580)
        self.setPalette(palette)

        backpath = r'resources/main/SGA/loadback.png'
        self.loadbacklab = QLabel("", self)
        self.loadbacklab.setPixmap(QPixmap(backpath))
        self.loadbacklab.setGeometry(0, 0, 910, 580)
        self.loadbacklab.setScaledContents(True)

        loadgifpath = r'resources/main/SGA/loading.gif'
        self.loadgiflab = QLabel("", self)
        self.loadgifmov = QMovie(loadgifpath)
        self.loadgiflab.setMovie(self.loadgifmov)
        self.loadgiflab.setGeometry(430, 440, 50, 50)
        self.loadgiflab.setScaledContents(True)
        self.loadgifmov.start()
        self.raise_()
