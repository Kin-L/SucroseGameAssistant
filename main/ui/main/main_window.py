from ..control import PicButton, Button, Picture, Stack, Widget
from ..ui_part import Support, InfoBox, OverallButton, MainWidget


class MainWindow:
    def __init__(self):
        self.widget = MainWidget()
        self.label_shelter = Picture(self.widget, (0, 0, 910, 580),  # 指示图标
                                          r"assets\main_window\back\set_back.png")
        self.label_shelter.raise_()
        # 全局/模块 设置按钮
        self.button_set_home = OverallButton(self.widget)  # 全局/模块 设置按钮
        self.button_history = PicButton(self.widget, (693, 0, 56, 56),  # 历史信息按钮
                                             r"assets\main_window\button\history.png", (25, 25))
        self.button_sponsor = PicButton(self.widget, (751, 0, 56, 56),  # 赞赏按钮
                                             r"assets\main_window\button\support.png", (25, 25))
        self.window_support = Support()
        self.button_statement = Button(self.widget, (809, 0, 96, 27), "使用须知")
        self.button_instructions = Button(self.widget, (809, 29, 96, 27), "使用说明")
        self.label_status = Picture(self.widget, (485, 430, 150, 150),  # 指示图标
                                         r"assets\main_window\indicate\0.png")
        self.box_info = InfoBox(self.widget)  # 指示信息窗口
        self.stack_setting = Stack(self.widget, (5, 0, 620, 570))

