from PyQt5.QtGui import QIntValidator
from maincode.tools.sgaqt.buttons import Button, TransPicButton, Combobox
from maincode.tools.sgaqt.texts import Label, SLineEdit, Line
from maincode.tools.sgaqt.widgets import ModuleStackPage


class ClickerPage(ModuleStackPage):
    def __init__(self):
        super().__init__()

    def LoadWidget(self):
        self._loadwidget()

    def _loadwidget(self):
        """初始化UI控件"""
        # 标题与分割线
        Label(self.page, (10, 12, 200, 18), "设置页面：连点器 运行方式")
        self.btrule = Button(self.page, (220, 7, 120, 30), "热键设置规则")
        Line(self.page, (0, 42, 610, 3))

        Label(self.page, (10, 50, 180, 27), "禁用/启用热键：")
        self.line_disable = SLineEdit(self.page, (130, 50, 160, 33))

        Label(self.page, (10, 90, 180, 27), "触发模式：")
        self.choose_trigger = Combobox(self.page, (130, 90, 100, 30))
        self.choose_trigger.addItems(["长按模式", "短按模式"])

        Label(self.page, (10, 125, 180, 27), "触发热键：")
        self.line_trigger = SLineEdit(self.page, (130, 125, 160, 33))

        Label(self.page, (10, 165, 180, 27), "连点模式：")
        self.choose_clicker_mode = Combobox(self.page, (130, 165, 100, 30))
        self.choose_clicker_mode.addItems(["按下模式", "连点模式", "脚本模式"])
        self.choose_clicker_mode.currentIndexChanged.connect(self._on_clicker_mode_changed)

        Label(self.page, (10, 200, 180, 27), "连点/按下键：")
        self.line_clicker = SLineEdit(self.page, (130, 200, 160, 33))

        Label(self.page, (10, 240, 180, 27), "间隔时间(ms)：")
        self.line_interval = SLineEdit(self.page, (130, 240, 80, 33))
        self.line_interval.setValidator(QIntValidator())

        Label(self.page, (10, 280, 180, 27), "脚本选择：")
        self.choose_sc = Combobox(self.page, (130, 280, 160, 30))

        Label(self.page, (10, 320, 180, 27), "重复次数：")
        self.line_scn = SLineEdit(self.page, (130, 320, 80, 33))
        self.line_scn.setValidator(QIntValidator())

        # 脚本文件夹按钮
        self.btjf = Button(self.page, (300, 280, 130, 30), "打开脚本文件夹")
        self.btrefresh = TransPicButton(
            self.page, (100, 285, 20, 20),
            "assets/main_window/ui/refresh.png", (20, 20)
        )

    def SetWidget(self, config: dict):
        """输入配置到UI"""
        # 触发配置
        self.line_disable.setText(config["DisableKey"])
        self.choose_trigger.setCurrentText(config["TriggerMode"])
        self.line_trigger.setText(config["TriggerKey"])

        # 连点配置
        self.choose_clicker_mode.setCurrentText(config["ClickerMode"])
        self.line_clicker.setText(config["ClickerKey"])
        self.line_interval.setText(config["Interval"])

        # 脚本配置
        self.choose_sc.setCurrentText(config["ScriptName"])
        self.line_scn.setText(config["RunNum"])

    def CollectConfig(self) -> dict:
        """从UI输出配置"""
        return {
            "DisableKey": self.line_disable.text(),
            "TriggerMode": self.choose_trigger.currentText(),
            "TriggerKey": self.line_trigger.text(),
            "ClickerMode": self.choose_clicker_mode.currentText(),
            "ClickerKey": self.line_clicker.text(),
            "Interval": int(self.line_interval.text() or 0),
            "ScriptName": self.choose_sc.currentText(),
            "RunNum": int(self.line_scn.text() or 0),
        }
    