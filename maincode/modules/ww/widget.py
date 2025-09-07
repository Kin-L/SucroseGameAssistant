from maincode.main.info import info
from maincode.tools.controls import (Combobox, SetStackPage, Check,
                                     ModuleStackPage, Widget, Line,
                                     Picture, TaskPanel, Label, tips,Button,
                                     SLineEdit, PicButton, SetButton, TipsButton)
from typing import Optional
from os import path, startfile, getcwd
from PyQt5.QtWidgets import QFileDialog
_path = "resources/main/button/fold.png"
from webbrowser import open as weopen


class wwPage(ModuleStackPage):
    def __init__(self):
        super().__init__()
        self.page00: Optional[wwPage00Set] = None
        self.pbset00 = SetButton(self, (180, 10, 25, 25), (25, 25))

    def LoadWidget(self):
        self.page00 = wwPage00Set()
        self.sksetting.addWidget(self.page00)
        Line(self, (215, 5, 3, 530), False)
        self.page00.btselect.clicked.connect(self.SelectPath)
        self.page00.button_ww_ok.clicked.connect(self.open_ww_ok)

    def SelectPath(self):
        self.page00.path.setText(QFileDialog.getOpenFileName(self, "选择启动路径")[0])

    def open_ww_ok(self):
        weopen("https://github.com/ok-oldking/ok-wuthering-waves")

    def SetWidget(self, config: dict):
        self.page00.bgipath.setText(config["bgipath"])
        self.page00.timeout.setText(config["timeout"])
        self.page00.taskpanel.ckkillsga.setChecked(config["SGAClose"])
        self.page00.taskpanel.ckmute.setChecked(config["Mute"])
        self.page00.taskpanel.ckkillprog.setChecked(config["SoftClose"])
        self.page00.taskpanel.cbafter.setCurrentIndex(config["Finished"])
        
    def CollectConfig(self) -> dict:
        _dict = dict()
        _dict["path"] = self.page00.path.text()
        _dict["timeout"] = self.page00.timeout.text()
        _dict["Mute"] = self.page00.taskpanel.ckmute.isChecked()
        _dict["SoftClose"] = self.page00.taskpanel.ckkillprog.isChecked()
        _dict["Finished"] = self.page00.taskpanel.cbafter.currentIndex()
        _dict["SGAClose"] = self.page00.taskpanel.ckkillsga.isChecked()
        return _dict


class wwPage00Set(SetStackPage):
    def __init__(self):
        super().__init__("设置页面：运行方式")
        self.lbgenshinoverall = Label(self, (0, 55, 180, 27), "全局设置：")

        self.lbpath = Label(self, (0, 85, 180, 27), "ww-ok启动路径:")
        self.path = SLineEdit(self, (0, 115, 355, 33))
        tips(self.path, '请填写或选择ww-ok.exe的路径')
        self.path.setText("D:\ww-ok\ww-ok.exe")  # 设置默认路径

        self.btselect = PicButton(self, (360, 115, 35, 33), _path, (30, 30))
        self.lbtimeout = Label(self, (0, 155, 180, 27), "超时关闭时间（分钟）：")
        self.timeout = SLineEdit(self, (190, 155, 40, 10))
        self.timeout.setText("0")  # 设置默认超时时间

        self.tips = Label(self, (0, 200, 220, 50), "提示：\n使用该模块前请设置好ww-ok")
        self.button_ww_ok = Button(self, (100, 260, 120, 27), "ww-ok下载")
        Line(self, (0, 292, 395, 3))
        self.taskpanel = TaskPanel(self, 295)
        

