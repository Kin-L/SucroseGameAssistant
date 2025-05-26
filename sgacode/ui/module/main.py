from sgacode.ui.control import (Button, Stack, Combobox,
                                PicButton, StateSigh)
from qfluentwidgets import EditableComboBox
from PyQt5.QtWidgets import QWidget
from sgacode.ui.module.moduleclass import SGAModuleGroup
from sgacode.configclass import SGAMainConfig
from sgacode.tools.main import env
import json


# 模组设置窗口
class ModuleWindow(QWidget):
    def __init__(self, smc: SGAMainConfig, smg: SGAModuleGroup):
        super().__init__()
        self.SMC = smc
        self.SMG = smg
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

    def setlock(self, lock: bool):
        if lock:
            self.btconfiglock.show()
            self.btconfigunlock.hide()
            self.btconfigdelete.hide()
            self.btconfigadd.show()
        else:
            self.btconfiglock.hide()
            self.btconfigunlock.show()
            self.btconfigdelete.show()
            self.btconfigadd.hide()

    def SubModuleInit(self):
        # 加载设置
        keys, modulekeys, names = list(zip(*env.value["SubConfigs"]))
        self.ecbconfig.addItems(names)
        self.setlock(self.SMC['ConfigLock'])
        configkey = self.SMC['ConfigKey']
        if configkey in keys:
            seq = keys.index(configkey)
        else:
            seq = 0
        self.ecbconfig.setCurrentIndex(seq)
        for ins in self.SMG.GetInstances():
            ins.Widget = ins.PageClass()
            self.skmodule.addWidget(ins.Widget)
        curconfig = self.SMC['CurrentConfig']
        signlist = self.SMG.GetSignList()
        self.boxmodule.addItems(list(zip(*signlist))[1])
        seq = self.SMG.FindSignList(curconfig['ModuleKey'])[0]
        self.boxmodule.setCurrentIndex(seq)
        self.skmodule.setCurrentIndex(seq)
        self.SMG.LoadWindow(curconfig)
        self.picicon.setIcon(signlist[seq][4])

    def LoadSubConfig(self, num: int):
        nk, name = env.value["SubConfigs"][num][1:]
        _path = f"personal/config/{nk+name}.json"
        with open(_path, 'r', encoding='utf-8') as c:
            _config = json.load(c)
        if self.SMG.CheckConfig(_config, True):
            return True
        return False
