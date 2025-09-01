from .widget import OverallWidget
from maincode.config.maingroup import sg
from webbrowser import open as weopen
from PyQt5.QtWidgets import QFileDialog
import os
from maincode.tools.constant import spr
from maincode.mainwindows.mainwindow import SGAQMainWindow


class SGAOverall:
    def __init__(self, SQMW: SGAQMainWindow):
        self.infoHead = SQMW.infoHead
        self.infoAdd = SQMW.infoAdd
        self.infoEnd = SQMW.infoEnd
        self.widget = OverallWidget(SQMW)
        self.widget.leocrpath.setText(sg.mainconfig.OcrPath)
        self.widget.lekeyboard.setText(sg.mainconfig.StopKeys)
        if sg.mainconfig.ModulesEnable:
            _l = sg.mainconfig.ModulesEnable
        else:
            _l = list(sg.modules.GetInfosT()[0])
            sg.mainconfig.ModulesEnable = _l
        self.widget.boxmodules.addItems(_l)
        self.widget.btmodulesdisable.clicked.connect(self.DisableModules)
        self.widget.btmodulesrefresh.clicked.connect(self.RefreshModules)
        self.widget.ckautoupdate.setChecked(sg.mainconfig.AutoUpdate)

        self.widget.btgithub.clicked.connect(lambda: weopen(spr["GithubURL"]))
        self.widget.btgitee.clicked.connect(lambda: weopen(spr["GiteeURL"]))
        self.widget.btbilibili.clicked.connect(lambda: weopen(spr["BilibiliURL"]))
        self.widget.btrunhistory.clicked.connect(lambda: os.startfile(f"{os.getcwd()}/"+spr["LogsDir"]))
        self.widget.btupdatehistory.clicked.connect(lambda: os.startfile(f"{os.getcwd()}/update.txt"))

        self.widget.ckautoupdate.clicked.connect(lambda: self.changeAutoUpdate())
        self.widget.leocrpath.editingFinished.connect(lambda: self.changeOcrPath())
        self.widget.lekeyboard.editingFinished.connect(lambda: self.changeStopKeys())
        self.widget.fileselect.clicked.connect(self.SelectOCRPath)

    def changeAutoUpdate(self):
        sg.mainconfig.AutoUpdate = self.widget.ckautoupdate.isChecked()

    def changeOcrPath(self):
        sg.mainconfig.OcrPath = self.widget.leocrpath.text()
        sg.info.OcrPath = sg.mainconfig.OcrPath

    def changeStopKeys(self):
        sg.mainconfig.StopKeys = self.widget.lekeyboard.text()

    def SelectOCRPath(self):
        _path = QFileDialog.getOpenFileName(self.widget, "选择OCR组件exe文件")
        self.widget.leocrpath.setText(_path[0])
        sg.mainconfig.OcrPath = _path[0]
        sg.info.OcrPath = sg.mainconfig.OcrPath

    def DisableModules(self):
        sg.mainconfig.ModulesEnable.remove(self.widget.boxmodules.currentText())
        self.widget.boxmodules.removeItem(self.widget.boxmodules.currentIndex())

    def RefreshModules(self):
        sg.mainconfig.ModulesEnable = list(sg.modules.GetInfosT()[0])
        self.widget.boxmodules.clear()
        self.widget.boxmodules.addItems(sg.mainconfig.ModulesEnable)
