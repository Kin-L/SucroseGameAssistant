from ui.element.control import *
from ui.element.ui_part import Independent
from tools.system import check_path
from webbrowser import open as weopen


class wwList:
    def __init__(self, widget, location):
        # 运行列表窗口
        self.scroll_list = Widget(widget, location)
        self.label_ww = Label(self.scroll_list, (70, 10, 120, 20), "鸣潮助手", 18)
        Line(widget, (215, 5, 3, 505), False)


class wwStack:
    def __init__(self, widget, location):
        # 功能堆叠窗口
        self.stack = Stack(widget, location)
        # 功能堆叠窗口
        self.stack = Widget(self.stack, (0, 0, 395, 515))
        self.label_local = Label(self.stack, (0, 12, 220, 18), "设置页面：")
        Line(self.stack, (0, 41, 395, 3))
        
        self.label_ww_overall = Label(self.stack, (0, 45, 360, 65), "使用说明：本模块支持ok-ww一条龙运行，请确保\n                  您已正确安装并配置好相关软件。\n    请在ok—ww一条龙设置点击内创建快捷启动方式")


        self.label_team_tip = Label(self.stack, (0, 160, 220, 27), "独立运行设置：")
        self.independent = Independent(self.stack, (0, 200, 350, 70), False)
        self.button_ww = Button(self.stack, (0, 280, 160, 30), "ok-ww鸣潮助手下载")
        self.button_ww.clicked.connect(self.open_ww)
    @staticmethod
    def open_ww():
        weopen("https://github.com/ok-oldking/ok-wuthering-waves")

class ww:
    def __init__(self, stack, main):
        # 鸣潮一条龙
        self.widget_ww = Widget()
        stack.addWidget(self.widget_ww)
        self.button = (
            Picture(main.widget_module, (0, 0, 50, 50),
                      r"assets\ww\pictures\ww_logo.png"))
        self.list = None
        self.set = None

    def load_window(self):
        self.list = wwList(self.widget_ww, (0, 0, 215, 515))
        self.set = wwStack(self.widget_ww, (225, 0, 395, 515))
        Line(self.widget_ww, (215, 5, 3, 505), False)

    def load_run(self, run):
        _dir = {}
        _dir.update(run)

    def get_run(self):
        return {}
    
    def input_config(self, _dir):
        config = {
            "模块": 9,
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
        config["模块"] = 9
        config["静音"] = self.set.independent.check_mute.isChecked()
        config["关闭软件"] = True
        config["完成后"] = self.set.independent.combo_after.currentIndex()
        config["SGA关闭"] = self.set.independent.check_kill_sga.isChecked()
        return config
