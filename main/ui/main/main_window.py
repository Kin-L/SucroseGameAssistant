from ..control import PicButton, Button, Picture, Stack
from ..ui_part import Support, OverallButton, InfoBox, MainWindow


class MainWindows:
    def __init__(self):
        # 主窗口初始化
        self.main_window = MainWindow()
        self.label_status = Picture(self.main_window, (0, 0, 910, 580),  # 指示图标
                                    r"assets\main_window\ui\ico\0.png")
        # 全局/模块 设置按钮
        self.button_set_home = OverallButton(self.main_window)  # 全局/模块 设置按钮
        self.button_history = PicButton(self.main_window, (693, 0, 56, 56),  # 历史信息按钮
                                        r"assets\main_window\ui\history.png", (25, 25))
        self.button_sponsor = PicButton(self.main_window, (751, 0, 56, 56),  # 赞赏按钮
                                        r"assets\main_window\ui\support.png", (25, 25))
        self.window_support = Support()
        self.button_statement = Button(self.main_window, (809, 0, 96, 27), "使用须知")
        self.button_instructions = Button(self.main_window, (809, 29, 96, 27), "使用说明")
        self.label_status = Picture(self.main_window, (485, 430, 150, 150),  # 指示图标
                                    r"assets\main_window\ui\ico\0.png")
        self.box_info = InfoBox(self.main_window)  # 指示信息窗口
        self.stack_setting = Stack(self.main_window, (5, 0, 620, 570))
        self.state = None

