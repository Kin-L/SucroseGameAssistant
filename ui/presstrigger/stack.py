import os
from ui.element.ui_part import Independent
from ui.element.control import *
from tools.environment import *
from PyQt5.QtGui import QIntValidator


class Local:
    def __init__(self, stack):
        # 初始化窗口
        self.page_local = Widget(stack)
        stack.addWidget(self.page_local)
        # 添加控件
        self.label_local = Label(self.page_local, (10, 12, 200, 18), "设置页面：连点器 运行方式")
        self.button_rule = Button(self.page_local, (220, 7, 120, 30), "热键设置规则")
        Line(self.page_local, (0, 42, 610, 3))

        self.label_disable = Label(self.page_local, (10, 50, 180, 27), "禁用/启用热键：")
        self.line_disable = Lineedit(self.page_local, (130, 50, 160, 33))

        self.label_trigger1 = Label(self.page_local, (10, 90, 180, 27), "触发模式：")
        self.choose_trigger = Combobox(self.page_local, (130, 90, 100, 30))
        self.choose_trigger.addItems(["长按模式", "短按模式"])
        self.label_trigger2 = Label(self.page_local, (10, 125, 180, 27), "触发热键：")
        self.line_trigger = Lineedit(self.page_local, (130, 125, 160, 33))

        self.label_clicker_mode = Label(self.page_local, (10, 165, 180, 27), "连点模式：")
        self.choose_clicker_mode = Combobox(self.page_local, (130, 165, 100, 30))
        self.choose_clicker_mode.addItems(["按下模式", "连点模式", "脚本模式"])
        self.label_clicker = Label(self.page_local, (10, 200, 180, 27), "连点/按下键：")
        self.line_clicker = Lineedit(self.page_local, (130, 200, 160, 33))
        self.label_interval = Label(self.page_local, (10, 240, 180, 27), "间隔时间(ms)：")
        self.line_interval = Lineedit(self.page_local, (130, 240, 80, 33))
        self.line_interval.setValidator(QIntValidator())

        self.label_sc = Label(self.page_local, (10, 280, 180, 27), "脚本选择：")
        self.choose_sc = Combobox(self.page_local, (130, 280, 160, 30))
        _path = env.workdir + "/personal/ptscript"
        if not os.path.exists(_path):
            os.makedirs(_path)
        _list = os.listdir("personal/ptscript")
        _nl = []
        for i in _list:
            [name, ext] = os.path.splitext(i)
            if ext == ".txt":
                _nl += [name]
        if not _nl:
            copyfile(r"assets\presstrigger\脚本示例.txt",
                     r"personal/ptscript\脚本示例.txt")
            _nl += ["脚本示例"]
        self.choose_sc.addItems(_nl)
        self.label_scn = Label(self.page_local, (10, 320, 180, 27), "重复次数：")
        self.line_scn = Lineedit(self.page_local, (130, 320, 80, 33))
        self.line_scn.setValidator(QIntValidator())

        self.button_folder = Button(self.page_local, (300, 280, 130, 30), "打开脚本文件夹")
        self.button_refresh = TransPicButton(self.page_local, (100, 285, 20, 20),
                       "assets/main_window/ui/refresh.png", (20, 20))

        self.independent = Independent(self.page_local, (0, 250, 350, 70))
        self.independent.widget.hide()


class PressTriggerStack(Local):
    def __init__(self, widget, location):
        # 功能堆叠窗口
        self.stack = Stack(widget, location)
        Local.__init__(self, self.stack)
