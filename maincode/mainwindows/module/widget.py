from maincode.tools.controls import (Button, Stack, Combobox,
                                     PicButton, StateSigh, SLineEdit)
from PyQt5.QtWidgets import QWidget


# 模组设置窗口
class ModuleWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 配置切换列表
        self.ecbconfig = Combobox(self, (40, 0, 215, 35))
        self.edlconfig = SLineEdit(self, (40, 0, 215, 35))
        self.edlconfig.hide()
        # 开始暂停按钮
        deletepath = r"resources/main/button/delete.png"
        unlockpath = r"resources/main/button/unlock.png"
        lockpath = r"resources/main/button/lock.png"
        addpath = r"resources/main/button/add.png"
        finish = r"resources/main/button/finish.png"
        rename = r"resources/main/button/rename.png"
        sizetp = (25, 25)
        self.btconfigdelete = PicButton(self, (0, 0, 35, 35), deletepath, sizetp)
        self.btconfigdelete.hide()
        self.btconfigadd = PicButton(self, (0, 0, 35, 35), addpath, sizetp)
        self.btconfigunlock = PicButton(self, (260, 0, 35, 35), unlockpath, sizetp)
        self.btconfigunlock.hide()
        self.btconfiglock = PicButton(self, (260, 0, 35, 35), lockpath, sizetp)

        self.btconfigedit = PicButton(self, (300, 0, 35, 35), rename, sizetp)
        self.btconfigfinish = PicButton(self, (300, 0, 35, 35), finish, sizetp)
        self.btconfigfinish.hide()

        self.btpause = Button(self, (340, 0, 55, 35), "停止")
        self.btpause.hide()
        self.btstart = Button(self, (340, 0, 55, 35), "开始")

        # 堆叠窗口
        self.skmodule = Stack(self, (0, 40, 625, 540))
        # 模块按钮
        self.boxmodule = Combobox(self, (0, 45, 170, 35))
        # self.boxmodule.addItems(sg.subconfig.GetSignListT()[0])
        # 图标标签
        defaultpath = "resources/main/SGA/default.png"
        self.picicon = PicButton(self, (525, 475, 100, 100), defaultpath, (98, 98))
        # 状态指示
        self.statesigh = StateSigh(self, (526, 440, 100, 40))
