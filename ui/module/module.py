from qfluentwidgets import EditableComboBox
from ui.element.control import *


# 模组设置窗口
class ModuleWindow:
    def __init__(self, main):
        # 模块设置窗口
        self.widget_module = Widget(None, (5, 0, 670, 570))
        main.stack_setting.addWidget(self.widget_module)
        # 模块按钮
        self.scroll_list = ScrollArea(self.widget_module, (0, 0, 215, 65))
        self.widget_icon = Widget(self.scroll_list, (0, 0, 325, 50))
        self.widget_icon.setMinimumSize(325, 50)
        self.scroll_list.setWidget(self.widget_icon)
        self.scroll_list.setFrameShape(QtWidgets.QFrame.Shape(0))
        # 配置切换列表
        self.box_config_change = EditableComboBox(self.widget_module)
        self.box_config_change.setGeometry(QtCore.QRect(265, 9, 215, 30))
        # self.box_config_change.setEnabled(False)
        # 开始暂停按钮
        self.button_config_delete = PicButton(self.widget_module, (225, 8, 35, 35),
                                              r"assets\main_window\ui\delete.png", (25, 25))
        self.button_config_unlock = TransPicButton(self.widget_module, (485, 8, 35, 35),
                                                   r"assets\main_window\ui\unlock.png", (25, 25))
        self.button_config_unlock.hide()
        self.button_config_lock = TransPicButton(self.widget_module, (485, 8, 35, 35),
                                                 r"assets\main_window\ui\lock.png", (25, 25))

        self.button_config_save = PicButton(self.widget_module, (525, 8, 35, 35),
                                            r"assets\main_window\ui\save.png", (25, 25))

        self.button_pause = Button(self.widget_module, (565, 8, 55, 35), "停止")
        self.button_pause.hide()
        self.button_start = Button(self.widget_module, (565, 8, 55, 35), "开始")
        # 堆叠窗口
        self.stack_module = Stack(self.widget_module, (0, 65, 670, 515))


