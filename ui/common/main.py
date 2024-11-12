import os
from os import startfile
from .list import CommonList
from .stack import CommonStack
from ui.element.control import *
from tools.environment import env


# 原神模组设置窗口
class Common:
    def __init__(self, stack, main):
        self.main = main
        self.widget_common = Widget()
        stack.addWidget(self.widget_common)
        self.button = Picture(main.widget_module, (0, 0, 50, 50),
                              r"assets\main_window\ui\common-icon.png")
        self.list = None
        self.set = None

    def load_window(self):
        self.list = CommonList(self.widget_common, (0, 0, 215, 515))
        self.set = CommonStack(self.widget_common, (225, 0, 410, 515))
        self.list.set_common.clicked.connect(lambda: self.set.stack.setCurrentIndex(0))
        self.list.set_start.clicked.connect(lambda: self.set.stack.setCurrentIndex(1))
        self.list.set_exit.clicked.connect(lambda: self.set.stack.setCurrentIndex(2))

        self.set.button_folder.clicked.connect(self.open_folder)
        Line(self.widget_common, (215, 5, 3, 505), False)

    def load_run(self, run):
        pass

    def get_run(self):
        return {}

    def input_config(self, _dir):
        config = {
            "模块": 6,
            "静音": False,
            "关闭软件": False,
            "完成后": 0,
            "SGA关闭": False,
            "启动路径": "",
            "附加命令": "",
            "开始前等待时间": "",
            "启动判断进程名": "",
            "启动操作类型": 0,
            "启动操作内容": "",
            "启动判断指定区域": "",
            "开始后等待时间": "",
            "结束判断进程名": "",
            "结束判断类型": 0,
            "结束判断内容": "",
            "结束判断指定区域": "",
            "判断循环": ""
        }
        config.update(_dir)
        self.set.independent.check_mute.setChecked(config["静音"])
        self.set.independent.check_kill_game.setChecked(config["关闭软件"])
        self.set.independent.combo_after.setCurrentIndex(config["完成后"])
        self.set.independent.check_kill_sga.setChecked(config["SGA关闭"])

        self.set.line_start.setText(config["启动路径"])
        self.set.line_extra.setText(config["附加命令"])

        self.set.line_fwait.setText(config["开始前等待时间"])
        self.set.line_act_proc.setText(config["启动判断进程名"])
        self.set.choose_act.setCurrentIndex(config["启动操作类型"])
        self.set.line_act.setText(config["启动操作内容"])
        self.set.line_act_zone.setText(config["结束判断指定区域"])
        self.set.line_await.setText(config["开始后等待时间"])

        self.set.line_exit_proc.setText(config["结束判断进程名"])
        self.set.choose_exit.setCurrentIndex(config["结束判断类型"])
        self.set.line_exit.setText(config["结束判断内容"])
        self.set.line_exit_zone.setText(config["结束判断指定区域"])
        self.set.line_interval.setText(config["判断循环"])

    def output_config(self):
        config = dict()
        config["模块"] = 6
        config["静音"] = self.set.independent.check_mute.isChecked()
        config["关闭软件"] = self.set.independent.check_kill_game.isChecked()
        config["完成后"] = self.set.independent.combo_after.currentIndex()
        config["SGA关闭"] = self.set.independent.check_kill_sga.isChecked()

        config["启动路径"] = self.set.line_start.text()
        config["附加命令"] = self.set.line_extra.text()

        config["开始前等待时间"] = self.set.line_fwait.text()
        config["启动判断进程名"] = self.set.line_act_proc.text()
        config["启动操作类型"] = self.set.choose_act.currentIndex()
        config["启动操作内容"] = self.set.line_act.text()
        config["启动判断指定区域"] = self.set.line_act_zone.text()
        config["开始后等待时间"] = self.set.line_await.text()

        config["结束判断进程名"] = self.set.line_exit_proc.text()
        config["结束判断类型"] = self.set.choose_exit.currentIndex()
        config["结束判断内容"] = self.set.line_exit.text()
        config["结束判断指定区域"] = self.set.line_exit_zone.text()
        config["判断循环"] = self.set.line_interval.text()
        return config

    def open_folder(self):
        _path = env.workdir + "/personal/common"
        if not os.path.exists(_path):
            os.makedirs(_path)
        self.main.indicate("", 1)
        startfile(_path)
        self.main.indicate("打开文件夹: 通用执行图像储存", 3)
