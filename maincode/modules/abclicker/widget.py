from os import startfile, getcwd
from typing import Optional
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from maincode.tools.sgaqt.buttons import Button, TransPicButton, Combobox
from maincode.tools.sgaqt.texts import Label, SLineEdit, Line
from maincode.tools.sgaqt.widgets import ModuleStackPage, Widget


class ClickerPage(ModuleStackPage):
    def __init__(self):
        super().__init__()
        self.widget = ClickerWidget(self)
        self.widget.btrule.clicked.connect(lambda: startfile(f"{getcwd()}/resources/clicker/rule.txt"))

    def SetWidget(self, config: dict):
        """输入配置到UI"""
        # 触发配置
        self.widget.line_disable.setText(config["DisableKey"])
        self.widget.choose_trigger.setCurrentText(config["TriggerMode"])
        self.widget.line_trigger.setText(config["TriggerKey"])

        # 连点配置
        self.widget.choose_clicker_mode.setCurrentText(config["ClickerMode"])
        self.widget.line_clicker.setText(config["ClickerKey"])
        self.widget.line_interval.setText(str(config["Interval"]))

        # 脚本配置
        self.widget.choose_sc.setCurrentText(config["ScriptName"])
        self.widget.line_scn.setText(str(config["RunNum"]))

    def CollectConfig(self) -> dict:
        """从UI输出配置"""
        return {
            "DisableKey": self.widget.line_disable.text(),
            "TriggerMode": self.widget.choose_trigger.currentText(),
            "TriggerKey": self.widget.line_trigger.text(),
            "ClickerMode": self.widget.choose_clicker_mode.currentText(),
            "ClickerKey": self.widget.line_clicker.text(),
            "Interval": float(self.widget.line_interval.text() or 0),
            "ScriptName": self.widget.choose_sc.currentText(),
            "RunNum": int(self.widget.line_scn.text() or 0),
        }


class ClickerWidget(Widget):
    def __init__(self, widget):
        super().__init__(widget)
        # Label(self, (10, 12, 200, 18), "设置页面：连点器 运行方式")
        self.btrule = Button(self, (220, 7, 120, 30), "热键设置规则")
        Line(self, (0, 42, 610, 3))

        Label(self, (10, 50, 180, 27), "禁用/启用热键：")
        self.line_disable = SLineEdit(self, (130, 50, 160, 33))

        Label(self, (10, 90, 180, 27), "触发模式：")
        self.choose_trigger = Combobox(self, (130, 90, 100, 30))
        self.choose_trigger.addItems(["长按模式", "短按模式"])

        Label(self, (10, 125, 180, 27), "触发热键：")
        self.line_trigger = SLineEdit(self, (130, 125, 160, 33))

        Label(self, (10, 165, 180, 27), "连点模式：")
        self.choose_clicker_mode = Combobox(self, (130, 165, 100, 30))
        self.choose_clicker_mode.addItems(["按下模式", "连点模式", "脚本模式"])

        Label(self, (10, 200, 180, 27), "连点/按下键：")
        self.line_clicker = SLineEdit(self, (130, 200, 160, 33))

        Label(self, (10, 240, 180, 27), "间隔时间(秒)：")
        self.line_interval = SLineEdit(self, (130, 240, 80, 33))
        self.line_interval.setValidator(QDoubleValidator())

        Label(self, (10, 280, 180, 27), "脚本选择：")
        self.choose_sc = Combobox(self, (130, 280, 160, 30))

        Label(self, (10, 320, 180, 27), "重复次数：")
        self.line_scn = SLineEdit(self, (130, 320, 80, 33))
        self.line_scn.setValidator(QIntValidator())

        # 脚本文件夹按钮
        self.btjf = Button(self, (300, 280, 130, 30), "打开脚本文件夹")
        self.btrefresh = TransPicButton(
            self, (100, 285, 20, 20),
            "assets/main_window/ui/refresh.png", (20, 20)
        )
