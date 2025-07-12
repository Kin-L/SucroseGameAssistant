from maincode.main.main import SGAMain2
from .widget import OverallWidget
from maincode.tools.main import sgatry
from maincode.main.maingroup import sg
from webbrowser import open as weopen
from PyQt5.QtWidgets import QFileDialog
import os


class SGAMain3(SGAMain2):
    def __init__(self, userui):
        super().__init__(userui)
        if self.loadui:
            self.overall = OverallWidget()
            self.mainwidget.sksetting.addWidget(self.overall)
            self.overall.leocrpath.setText(sg.mainconfig.OcrPath)
            self.overall.lekeyboard.setText(sg.mainconfig.StopKeys)
            if sg.mainconfig.ModulesEnable:
                _l = sg.mainconfig.ModulesEnable
            else:
                _l = list(sg.modules.GetInfosT()[0])
                sg.mainconfig.ModulesEnable = _l
            self.overall.boxmodules.addItems(_l)
            self.overall.btmodulesdisable.clicked.connect(self.DisableModules)
            self.overall.btmodulesrefresh.clicked.connect(self.RefreshModules)
            self.overall.ckautoupdate.setChecked(sg.mainconfig.AutoUpdate)

            self.overall.btsupport.clicked.connect(self.mainwidget.support.show)
            self.overall.btgithub.clicked.connect(lambda: weopen("https://github.com/Kin-L/SucroseGameAssistant"))
            self.overall.btgitee.clicked.connect(lambda: weopen("https://gitee.com/huixinghen/SucroseGameAssistant"))
            self.overall.btbilibili.clicked.connect(lambda: weopen("https://space.bilibili.com/406315493"))
            self.overall.btrunhistory.clicked.connect(lambda: os.startfile(f"{os.getcwd()}/personal/logs"))
            self.overall.btupdatehistory.clicked.connect(lambda: os.startfile(f"{os.getcwd()}/update.txt"))

            self.overall.ckautoupdate.clicked.connect(lambda: self.changeAutoUpdate())
            self.overall.leocrpath.editingFinished.connect(lambda: self.changeOcrPath())
            self.overall.lekeyboard.editingFinished.connect(lambda: self.changeStopKeys())
            self.overall.fileselect.clicked.connect(self.SelectOCRPath)

    @sgatry
    def changeAutoUpdate(self):
        sg.mainconfig.AutoUpdate = self.overall.ckautoupdate.isChecked()

    @sgatry
    def changeOcrPath(self):
        sg.mainconfig.OcrPath = self.overall.leocrpath.text()

    @sgatry
    def changeStopKeys(self):
        sg.mainconfig.StopKeys = self.overall.lekeyboard.text()

    @sgatry
    def SelectOCRPath(self):
        _path = QFileDialog.getOpenFileName(self, "选择OCR组件exe文件")
        self.overall.leocrpath.setText(_path[0])
        sg.mainconfig.OcrPath = _path

    @sgatry
    def DisableModules(self):
        sg.mainconfig.ModulesEnable.remove(self.overall.boxmodules.currentText())
        self.overall.boxmodules.removeItem(self.overall.boxmodules.currentIndex())

    @sgatry
    def RefreshModules(self):
        sg.mainconfig.ModulesEnable = list(sg.modules.GetInfosT()[0])
        self.overall.boxmodules.clear()
        self.overall.boxmodules.addItems(sg.mainconfig.ModulesEnable)
