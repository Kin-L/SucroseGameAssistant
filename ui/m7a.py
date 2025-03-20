from ui.element.control import *
from ui.element.ui_part import Independent
from tools.system import check_path
from webbrowser import open as weopen
from tools.environment import *
from task.default_task import Task

class M7AList:
    def __init__(self, widget, location):
        # 运行列表窗口
        self.scroll_list = Widget(widget, location)
        self.label_m7a = Label(self.scroll_list, (70, 10, 120, 20), "崩坏：星穹铁道助手", 18)
        Line(widget, (215, 5, 3, 505), False)


class M7AStack:
    def __init__(self, widget, location):
        # 功能堆叠窗口
        self.stack = Stack(widget, location)
        # 功能堆叠窗口
        self.stack = Widget(self.stack, (0, 0, 395, 515))
        self.label_local = Label(self.stack, (0, 12, 220, 18), "设置页面：")
        Line(self.stack, (0, 41, 395, 3))
        
        self.label_m7a_overall = Label(self.stack, (0, 45, 350, 40), "使用说明：本模块支持三月七助手和星穹铁道一\n                  条龙两种脚本")
        self.label_start = Label(self.stack, (0, 80, 80, 27), "启动路径")
        self.line_start = Lineedit(self.stack, (0, 110, 385, 33))
        Line(self.stack, (0, 150, 395, 3))

        self.label_team_tip = Label(self.stack, (0, 190, 220, 27), "独立运行设置：")
        self.independent = Independent(self.stack, (0, 220, 350, 70), False)
        self.button_m7a = Button(self.stack, (0, 300, 125, 30), "三月七助手下载")
        self.button_SROD = Button(self.stack, (130, 300, 150, 30), "星穹铁道一条龙下载")
        self.button_m7a.clicked.connect(self.open_m7a)
        self.button_SROD.clicked.connect(self.open_sr)

    @staticmethod
    def open_m7a():
        weopen("https://moesnow.github.io/March7thAssistant")

    @staticmethod
    def open_sr():
        weopen("https://github.com/DoctorReid/StarRailOneDragon")

    def open_path(self):
        _path = self.line_start.text()
        if isfile(_path):
            dire, name = split(_path)
            if "March7th" in name:
                _path = dire + "/March7th Assistant.exe"
            elif "OneDragon" in name:
                    _path = dire + "/OneDragon Launcher.exe"
            else:
                Task.indicate("无效启动路径")
                raise ValueError("崩坏：星穹铁道助手,无效启动路径")
        else:
            Task.indicate("无效启动路径")
            raise ValueError("崩坏：星穹铁道助手,无效启动路径")
        env.set_soft(None, (0, "UnityWndClass", "崩坏：星穹铁道助手"))
        env.soft.set_path(_path)
        _run = env.soft.run(fls=False, tit="m7a")
        if _run:
            pass
        else:
            Task.indicate("崩坏：星穹铁道助手启动失败")


class M7A:
    def __init__(self, stack, main):
        # 三月七助手
        self.widget_m7a = Widget()
        stack.addWidget(self.widget_m7a)
        self.button = (
            Picture(main.widget_module, (0, 0, 50, 50),
                      r"assets\m7a\picture\M7A-icon.png"))
        self.list = None
        self.set = None

    def load_window(self):
        self.list = M7AList(self.widget_m7a, (0, 0, 215, 515))
        self.set = M7AStack(self.widget_m7a, (225, 0, 395, 515))
        Line(self.widget_m7a, (215, 5, 3, 505), False)

    def load_run(self, run):
        _dir = {
            "m7a_path": ""
        }
        _dir.update(run)
        self.set.line_start.setText(_dir["m7a_path"])
        self.set.line_start.setSelection(0, 0)

    def get_run(self):
        return {"m7a_path": check_path(self.set.line_start.text())}

    def input_config(self, _dir):
        config = {
            "模块": 4,
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
        config["模块"] = 4
        config["静音"] = self.set.independent.check_mute.isChecked()
        config["关闭软件"] = True
        config["完成后"] = self.set.independent.combo_after.currentIndex()
        config["SGA关闭"] = self.set.independent.check_kill_sga.isChecked()
        return config
