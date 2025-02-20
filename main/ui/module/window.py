from main.ui.control import (PicButton, Button, Stack,
                             Combobox, Widget, QtCore)
from qfluentwidgets import EditableComboBox
from main.ui.ui_part import TaskWidgt
from main.tools.environment import env


# 模组设置窗口
class ModuleWindow:
    def __init__(self, _stack):
        self.widget = Widget()
        _stack.addWidget(self.widget)
        # 配置切换列表
        self.box_config_change = EditableComboBox(self.widget)
        self.box_config_change.setGeometry(QtCore.QRect(40, 0, 215, 35))
        # self.box_config_change.setEnabled(False)
        # 开始暂停按钮
        self.button_config_delete = PicButton(self.widget, (0, 0, 35, 35),
                                              r"assets\main_window\button\delete.png", (25, 25))
        self.button_config_unlock = PicButton(self.widget, (260, 0, 35, 35),
                                                   r"assets\main_window\button\unlock.png", (25, 25))
        self.button_config_unlock.hide()
        self.button_config_lock = PicButton(self.widget, (260, 0, 35, 35),
                                                 r"assets\main_window\button\lock.png", (25, 25))
        self.button_config_add = PicButton(self.widget, (300, 0, 35, 35),
                                               r"assets\main_window\button\add.png", (25, 25))

        self.button_config_save = PicButton(self.widget, (340, 0, 35, 35),
                                            r"assets\main_window\button\save.png", (25, 25))

        self.button_pause = Button(self.widget, (380, 0, 55, 35), "停止")
        self.button_pause.hide()
        self.button_start = Button(self.widget, (380, 0, 55, 35), "开始")

        # 堆叠窗口
        self.stack_module = Stack(self.widget, (0, 40, 670, 540))
        # 模块按钮
        self.box_module_change = Combobox(self.widget, (0, 45, 160, 35))
        self.box_module_change.addItems(
            ["连续任务", "环行旅舍", "原神", "MAA", "崩铁助手", "尘白禁区", "通用执行", "连点器", "绝区零助手"])

        self.mix = TaskWidgt(self, r"assets\main_window\icon\mix-icon.png", ("mix", "00"))
        self.klein = TaskWidgt(self, r"assets\main_window\icon\klein-icon.png", ("kleins", "01"))
        self.genshin = TaskWidgt(self, r"assets\snow\picture\snow-icon.png", ("genshin", "02"))
        self.maa = TaskWidgt(self, r"assets\main_window\icon\MAA-icon.png", ("maa", "03"))
        self.m7a = TaskWidgt(self, r"assets\main_window\icon\M7A-icon.png", ("m7a", "04"))
        self.snow = TaskWidgt(self, r"assets\snow\picture\snow-icon.png", ("snow", "05"))
        self.common = TaskWidgt(self, r"assets\main_window\icon\snow-icon.png", ("common", "06"))
        self.presstrigger = TaskWidgt(self, r"assets\main_window\icon\presstrigger-icon.png", ("presstrigger", "07"))
        self.zzz = TaskWidgt(self, r"assets\main_window\icon\zzz_logo.png", ("zzz", "08"))
        env.version = "v3.X.X"
        env.name = [self.mix, self.klein, self.genshin,
                    self.maa, self.m7a, self.snow,
                    self.common, self.presstrigger]

    def load_module_window(self, num):
        if num == 0:
            from main.ui.module.mix import MixList, MixStack, mix_box_refresh
            if not env.load[num]:
                self.mix.list = MixList(self.mix.widget)
                self.mix.set = MixStack(self.mix.widget)
                env.load[num] = True
            mix_box_refresh(env.config_name)
        elif num == 5:
            if not env.load[num]:
                from main.ui.module.snow.list import SnowList
                from main.ui.module.snow.stack import SnowStack
                self.snow.list = SnowList(self.snow.widget)
                self.snow.set = SnowStack(self.snow.widget)
                env.load[num] = True
        else:
            raise ValueError("load_module_window:传入值不在允许范围")

    def load_module_config(self, _dict=None):
        if _dict:
            num = _dict["模块"]
        else:
            num = 0
        if num == 0:
            from main.ui.module.mix import mix_input_config
            mix_input_config(_dict)
        elif num == 5:
            from main.ui.module.snow.configwr import snow_input_config
            snow_input_config(_dict)
        self.box_module_change.setCurrentIndex(num)

    def collect_module_config(self):
        _num = self.box_module_change.currentIndex()
        if _num == 0:
            from main.ui.module.mix import mix_collect_config
            _dict = mix_collect_config()
        elif _num == 5:
            from main.ui.module.snow.configwr import snow_collect_config
            _dict = snow_collect_config()
        else:
            _dict = {}
        return _dict


