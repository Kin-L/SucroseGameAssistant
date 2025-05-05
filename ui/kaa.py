import os
from ui.element.control import *
from os.path import isfile, split
from tools.environment import env
from task.default_task import Task
from tools.system import check_path
from webbrowser import open as weopen
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from ui.element.ui_part import Independent


class KaaList:
    def __init__(self, widget, location):
        # 运行列表窗口
        self.scroll_list = Widget(widget, location)
        self.label_kaa = Label(self.scroll_list, (70, 10, 120, 20), "琴音小助手", 18)
        Line(widget, (215, 5, 3, 505), False)


class KaaStack:
    def __init__(self, widget, location):
        # 功能堆叠窗口
        self.stack = Stack(widget, location)
        # 功能堆叠窗口
        self.stack = Widget(self.stack, (0, 0, 395, 515))
        self.label_local = Label(self.stack, (0, 12, 220, 18), "设置页面：")
        Line(self.stack, (0, 41, 395, 3))

        Y_KAA_PATH = 90
        self.label_kaa_overall = Label(self.stack, (0, 45, 360, 40), "使用说明：本模块支持琴音小助手运行，请确保\n                  您已正确安装并配置好相关软件。")
        self.label_path = Label(self.stack, (0, Y_KAA_PATH, 120, 27), "琴音小助手路径")
        self.line_path = Lineedit(self.stack, (0, Y_KAA_PATH + 30, 355, 33))
        self.button_select = Button(self.stack, (360, Y_KAA_PATH + 30, 35, 33), "...")
        self.button_select.clicked.connect(self.select_kaa_path)
        Line(self.stack, (0, 190, 395, 3))

        self.label_team_tip = Label(self.stack, (0, 200, 220, 27), "独立运行设置：")
        self.independent = Independent(self.stack, (0, 230, 350, 70), False)
        self.button_github = Button(self.stack, (0, 310, 160, 30), "琴音小助手下载")
        self.button_tutorial = Button(self.stack, (180, 310, 160, 30), "使用教程")
        self.button_github.clicked.connect(self.open_kaa_github)
        self.button_tutorial.clicked.connect(self.open_kaa_tutorial)

    @staticmethod
    def open_kaa_github():
        weopen("https://github.com/XcantloadX/kotones-auto-assistant/releases")
        
    @staticmethod
    def open_kaa_tutorial():
        weopen("https://kdocs.cn/l/cetCY8mGKHLj")

    def select_kaa_path(self):
        # 选择文件夹
        path = str(QFileDialog.getExistingDirectory(self.stack, "选择琴音小助手所在文件夹"))
        if not path:
            return
        if not self.check_kaa_installed(path):
            QMessageBox.information(self.stack, "提示", "未找到琴音小助手或未安装。需至少执行一次琴音小助手本体才能使用。")
            return
        self.line_path.setText(path)

    def check_kaa_installed(self, path):
        """
        检查琴音小助手是否安装
        :param path: 琴音小助手路径
        :return: bool
        """
        if not os.path.isdir(path):
            return False
        # 判断 <path>\WPy64-310111\python-3.10.11.amd64\Scripts\kaa.exe
        return os.path.isfile(path + r"\WPy64-310111\python-3.10.11.amd64\Scripts\kaa.exe")


class Kaa:
    def __init__(self, stack, main):
        # 琴音小助手
        self.widget_kaa = Widget()
        stack.addWidget(self.widget_kaa)
        self.button = (
            Picture(main.widget_module, (0, 0, 50, 50),
                      r"assets\kaa\picture\kaa-icon.png"))
        self.list = None
        self.set = None

    def load_window(self):
        self.list = KaaList(self.widget_kaa, (0, 0, 215, 515))
        self.set = KaaStack(self.widget_kaa, (225, 0, 395, 515))
        Line(self.widget_kaa, (215, 5, 3, 505), False)

    def load_run(self, run):
        _dir = {
            "kaa_path": ""
        }
        _dir.update(run)
        self.set.line_path.setText(_dir["kaa_path"])
        self.set.line_path.setSelection(0, 0)

    def get_run(self):
        return {"kaa_path": check_path(self.set.line_path.text())}

    def input_config(self, _dir):
        config = {
            "模块": 10,
            "静音": False,
            "关闭软件": False,
            "完成后": 0,
            "SGA关闭": False
        }
        config.update(_dir)
        self.set.independent.check_mute.setChecked(config["静音"])
        self.set.independent.combo_after.setCurrentIndex(config["完成后"])
        self.set.independent.check_kill_sga.setChecked(config["SGA关闭"])

    def output_config(self):
        config = dict()
        config["模块"] = 10
        config["静音"] = self.set.independent.check_mute.isChecked()
        config["关闭软件"] = True
        config["完成后"] = self.set.independent.combo_after.currentIndex()
        config["SGA关闭"] = self.set.independent.check_kill_sga.isChecked()
        return config