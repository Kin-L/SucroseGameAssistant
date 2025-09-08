from maincode.tools.sgaqt.texts import SLineEdit, tips
from maincode.tools.sgaqt.buttons import Button, PicButton, Combobox
from maincode.tools.sgaqt.widgets import Stack, StateSigh
from PyQt5.QtWidgets import QWidget
from maincode.tools.core.constant import spr


# 模组设置窗口
class ModuleWidget(QWidget):
    def __init__(self):
        super().__init__()
        # 配置切换列表
        self.ecbconfig = Combobox(self, (40, 0, 215, 35))
        self.edlconfig = SLineEdit(self, (40, 0, 215, 35))
        self.edlconfig.hide()
        # 开始暂停按钮
        sizetp = (25, 25)
        self.btconfigdelete = PicButton(self, (0, 0, 35, 35), spr.DeletePic, sizetp)
        self.btconfigdelete.hide()
        self.btconfigadd = PicButton(self, (0, 0, 35, 35), spr.AddPic, sizetp)
        self.btconfigunlock = PicButton(self, (260, 0, 35, 35), spr.UnlockPic, sizetp)
        self.btconfigunlock.hide()
        self.btconfiglock = PicButton(self, (260, 0, 35, 35), spr.LockPic, sizetp)

        self.btconfigedit = PicButton(self, (300, 0, 35, 35), spr.RenamePic, sizetp)
        self.btconfigfinish = PicButton(self, (300, 0, 35, 35), spr.FinishPic, sizetp)
        self.btconfigfinish.hide()

        self.btpause = Button(self, (340, 0, 55, 35), "停止")
        self.btpause.hide()
        self.btstart = Button(self, (340, 0, 55, 35), "开始")
        tips(self.btstart, "点击箭头按钮切换运行模式")
        self.btstartmode = PicButton(self, (400, 0, 35, 35), spr.ArrowDownPic, sizetp)
        tips(self.btstartmode, "点击切换运行模式\n箭头向下执行当前页面任务\n箭头向左执行栏目中任务")
        # 堆叠窗口
        self.skmodule = Stack(self, (0, 40, 625, 540))
        # 模块按钮
        self.boxmodule = Combobox(self, (0, 45, 170, 35))
        # self.boxmodule.addItems(sg.subconfig.GetSignListT()[0])
        # 图标标签
        self.picicon = PicButton(self, (525, 475, 100, 100), spr.SGAdefaultPic, (98, 98))
        # 状态指示
        self.statesigh = StateSigh(self, (526, 440, 100, 40))
