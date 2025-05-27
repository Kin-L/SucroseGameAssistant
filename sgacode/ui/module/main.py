from os import path, remove, rename
from sgacode.ui.control import (Button, Stack, Combobox,
                                PicButton, StateSigh)
from qfluentwidgets import EditableComboBox
from PyQt5.QtWidgets import QWidget
from sgacode.tools.sgagroup import sg


# 模组设置窗口
class ModuleWindow(QWidget):
    def __init__(self):
        super().__init__()
        # 配置切换列表
        self.ecbconfig = EditableComboBox(self)
        self.ecbconfig.setGeometry(40, 0, 215, 35)
        self.ecbconfig.addItems(sg.subconfig.GetFileListT()[2])
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
        self.boxmodule.addItems(sg.subconfig.GetSignListT()[0])
        # 图标标签
        defaultpath = "resources/main/SGA/default.png"
        self.picicon = PicButton(self, (525, 475, 100, 100), defaultpath, (98, 98))
        # 状态指示
        self.statesigh = StateSigh(self, (526, 440, 100, 40))

    def configdelete(self):
        num = self.boxmodule.currentIndex()
        ol = sg.subconfig.GetFileList()
        filepath = f"personal/config/{ol[num][0]}{ol[num][2]}.json"
        onl = sg.subconfig.GetFileListT()[2]
        sg.subconfig.SetFileList(ol[:num] + ol[num+1:])
        self.boxmodule.clear()
        self.boxmodule.addItems(onl[:num] + onl[num+1:])
        remove(filepath)

    def configadd(self):
        import random
        from sgacode.tools.configclass import ConfigTool
        default = sg.subconfig.GetConfigList()[0].getdefault()
        while 1:
            key = f"{random.randint(0, 9999):04d}"
            if key in sg.subconfig.GetFileListT()[0]:
                continue
            else:
                break
        default['ConfigKey'] = key
        ConfigTool.save(default)
        self.boxmodule.addItem("默认配置")
        fl = sg.subconfig.GetFileList()
        nfl = fl + [default['ConfigKey'], default['ModuleKey'], default['ConfigName']]
        sg.subconfig.SetFileList(nfl)
        self.boxmodule.setCurrentIndex(len(fl))

    def configrename(self):
        oldname = sg.subconfig.GetFileListT()[2][self.boxmodule.currentIndex()]
        newname = self.boxmodule.currentText()
        num = self.boxmodule.currentIndex()
        fl = sg.subconfig.GetFileList()
        fl[2][num] = newname
        sg.subconfig.SetFileList(fl)
        configkey = sg.mainconfig['ConfigKey']
        if newname != oldname:
            oldpath = path.join(sg.info.workdir,f"personal/config/{configkey}{oldname}.json")
            newpath = path.join(sg.info.workdir,f"personal/config/{configkey}{newname}.json")
            rename(oldpath, newpath)
