from .timer.main import Timer
from ui.element.control import *
import json
import webbrowser


class Overall:
    def __init__(self, stack):
        self.widget = Widget()
        stack.addWidget(self.widget)
        Label(self.widget, (0, 0, 80, 40), "全局设置", 18)
        Line(self.widget, (0, 43, 620, 3))
        self.timer = Timer(self.widget, (0, 60, 620, 300))
        Line(self.widget, (0, 300, 620, 3))
        self.auto_update = Check(self.widget, (0, 310, 150, 40), "自动检查并更新")
        self.button_check = Button(self.widget, (145, 315, 100, 30), "检查更新")
        self.button_update = Button(self.widget, (145, 315, 100, 30), "开始更新")
        self.button_update.hide()
        self.button_update.setEnabled(False)
        self.version = self.get_ver()
        Label(self.widget, (255, 310, 120, 40), f"版本号 {self.version}", 14)
        self.button_github = TransPicButton(self.widget, (400, 312, 30, 30), r"assets\main_window\ui\github.png", (30, 30))
        self.button_gitee = TransPicButton(self.widget, (440, 312, 30, 30), r"assets\main_window\ui\gitee.png", (30, 30))
        self.button_bilibili = TransPicButton(self.widget, (480, 312, 30, 30), r"assets\main_window\ui\bilibili.png", (30, 30))
        self.button_github.clicked.connect(self.open_github)
        self.button_gitee.clicked.connect(self.open_gitee)
        self.button_bilibili.clicked.connect(self.open_bilibili)

    @staticmethod
    def get_ver():
        with open(r"assets\main_window\version.json", 'r', encoding='utf-8') as m:
            _dir = json.load(m)
            return _dir["version"]
        
    @staticmethod
    def open_github():
        webbrowser.open("https://github.com/Kin-L/SucroseGameAssistant")
    
    @staticmethod
    def open_gitee():
        webbrowser.open("https://gitee.com/huixinghen/SucroseGameAssistant")
    
    @staticmethod
    def open_bilibili():
        webbrowser.open("https://space.bilibili.com/406315493")