from .widget import OverallWidget
from maincode.config.configctrl import scc
from webbrowser import open as weopen
from PyQt5.QtWidgets import QFileDialog
import os
from maincode.tools.core.constant import spr
from maincode.mainwindows.mainwindow import SGAQMainWindow


class SGAOverall:
    def __init__(self, SQMW: SGAQMainWindow):
        self.infoHead = SQMW.infoHead
        self.infoAdd = SQMW.infoAdd
        self.infoEnd = SQMW.infoEnd
        self.widget = OverallWidget(SQMW)
        self._setup_ui()
        self._bind_signals()

    def _setup_ui(self):
        self.widget.leocrpath.setText(scc.mc.OcrPath)
        self.widget.lekeyboard.setText(scc.mc.StopKeys)
        self.widget.ckautoupdate.setChecked(scc.mc.AutoUpdate)

        if scc.mc.ModulesEnable:
            enabled_modules = scc.mc.ModulesEnable
        else:
            enabled_modules = list(scc.modules.GetInfosT()[0])
            scc.mc.ModulesEnable = enabled_modules
        self.widget.boxmodules.addItems(enabled_modules)

    def _bind_signals(self):
        self.widget.btmodulesdisable.clicked.connect(self.DisableModules)
        self.widget.btmodulesrefresh.clicked.connect(self.RefreshModules)

        self.widget.btgithub.clicked.connect(lambda: weopen(spr["GithubURL"]))
        self.widget.btgitee.clicked.connect(lambda: weopen(spr["GiteeURL"]))
        self.widget.btbilibili.clicked.connect(lambda: weopen(spr["BilibiliURL"]))

        logs_dir = os.path.join(os.getcwd(), spr["LogsDir"])
        self.widget.btrunhistory.clicked.connect(lambda: os.startfile(logs_dir))
        update_file = os.path.join(os.getcwd(), "update.txt")
        self.widget.btupdatehistory.clicked.connect(lambda: os.startfile(update_file))

        self.widget.ckautoupdate.clicked.connect(self.changeAutoUpdate)
        self.widget.leocrpath.editingFinished.connect(self.changeOcrPath)
        self.widget.lekeyboard.editingFinished.connect(self.changeStopKeys)
        self.widget.fileselect.clicked.connect(self.SelectOCRPath)

    def changeAutoUpdate(self):
        scc.mc.AutoUpdate = self.widget.ckautoupdate.isChecked()

    @staticmethod
    def _update_ocr_path(path: str):
        scc.mc.OcrPath = path
        scc.info.OcrPath = path

    def changeOcrPath(self):
        self._update_ocr_path(self.widget.leocrpath.text())

    def changeStopKeys(self):
        scc.mc.StopKeys = self.widget.lekeyboard.text()

    def SelectOCRPath(self):
        _path, _ = QFileDialog.getOpenFileName(self.widget, "选择OCR组件exe文件")
        if _path and os.path.isfile(_path):  # 增加路径有效性校验
            self.widget.leocrpath.setText(_path)
            self._update_ocr_path(_path)

    def DisableModules(self):
        current_text = self.widget.boxmodules.currentText()
        if current_text in scc.mc.ModulesEnable:
            scc.mc.ModulesEnable.remove(current_text)
            self.widget.boxmodules.removeItem(self.widget.boxmodules.currentIndex())

    def RefreshModules(self):
        scc.mc.ModulesEnable = list(scc.modules.GetInfosT()[0])
        self.widget.boxmodules.clear()
        self.widget.boxmodules.addItems(scc.mc.ModulesEnable)
