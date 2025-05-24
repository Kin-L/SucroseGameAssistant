from sgacode.ui.control import Button, Stack, Combobox, PicButton
from qfluentwidgets import EditableComboBox
from PyQt5.QtWidgets import QWidget
from sgacode.ui.module.moduleclass import SGAModuleInstances


# 模组设置窗口
class ModuleWindow(QWidget):
    def __init__(self, smi: SGAModuleInstances):
        super().__init__()
        self.smi = smi
        # 配置切换列表
        self.ecbconfig = EditableComboBox(self)
        self.ecbconfig.setGeometry(40, 0, 215, 35)
        # self.box_config_change.setEnabled(False)
        # 开始暂停按钮
        deletepath = r"resources/main/button/delete.png"
        unlockpath = r"resources/main/button/unlock.png"
        lockpath = r"resources/main/button/lock.png"
        addpath = r"resources/main/button/add.png"
        savepath = r"resources/main/button/save.png"
        sizetp = (25, 25)
        self.btconfigdelete = PicButton((0, 0, 35, 35), deletepath, sizetp)
        self.btconfigunlock = PicButton((260, 0, 35, 35), unlockpath, sizetp)
        self.btconfiglock = PicButton((260, 0, 35, 35), lockpath, sizetp)
        self.btconfigadd = PicButton((300, 0, 35, 35), addpath, sizetp)
        self.btconfigsave = PicButton((340, 0, 35, 35), savepath, sizetp)

        self.btpause = Button((380, 0, 55, 35), "停止")
        self.btpause.hide()
        self.button_start = Button((380, 0, 55, 35), "开始")

        # 堆叠窗口
        self.skmodule = Stack((0, 40, 670, 540))
        # 模块按钮
        self.boxmodule = Combobox((0, 45, 160, 35))

    def SubModuleInit(self):
        for ins in self.smi.GetInstances():
            pass
            # ins.
