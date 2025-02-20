from main.ui.control import (Button, Widget, TransPicButton,
                             Label, Line, Check)
from main.ui.overall.timer.window import TimerWindow


class OverallWindow:
    def __init__(self, _stack):
        self.widget = Widget()
        _stack.addWidget(self.widget)
        Label(self.widget, (0, 0, 80, 40), "全局设置", 18)
        Line(self.widget, (0, 43, 620, 3))
        self.timer = TimerWindow(self.widget, (0, 60, 620, 300))
        Line(self.widget, (0, 300, 620, 3))
        self.auto_update = Check(self.widget, (0, 310, 150, 40), "自动更新")
        self.button_check = Button(self.widget, (135, 315, 80, 30), "检查更新")
        self.button_update = Button(self.widget, (135, 315, 80, 30), "开始更新")
        self.button_update.hide()
        self.button_update.setEnabled(False)
        self.label_version = Label(self.widget, (225, 310, 120, 40), f"版本号 3.5.X", 14)

        self.button_update_history = Button(self.widget, (325, 315, 80, 30), "更新日志")

        self.button_github = TransPicButton(self.widget, (500, 312, 30, 30),
                                            r"assets\main_window\button\github.png", (30, 30))
        self.button_gitee = TransPicButton(self.widget, (540, 312, 30, 30),
                                           r"assets\main_window\button\gitee.png", (30, 30))
        self.button_bilibili = TransPicButton(self.widget, (580, 312, 30, 30),
                                              r"assets\main_window\button\bilibili.png", (30, 30))
