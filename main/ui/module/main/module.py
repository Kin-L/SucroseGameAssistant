from main.ui.control import (PicButton, Button, Stack,
                             Combobox, TransPicButton, Widget)
from main.ui.ui_part import TaskWidgt


# 模组设置窗口
class ModuleWindow:
    def __init__(self, _stack):
        self.widget = Widget()
        _stack.addWidget(self.widget)
        # 模块按钮
        self.box_module_change = Combobox(self.widget, (55, 8, 160, 35))
        self.box_module_change.addItems(
            ["连续任务", "环行旅舍", "原神", "MAA", "崩坏：星穹铁道助手", "尘白禁区", "通用执行", "连点器", "绝区零助手"])
        # 配置切换列表
        self.box_config_change = Combobox(self.widget, (265, 9, 215, 35))
        # self.box_config_change.setEnabled(False)
        # 开始暂停按钮
        self.button_config_delete = PicButton(self.widget, (225, 8, 35, 35),
                                              r"assets\main_window\button\delete.png", (25, 25))
        self.button_config_unlock = TransPicButton(self.widget, (485, 8, 35, 35),
                                                   r"assets\main_window\button\unlock.png", (25, 25))
        self.button_config_unlock.hide()
        self.button_config_lock = TransPicButton(self.widget, (485, 8, 35, 35),
                                                 r"assets\main_window\button\lock.png", (25, 25))

        self.button_config_save = PicButton(self.widget, (525, 8, 35, 35),
                                            r"assets\main_window\button\save.png", (25, 25))

        self.button_pause = Button(self.widget, (565, 8, 55, 35), "停止")
        self.button_pause.hide()
        self.button_start = Button(self.widget, (565, 8, 55, 35), "开始")
        # 堆叠窗口
        self.stack_module = Stack(self.widget, (0, 65, 670, 515))
        self.mix = TaskWidgt(self, r"assets\main_window\icon\mix-icon.png")
        self.klein = TaskWidgt(self, r"assets\main_window\icon\klein-icon.png")
        self.genshin = TaskWidgt(self, r"assets\snow\picture\snow-icon.png")
        self.maa = TaskWidgt(self, r"assets\main_window\icon\MAA-icon.png")
        self.m7a = TaskWidgt(self, r"assets\main_window\icon\M7A-icon.png")
        self.snow = TaskWidgt(self, r"assets\snow\picture\snow-icon.png")
        self.common = TaskWidgt(self, r"assets\main_window\icon\snow-icon.png")
        self.presstrigger = TaskWidgt(self, r"assets\main_window\icon\presstrigger-icon.png")
        self.zzz = TaskWidgt(self, r"assets\main_window\icon\zzz_logo.png")
