from .timer.main import Timer
from ui.element.control import *
from tools.environment import env
from json import load


class Overall:
    def __init__(self, stack):
        self.widget = Widget()
        stack.addWidget(self.widget)
        Label(self.widget, (0, 0, 80, 40), "全局设置", 18)
        Line(self.widget, (0, 43, 620, 3))
        self.timer = Timer(self.widget, (0, 60, 620, 300))
        Line(self.widget, (0, 300, 620, 3))
        self.auto_update = Check(self.widget, (0, 310, 150, 40), "自动检查并更新")
        self.button_check = Button(self.widget, (135, 315, 80, 30), "检查更新")
        self.button_update = Button(self.widget, (135, 315, 80, 30), "开始更新")
        self.button_update.hide()
        self.button_update.setEnabled(False)
        Label(self.widget, (225, 310, 120, 40), f"版本号 {env.version}", 14)

        self.button_update_history = Button(self.widget, (325, 315, 80, 30), "更新日志")
        self.button_logger = Button(self.widget, (410, 315, 80, 30), "运行日志")

        self.button_github = TransPicButton(self.widget, (500, 312, 30, 30),
                                            r"assets\main_window\ui\github.png", (30, 30))
        self.button_gitee = TransPicButton(self.widget, (540, 312, 30, 30),
                                           r"assets\main_window\ui\gitee.png", (30, 30))
        self.button_bilibili = TransPicButton(self.widget, (580, 312, 30, 30),
                                              r"assets\main_window\ui\bilibili.png", (30, 30))

    @staticmethod
    def get_ver():
        with open(r"assets\main_window\version.json", 'r', encoding='utf-8') as m:
            _dir = load(m)
            return _dir["version"]
