from sgacode.ui.control import (Button, Stack, Combobox,
                                PicButton, StateSigh)
from qfluentwidgets import EditableComboBox
from PyQt5.QtWidgets import QWidget
from sgacode.ui.module.moduleclass import SGAModuleGroup


# 模组设置窗口
class ModuleWindow(QWidget):
    def __init__(self, smi: SGAModuleGroup):
        super().__init__()
        self.smi = smi
        # 配置切换列表
        self.ecbconfig = EditableComboBox(self)
        self.ecbconfig.setGeometry(40, 0, 215, 35)
        # 开始暂停按钮
        deletepath = r"resources/main/button/delete.png"
        unlockpath = r"resources/main/button/unlock.png"
        lockpath = r"resources/main/button/lock.png"
        addpath = r"resources/main/button/add.png"
        sizetp = (25, 25)
        self.btconfigdelete = PicButton(self, (0, 0, 35, 35), deletepath, sizetp)
        self.btconfigdelete.hide()
        self.btconfigadd = PicButton(self, (0, 0, 35, 35), addpath, sizetp)
        self.btconfigunlock = PicButton(self, (260, 0, 35, 35), unlockpath, sizetp)
        self.btconfigunlock.hide()
        self.btconfiglock = PicButton(self, (260, 0, 35, 35), lockpath, sizetp)

        self.btpause = Button(self, (300, 0, 55, 35), "停止")
        self.btpause.hide()
        self.button_start = Button(self, (300, 0, 55, 35), "开始")

        # 堆叠窗口
        self.skmodule = Stack(self, (0, 40, 625, 540))
        # 模块按钮
        self.boxmodule = Combobox(self, (0, 45, 170, 35))
        # 图标标签
        defaultpath = "resources/main/SGA/default.png"
        self.picicon = PicButton(self, (525, 475, 100, 100), defaultpath, (98, 98))
        # 状态指示
        self.statesigh = StateSigh(self, (526, 440, 100, 40))

    def SubModuleInit(self):
        for ins in self.smi.GetInstances():
            ins.WidgetInit(self.skmodule)

            pass
            # ins.
