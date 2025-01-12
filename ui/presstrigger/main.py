import os
from os import startfile
from ui.element.control import *
from .stack import *
from tools.environment import env


class PressTrigger:
    def __init__(self, stack, main):
        self.main = main
        self.widget_presstrigger = Widget()
        stack.addWidget(self.widget_presstrigger)
        self.button = Picture(main.widget_module, (0, 0, 50, 50),
                              r"assets\main_window\ui\presstrigger-icon.png")
        self.list = None
        self.set = None

    def load_window(self):
        # self.list = PressTriggerList(self.widget_presstrigger, (0, 0, 215, 515))
        self.set = PressTriggerStack(self.widget_presstrigger, (0, 0, 635, 515))
        # self.list.set_presstrigger.clicked.connect(lambda: self.set.stack.setCurrentIndex(0))

        self.set.button_folder.clicked.connect(self.open_folder)
        self.set.button_rule.clicked.connect(self.open_rule)
        self.set.button_refresh.clicked.connect(self.refresh)
        # Line(self.widget_presstrigger, (215, 5, 3, 505), False)

    def load_run(self, run):
        pass

    def get_run(self):
        return {}

    def refresh(self):
        self.main.indicate("", 1)
        _path = env.workdir + "/personal/ptscript"
        if not os.path.exists(_path):
            os.makedirs(_path)
        _list = os.listdir("personal/ptscript")
        _nl = []
        for i in _list:
            _nl += [os.path.splitext(i)[0]]
        self.set.choose_sc.clear()
        self.set.choose_sc.addItems(_nl)
        self.main.indicate("脚本选择列表已刷新", 3)

    def input_config(self, _dir):
        config = {
            "模块": 7,
            "静音": False,
            "关闭软件": False,
            "完成后": 0,
            "SGA关闭": False,
            "disablekey": "",
            "TriggerMode": "长按模式",
            "triggerkey": "",
            "ClickerMode": "连点模式",
            "clickerkey": "",
            "interval": 0,
            "scriptname": "",
            "runnum": 0
        }
        config.update(_dir)
        self.set.independent.check_mute.setChecked(config["静音"])
        self.set.independent.check_kill_game.setChecked(config["关闭软件"])
        self.set.independent.combo_after.setCurrentIndex(config["完成后"])
        self.set.independent.check_kill_sga.setChecked(config["SGA关闭"])

        self.set.line_disable.setText(config["disablekey"])

        self.set.choose_trigger.setCurrentText(config["TriggerMode"])
        self.set.line_trigger.setText(config["triggerkey"])

        self.set.choose_clicker_mode.setCurrentText(config["ClickerMode"])
        self.set.line_clicker.setText(config["clickerkey"])
        self.set.line_interval.setText(str(config["interval"]))

        self.set.choose_sc.setCurrentText(config["scriptname"])
        self.set.line_scn.setText(str(config["runnum"]))

    def output_config(self):
        config = dict()
        config["模块"] = 7
        config["静音"] = self.set.independent.check_mute.isChecked()
        config["关闭软件"] = self.set.independent.check_kill_game.isChecked()
        config["完成后"] = self.set.independent.combo_after.currentIndex()
        config["SGA关闭"] = self.set.independent.check_kill_sga.isChecked()

        config["disablekey"] = self.set.line_disable.text()
        config["TriggerMode"] = self.set.choose_trigger.currentText()

        config["triggerkey"] = self.set.line_trigger.text()
        config["ClickerMode"] = self.set.choose_clicker_mode.currentText()
        config["clickerkey"] = self.set.line_clicker.text()
        if self.set.line_interval.text():
            config["interval"] = int(self.set.line_interval.text())
        else:
            config["interval"] = 0
        config["scriptname"] = self.set.choose_sc.currentText()
        if self.set.line_scn.text():
            config["runnum"] = int(self.set.line_scn.text())
        else:
            config["runnum"] = 0
        return config

    def open_folder(self):
        _path = env.workdir + "/personal/ptscript"
        if not os.path.exists(_path):
            os.makedirs(_path)
        self.main.indicate("", 1)
        startfile(_path)
        self.main.indicate("打开文件夹: 脚本方案", 3)

    def open_rule(self):
        _path = r"assets\presstrigger\rule.txt"
        if os.path.exists(_path):
            self.main.indicate("", 1)
            startfile(_path)
            self.main.indicate("打开文件: 热键规则", 3)
        else:
            self.main.indicate("", 1)
            self.main.indicate("文件丢失：热键规则", 3)
