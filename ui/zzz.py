from ui.element.control import *
from ui.element.ui_part import Independent
from tools.system import check_path
from webbrowser import open as weopen


class zzzList:
    def __init__(self, widget, location):
        # 运行列表窗口
        self.scroll_list = Widget(widget, location)
        self.label_zzz = Label(self.scroll_list, (70, 10, 120, 20), "绝区零助手", 18)
        Line(widget, (215, 5, 3, 505), False)


class zzzStack:
    def __init__(self, widget, location):
        # 功能堆叠窗口
        self.stack = Stack(widget, location)
        # 功能堆叠窗口
        self.stack = Widget(self.stack, (0, 0, 395, 515))
        self.label_local = Label(self.stack, (0, 12, 220, 18), "设置页面：")
        Line(self.stack, (0, 41, 395, 3))
        
        self.label_zzz_overall = Label(self.stack, (0, 45, 360, 40), "使用说明：本模块支持绝区零一条龙运行，请确保\n                  您已正确安装并配置好相关软件。")
        self.label_start = Label(self.stack, (0, 80, 80, 27), "启动路径")
        self.line_start = Lineedit(self.stack, (0, 110, 385, 33))
        Line(self.stack, (0, 152, 395, 3))

        self.label_team_tip = Label(self.stack, (0, 160, 220, 27), "独立运行设置：")
        self.independent = Independent(self.stack, (0, 200, 350, 70), False)
        self.button_zzz = Button(self.stack, (0, 280, 140, 30), "绝区零一条龙下载")
        self.button_zzz.clicked.connect(self.open_zzz)
    @staticmethod
    def open_zzz():
        weopen("https://one-dragon.org/zzz/zh/home.html")

class zzz:
    def __init__(self, stack, main):
        # 绝区零一条龙
        self.widget_zzz = Widget()
        stack.addWidget(self.widget_zzz)
        self.button = (
            Picture(main.widget_module, (0, 0, 50, 50),
                      r"assets\zzz\pictures\zzz_logo.png"))
        self.list = None
        self.set = None

    def load_window(self):
        self.list = zzzList(self.widget_zzz, (0, 0, 215, 515))
        self.set = zzzStack(self.widget_zzz, (225, 0, 395, 515))
        Line(self.widget_zzz, (215, 5, 3, 505), False)

    def load_run(self, run):
        _dir = {
            "zzz_path": ""
        }
        _dir.update(run)
        self.set.line_start.setText(_dir["zzz_path"])
        self.set.line_start.setSelection(0, 0)

    def get_run(self):
        return {"zzz_path": check_path(self.set.line_start.text())}

    def input_config(self, _dir):
        config = {
            "模块": 8,
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
        config["模块"] = 8
        config["静音"] = self.set.independent.check_mute.isChecked()
        config["关闭软件"] = True
        config["完成后"] = self.set.independent.combo_after.currentIndex()
        config["SGA关闭"] = self.set.independent.check_kill_sga.isChecked()
        return config
