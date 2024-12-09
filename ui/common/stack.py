from ui.element.ui_part import Independent
from ui.element.control import *


class Local:
    def __init__(self, stack):
        # 初始化窗口
        self.page_local = Widget(stack)
        stack.addWidget(self.page_local)
        # 添加控件
        self.label_local = Label(self.page_local, (0, 12, 180, 18), "设置页面：通用执行 运行方式")

        Line(self.page_local, (0, 42, 395, 3))

        self.label_common_overall = Label(self.page_local, (0, 50, 180, 27), "全局设置：")

        self.label_start = Label(self.page_local, (0, 82, 80, 27), "启动路径：")
        self.line_start = Lineedit(self.page_local, (0, 115, 385, 33))
        self.label_extra = Label(self.page_local, (0, 147, 80, 27), "附加命令：")
        self.line_extra = Lineedit(self.page_local, (0, 180, 385, 33))

        Line(self.page_local, (0, 217, 395, 3))

        self.label_common_tip = Label(self.page_local, (0, 220, 220, 27), "独立运行设置：")
        self.independent = Independent(self.page_local, (0, 250, 350, 70))


class Start:
    def __init__(self, stack):
        # 初始化窗口
        self.page_start = Widget(stack)
        stack.addWidget(self.page_start)
        # 添加控件
        self.label_start = Label(self.page_start, (0, 12, 220, 18), "设置页面：启动设置")

        Line(self.page_start, (0, 42, 395, 3))

        self.label_fwait = Label(self.page_start, (0, 55, 150, 18), "开始前等待时间(秒)：")
        self.line_fwait = Lineedit(self.page_start, (150, 50, 70, 30))
        self.label_act_proc = Label(self.page_start, (0, 85, 100, 27), "指定进程名：")
        self.line_act_proc = Lineedit(self.page_start, (0, 120, 385, 33))
        self.label_act = Label(self.page_start, (0, 160, 80, 27), "启动操作：")
        self.choose_act = Combobox(self.page_start, (0, 190, 100, 30))
        self.choose_act.addItems(["无", "点击文本", "点击图像", "快捷键"])
        self.line_act = Lineedit(self.page_start, (0, 233, 385, 33))
        self.button_folder = Button(self.page_start, (110, 190, 130, 30), "图像储存文件夹")
        self.label_act_zone = Label(self.page_start, (0, 280, 80, 27), "指定区域：")
        self.line_act_zone = Lineedit(self.page_start, (0, 315, 180, 33))
        self.label_await = Label(self.page_start, (0, 365, 120, 18), "开始后等待时间：")
        self.line_await = Lineedit(self.page_start, (125, 360, 70, 33))


class Exit:
    def __init__(self, stack):
        # 初始化窗口
        self.page_exit = Widget(stack)
        stack.addWidget(self.page_exit)
        # 添加控件
        self.label_exit = Label(self.page_exit, (0, 12, 180, 18), "设置页面：结束设置")

        Line(self.page_exit, (0, 42, 395, 3))

        self.label_exit_proc = Label(self.page_exit, (0, 50, 100, 27), "指定进程名：")
        self.line_exit_proc = Lineedit(self.page_exit, (0, 85, 385, 33))
        self.label_choose_exit = Label(self.page_exit, (0, 125, 80, 27), "结束判断：")

        self.choose_exit = Combobox(self.page_exit, (0, 160, 120, 30))
        self.choose_exit.addItems(["进程退出", "匹配到文本", "匹配到图像", "cpu利用率"])
        self.line_exit = Lineedit(self.page_exit, (0, 205, 385, 33))
        self.label_exit_zone = Label(self.page_exit, (0, 240, 80, 27), "指定区域：")
        self.line_exit_zone = Lineedit(self.page_exit, (0, 275, 180, 33))
        self.label_interval = Label(self.page_exit, (0, 310, 180, 27), "判断循环（间隔/次数）：")
        self.line_interval = Lineedit(self.page_exit, (0, 345, 180, 33))


class CommonStack(Local, Start, Exit):
    def __init__(self, widget, location):
        # 功能堆叠窗口
        self.stack = Stack(widget, location)
        Local.__init__(self, self.stack)
        Start.__init__(self, self.stack)
        Exit.__init__(self, self.stack)
