from maincode.config.info import info
from maincode.tools.sgaqt.texts import Label, Picture, SLineEdit, Line, tips, TipsButton
from maincode.tools.sgaqt.buttons import (PicButton, Button,
                                          SetButton, Swicher)
from maincode.tools.sgaqt.widgets import Widget, SetStackPage, ModuleStackPage, TaskPanel

from typing import Optional
from os import path, startfile, getcwd
from PyQt5.QtWidgets import QFileDialog
_path = "resources/main/button/fold.png"
from webbrowser import open as weopen


class GenshinPage(ModuleStackPage):
    def __init__(self):
        super().__init__()
        self.page00: Optional[GenshinPage00Set] = None
        self.pbset00 = SetButton(self, (180, 10, 25, 25), (25, 25))

    def LoadWidget(self):
        self.page00 = GenshinPage00Set()
        self.sksetting.addWidget(self.page00)
        Line(self, (215, 5, 3, 530), False)
        self.page00.btselect.clicked.connect(self.SelectPath)
        self.page00.button_BGI.clicked.connect(self.open_BGI)

    def SelectPath(self):
        self.page00.bgipath.setText(QFileDialog.getOpenFileName(self, "选择启动路径")[0])

    def open_BGI(self):
        weopen("https://bgi.huiyadan.com/")

    def SetWidget(self, config: dict):
        self.page00.bgipath.setText(config["bgipath"])
        self.page00.timeout.setText(config["timeout"])
        self.page00.taskpanel.ckkillsga.setChecked(config["SGAClose"])
        self.page00.taskpanel.ckmute.setChecked(config["Mute"])
        self.page00.taskpanel.ckkillprog.setChecked(config["SoftClose"])
        self.page00.taskpanel.cbafter.setCurrentIndex(config["Finished"])
        
    def CollectConfig(self) -> dict:
        _dict = dict()
        _dict["bgipath"] = self.page00.bgipath.text()
        _dict["timeout"] = self.page00.timeout.text()
        _dict["Mute"] = self.page00.taskpanel.ckmute.isChecked()
        _dict["SoftClose"] = self.page00.taskpanel.ckkillprog.isChecked()
        _dict["Finished"] = self.page00.taskpanel.cbafter.currentIndex()
        _dict["SGAClose"] = self.page00.taskpanel.ckkillsga.isChecked()
        return _dict


class GenshinPage00Set(SetStackPage):
    def __init__(self):
        super().__init__("设置页面：运行方式")
        self.lbgenshinoverall = Label(self, (0, 55, 180, 27), "全局设置：")

        self.lbpath = Label(self, (0, 85, 180, 27), "BGI启动路径:")
        self.bgipath = SLineEdit(self, (0, 115, 355, 33))
        tips(self.bgipath, '请填写或选择BetterGI.exe的路径')
        self.bgipath.setText("D:\BetterGI\BetterGI.exe")  # 设置默认路径

        self.btselect = PicButton(self, (360, 115, 35, 33), _path, (30, 30))
        self.lbtimeout = Label(self, (0, 155, 180, 27), "超时关闭时间（分钟）：")
        self.timeout = SLineEdit(self, (190, 155, 40, 10))
        self.timeout.setText("0")  # 设置默认超时时间

        self.tips = Label(self, (0, 200, 220, 50), "提示：\n使用该模块前请设置好BGI")
        self.button_BGI = Button(self, (10, 260, 100, 27), "BGI下载")
        Line(self, (0, 292, 395, 3))
        self.taskpanel = TaskPanel(self, 295)
        

