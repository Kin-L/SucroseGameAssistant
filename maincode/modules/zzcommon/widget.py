from typing import Optional
import os
from PyQt5.QtGui import QIntValidator

from maincode.config.configctrl import scc
from maincode.tools.sgaqt.texts import Label, Picture, SLineEdit, Line
from maincode.tools.sgaqt.buttons import Button, Combobox, SetButton
from maincode.tools.sgaqt.widgets import Widget, SetStackPage, ModuleStackPage, TaskPanel


class CommonPage(ModuleStackPage):
    def __init__(self):
        super().__init__()
        self.wdlist: Optional[CommonList] = None
        self.page00: Optional[CommonPage00Set] = None
        self.page01: Optional[CommonPage01Set] = None
        self.page02: Optional[CommonPage02Set] = None
        self.picbt: Optional[Picture] = None
        self.pbset00 = SetButton(self, (180, 10, 25, 25), (25, 25))

    def LoadWidget(self):
        # 初始化功能列表
        self.wdlist = CommonList()
        self.srlist.setWidget(self.wdlist)

        # 初始化设置页面
        self.page00 = CommonPage00Set()
        self.page01 = CommonPage01Set()
        self.page02 = CommonPage02Set()
        self.sksetting.addWidget(self.page00)
        self.sksetting.addWidget(self.page01)
        self.sksetting.addWidget(self.page02)

        # 分隔线
        Line(self, (215, 5, 3, 530), False)

        self.pbset00.clicked.connect(lambda: self.sksetting.setCurrentIndex(0))
        self.wdlist.pbset01.clicked.connect(lambda: self.sksetting.setCurrentIndex(1))
        self.wdlist.pbset02.clicked.connect(lambda: self.sksetting.setCurrentIndex(2))
        self.page01.button_folder.clicked.connect(self._open_image_folder)

    @staticmethod
    def _open_image_folder():
        """打开图像储存文件夹"""
        _path = f"{scc.mc.WorkDir}/personal/common"
        if not os.path.exists(_path):
            os.makedirs(_path)
        os.startfile(_path)

    def SetWidget(self, config: dict):
        """从配置更新UI控件"""
        # 本地设置页
        self.page00.choose_mode.setCurrentIndex(config["StartMode"])
        self.page00.line_command.setText(config["CMDLine"])
        self.page00.taskpanel.ckkillsga.setChecked(config["SGAClose"])
        self.page00.taskpanel.ckmute.setChecked(config["Mute"])
        self.page00.taskpanel.ckkillprog.setChecked(config["SoftClose"])
        self.page00.taskpanel.cbafter.setCurrentIndex(config["Finished"])

        # 启动设置页
        self.page01.line_fwait.setText(config["WaitTimeBefore"])
        self.page01.line_act_proc.setText(config["StartProcess"])
        self.page01.choose_act.setCurrentIndex(config["StartOperateMode"])
        self.page01.line_act.setText(config["StartOperateContent"])
        self.page01.line_act_zone.setText(config["StartRecogZone"])
        self.page01.line_await.setText(config["WaitTimeAfter"])

        # 结束设置页
        self.page02.line_exit_proc.setText(config["EndProcess"])
        self.page02.choose_exit.setCurrentIndex(config["EndRecogMode"])
        self.page02.line_exit.setText(config["EndRecogContent"])
        self.page02.line_exit_zone.setText(config["EndRecogZone"])
        self.page02.line_interval.setText(config["Circular"])

    def CollectConfig(self) -> dict:
        """从UI收集配置信息"""
        return {
            "StartMode": self.page00.choose_mode.currentIndex(),
            "CMDLine": self.page00.line_command.text(),
            "Mute": self.page00.taskpanel.ckmute.isChecked(),
            "SoftClose": self.page00.taskpanel.ckkillprog.isChecked(),
            "Finished": self.page00.taskpanel.cbafter.currentIndex(),
            "SGAClose": self.page00.taskpanel.ckkillsga.isChecked(),
            # 启动设置
            "WaitTimeBefore": self.page01.line_fwait.text(),
            "StartProcess": self.page01.line_act_proc.text(),
            "StartOperateMode": self.page01.choose_act.currentIndex(),
            "StartOperateContent": self.page01.line_act.text(),
            "StartRecogZone": self.page01.line_act_zone.text(),
            "WaitTimeAfter": self.page01.line_await.text(),
            # 结束设置
            "EndProcess": self.page02.line_exit_proc.text(),
            "EndRecogMode": self.page02.choose_exit.currentIndex(),
            "EndRecogContent": self.page02.line_exit.text(),
            "EndRecogZone": self.page02.line_exit_zone.text(),
            "Circular": self.page02.line_interval.text(),

        }


class CommonList(Widget):
    def __init__(self):
        super().__init__()
        self.lbitem01 = Label(self, (10, 5, 120, 22), "启动设置")
        self.lbitem02 = Label(self, (10, 50, 120, 22), "结束设置")
        self.pbset01 = SetButton(self, (180, 5, 25, 25), (25, 25))
        self.pbset02 = SetButton(self, (180, 50, 25, 25), (25, 25))


class CommonPage00Set(SetStackPage):
    def __init__(self):
        super().__init__("设置页面：运行方式")
        # 全局设置区域
        Label(self, (0, 50, 120, 27), "全局设置：")

        Label(self, (0, 82, 80, 27), "启动模式：")
        self.choose_mode = Combobox(self, (0, 115, 200, 30))
        self.choose_mode.addItems(["文件路径启动", "命令行自定义命令启动"])

        Label(self, (0, 147, 180, 27), "文件路径 / CMD命令：")
        self.line_command = SLineEdit(self, (0, 180, 395, 33))

        Line(self, (0, 217, 395, 3))

        self.taskpanel = TaskPanel(self, 220)


class CommonPage01Set(SetStackPage):
    def __init__(self):
        super().__init__("设置页面：启动设置")
        # 启动前设置
        Label(self, (0, 55, 150, 18), "开始前等待时间(秒)：")
        self.line_fwait = SLineEdit(self, (160, 50, 70, 30))
        self.line_fwait.setValidator(QIntValidator())

        Label(self, (0, 85, 120, 27), "指定进程名：")
        self.line_act_proc = SLineEdit(self, (0, 120, 395, 33))

        # 启动操作设置
        Label(self, (0, 160, 80, 27), "启动操作：")
        self.choose_act = Combobox(self, (0, 190, 100, 30))
        self.choose_act.addItems(["无", "点击文本", "点击图像", "快捷键"])

        self.button_folder = Button(self, (115, 190, 130, 30), "图像储存文件夹")
        self.line_act = SLineEdit(self, (0, 233, 395, 33))

        # 区域与等待设置
        Label(self, (0, 280, 100, 27), "指定区域：")
        self.line_act_zone = SLineEdit(self, (0, 315, 180, 33))

        Label(self, (0, 365, 150, 18), "开始后等待时间(秒)：")
        self.line_await = SLineEdit(self, (150, 360, 70, 30))
        self.line_await.setValidator(QIntValidator())


class CommonPage02Set(SetStackPage):
    def __init__(self):
        super().__init__("设置页面：结束设置")
        Label(self, (0, 50, 120, 27), "指定进程名：")
        self.line_exit_proc = SLineEdit(self, (0, 85, 395, 33))

        # 结束判断设置
        Label(self, (0, 125, 80, 27), "结束判断：")
        self.choose_exit = Combobox(self, (0, 160, 120, 30))
        self.choose_exit.addItems(["进程退出", "匹配到文本", "匹配到图像", "cpu利用率"])

        self.line_exit = SLineEdit(self, (0, 205, 395, 33))

        # 区域与循环设置
        Label(self, (0, 240, 100, 27), "指定区域：")
        self.line_exit_zone = SLineEdit(self, (0, 275, 180, 33))

        Label(self, (0, 310, 180, 27), "判断循环（间隔/次数）：")
        self.line_interval = SLineEdit(self, (0, 345, 180, 33))
