from ..timer.main import SGAMain4
from .widget import ModuleWidget
from maincode.main.maingroup import sg
from maincode.tools.main import logger, GetTracebackInfo
from os import path, remove, replace


class SGAMain5(SGAMain4):
    def __init__(self, userui):
        super().__init__(userui)
        if self.loadui:
            self.module = ModuleWidget()
            self.mainwidget.sksetting.addWidget(self.module)
            self.mainwidget.sksetting.setCurrentIndex(1)
            for widget in sg.modules.GetWidgets():
                self.module.skmodule.addWidget(widget)

            if sg.mainconfig.ConfigLock:
                self.module.btconfiglock.show()
                self.module.btconfigunlock.hide()
                self.module.btconfigdelete.hide()
                self.module.btconfigadd.show()
            else:
                self.module.btconfiglock.hide()
                self.module.btconfigunlock.show()
                self.module.btconfigdelete.show()
                self.module.btconfigadd.hide()
            self.module.ecbconfig.addItems(sg.subconfig.GetFilesT()[1])
            self.module.boxmodule.addItems(sg.modules.GetInfosT()[0])

            item = sg.subconfig.FindItem(sg.mainconfig.ConfigKey)
            if item:
                seq = item[-1]
            else:
                seq = 0
                sg.mainconfig.ConfigKey = str(sg.subconfig.filelist[0][0])
            self.module.ecbconfig.setCurrentIndex(seq)
            self.module.boxmodule.currentIndexChanged.connect(self.ChangePage)
            self.LoadSet(sg.mainconfig.CurrentConfig)

            self.module.btconfiglock.clicked.connect(lambda: self.setlock(False))
            self.module.btconfigunlock.clicked.connect(lambda: self.setlock(True))
            self.module.btconfigdelete.clicked.connect(self.configdelete)
            self.module.btconfigadd.clicked.connect(self.configadd)
            self.module.btconfigedit.clicked.connect(self.ReadyToRename)
            self.module.btconfigfinish.clicked.connect(self.configrename)
            self.module.ecbconfig.currentIndexChanged.connect(self.configchange)

    def setlock(self, lock: bool):
        try:
            if lock:
                self.module.btconfiglock.show()
                self.module.btconfigunlock.hide()
                self.module.btconfigdelete.hide()
                self.module.btconfigadd.show()
                sg.mainconfig.ConfigLock = True
                self.configchange()
            else:
                self.module.btconfiglock.hide()
                self.module.btconfigunlock.show()
                self.module.btconfigdelete.show()
                self.module.btconfigadd.hide()
                sg.mainconfig.ConfigLock = False
            sg.mainconfig.ConfigLock = lock
        except Exception as e:
            _str = GetTracebackInfo(e) + "切换锁定流程异常"
            logger.error(_str)
            self.infoAdd(f"切换锁定流程异常")

    def configchange(self):
        try:
            num = self.module.ecbconfig.currentIndex()
            if sg.mainconfig.ConfigLock:
                _config = sg.subconfig.Read(num)
                if sg.modules.CheckConfig(_config):
                    name = _config["ConfigName"]
                    configkey = _config["ConfigKey"]
                    self.infoHead()
                    self.infoAdd(f"载入配置：{configkey}{name}")
                    self.infoEnd()
                    self.LoadSet(_config)
            sg.mainconfig.ConfigKey = sg.subconfig.filelist[num][0]
        except Exception as e:
            _str = GetTracebackInfo(e) + "子配置变换流程异常"
            logger.error(_str)
            self.infoAdd(f"子配置变换流程异常")

    def ChangePage(self):
        try:
            seq = self.module.boxmodule.currentIndex()
            self.module.skmodule.setCurrentIndex(seq)
            _path = sg.modules.GetInfosT()[-1][seq]
            self.module.picicon.setIcon(_path)
            if not sg.modules.WidgetsLoad[seq]:
                sg.modules.GetWidgets()[seq].LoadWidget()
                sg.modules.WidgetsLoad[seq] = True
        except Exception as e:
            _str = GetTracebackInfo(e) + "切换模块子页面流程异常"
            logger.error(_str)
            self.infoAdd(f"切换模块子页面流程异常")

    def LoadSet(self, subconfig: dict):
        try:
            modulekey = subconfig["ModuleKey"]
            subconfig.update(sg.mainconfig.OtherConfig)
            seq = sg.modules.FindItem(modulekey)[-1]
            self.module.boxmodule.setDisabled(True)
            self.module.boxmodule.setCurrentIndex(seq)
            self.module.skmodule.setCurrentIndex(seq)
            if not sg.modules.WidgetsLoad[seq]:
                sg.modules.GetWidgets()[seq].LoadWidget()
                sg.modules.WidgetsLoad[seq] = True
            self.module.boxmodule.setDisabled(False)
            sg.info.OtherConfig = sg.mainconfig.OtherConfig
            sg.modules.GetWidgets()[seq].SetWidget(subconfig)
            _path = sg.modules.GetInfosT()[-1][seq]
            self.module.picicon.setIcon(_path)
            self.module.boxmodule.setCurrentIndex(seq)
            # self.module.skmodule.setCurrentIndex(seq)
        except Exception as e:
            _str = GetTracebackInfo(e) + "载入子配置流程异常"
            logger.error(_str)
            self.infoAdd(f"载入子配置流程异常")

    def configdelete(self):
        try:
            num = self.module.ecbconfig.currentIndex()
            ck, name, mk = sg.subconfig.GetFiles()[num]
            filepath = f"personal/config/{ck}{name}.json"
            del sg.subconfig.filelist[num]
            self.module.ecbconfig.removeItem(num)
            remove(filepath)
            _tw = self.overall.timer.wdtime
            nn = num+1
            for i in range(10):
                getattr(_tw, f"text{i}").removeItem(nn)
            if sg.modules.WidgetsLoad[0]:
                _wdlist = sg.modules.GetWidgets()[0].wdlist
                for i in range(1, 9):
                    getattr(_wdlist, f"task0{i}").removeItem(nn)
            self.infoHead()
            self.infoAdd(f"删除配置：{ck}{name}")
            self.infoEnd()
        except Exception as e:
            _str = GetTracebackInfo(e) + "子配置删除流程异常"
            logger.error(_str)
            self.infoAdd(f"子配置删除流程异常")

    def configadd(self):
        try:
            import random
            default = sg.modules.GetConfig(0).model_dump()
            while 1:
                key = f"{random.randint(0, 9999):04d}"
                if key in sg.subconfig.GetFilesT()[0]:
                    continue
                else:
                    break
            default['ConfigKey'] = key
            sg.subconfig.Save(default)
            self.module.ecbconfig.addItem("默认配置")
            sg.subconfig.filelist.append([key, "默认配置", 0])
            self.module.ecbconfig.setCurrentIndex(len(sg.subconfig.filelist)-1)
            _tw = self.overall.timer.wdtime
            for i in range(10):
                getattr(_tw, f"text{i}").addItem("默认配置")
            if sg.modules.WidgetsLoad[0]:
                _wdlist = sg.modules.GetWidgets()[0].wdlist
                for i in range(1, 9):
                    getattr(_wdlist, f"task0{i}").addItem("默认配置")
            self.infoHead()
            self.infoAdd(f"新建配置")
            self.infoEnd()
        except Exception as e:
            _str = GetTracebackInfo(e) + "子配置新增流程异常"
            logger.error(_str)
            self.infoAdd(f"子配置新增流程异常")

    def ReadyToRename(self):
        try:
            _text = self.module.ecbconfig.currentText()
            self.module.ecbconfig.hide()
            self.module.edlconfig.setText(_text)
            self.module.edlconfig.show()
            self.module.btconfigfinish.show()
            self.module.btconfigedit.hide()
            self.module.btconfigunlock.setDisabled(True)
            self.module.btconfiglock.setDisabled(True)
            self.module.btstart.setDisabled(True)
            self.module.btpause.setDisabled(True)
            self.module.btconfigadd.setDisabled(True)
            self.module.btconfigdelete.setDisabled(True)
        except Exception as e:
            _str = GetTracebackInfo(e) + "子配置准备更名流程异常"
            logger.error(_str)
            self.infoAdd(f"子配置准备更名流程异常")

    def configrename(self):
        try:
            num = self.module.ecbconfig.currentIndex()
            oldname = self.module.ecbconfig.currentText()
            newname = self.module.edlconfig.text()
            if newname != oldname:
                _dict = sg.subconfig.Read(num)
                self.module.ecbconfig.setItemText(num, newname)
                fl = sg.subconfig.GetFiles()
                fl[num][1] = newname
                sg.subconfig.filelist = fl
                configkey = sg.mainconfig.ConfigKey
                oldpath = path.join(sg.info.Workdir, f"personal/config/{configkey}{oldname}.json")
                newpath = path.join(sg.info.Workdir, f"personal/config/{configkey}{newname}.json")

                _dict["ConfigName"] = newname
                replace(oldpath, newpath)
                sg.subconfig.Save(_dict)
                _tw = self.overall.timer.wdtime
                old_index = num + 1
                for i in range(10):
                    getattr(_tw, f"text{i}").setItemText(old_index, newname)
                if sg.modules.WidgetsLoad[0]:
                    _wdlist = sg.modules.GetWidgets()[0].wdlist
                    for i in range(1, 9):
                        getattr(_wdlist, f"task0{i}").setItemText(old_index, newname)
                self.infoHead()
                self.infoAdd(f"重命名配置：{configkey}")
                self.infoAdd(f"  {oldname} -> {newname}", False)
                self.infoEnd()
            self.module.edlconfig.hide()
            self.module.ecbconfig.show()
            self.module.btconfigfinish.hide()
            self.module.btconfigedit.show()
            self.module.btconfigunlock.setEnabled(True)
            self.module.btconfiglock.setEnabled(True)
            self.module.btstart.setEnabled(True)
            self.module.btpause.setEnabled(True)
            self.module.btconfigadd.setEnabled(True)
            self.module.btconfigdelete.setEnabled(True)
        except Exception as e:
            _str = GetTracebackInfo(e) + "子配置确认更名流程异常"
            logger.error(_str)
            self.infoAdd(f"子配置确认更名流程异常")
