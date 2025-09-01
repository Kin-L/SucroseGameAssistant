from .widget import ModuleWidget
from maincode.config.maingroup import sg
from maincode.tools.main import logger, GetTracebackInfo
from os import path, remove, replace
from maincode.mainwindows.mainwindow import SGAQMainWindow


class SGAModule:
    def __init__(self, SQMW: SGAQMainWindow):
        self.infoHead = SQMW.infoHead
        self.infoAdd = SQMW.infoAdd
        self.infoEnd = SQMW.infoEnd
        self.wdtime = SQMW.overall.widget.timer.widgets.wdtime
        self.widget = ModuleWidget()
        for widget in sg.modules.GetWidgets():
            self.widget.skmodule.addWidget(widget)

        if sg.mainconfig.ConfigLock:
            self.widget.btconfiglock.show()
            self.widget.btconfigunlock.hide()
            self.widget.btconfigdelete.hide()
            self.widget.btconfigadd.show()
        else:
            self.widget.btconfiglock.hide()
            self.widget.btconfigunlock.show()
            self.widget.btconfigdelete.show()
            self.widget.btconfigadd.hide()
        self.widget.ecbconfig.addItems(sg.subconfig.GetFilesT()[1])
        self.widget.boxmodule.addItems(sg.modules.GetInfosT()[0])

        item = sg.subconfig.FindItem(sg.mainconfig.ConfigKey)
        if item:
            seq = item[-1]
        else:
            seq = 0
            sg.mainconfig.ConfigKey = str(sg.subconfig.filelist[0][0])
        self.widget.ecbconfig.setCurrentIndex(seq)
        self.widget.boxmodule.currentIndexChanged.connect(self.ChangePage)
        self.LoadSet(sg.mainconfig.CurrentConfig)

        self.widget.btconfiglock.clicked.connect(lambda: self.setlock(False))
        self.widget.btconfigunlock.clicked.connect(lambda: self.setlock(True))
        self.widget.btconfigdelete.clicked.connect(self.configdelete)
        self.widget.btconfigadd.clicked.connect(self.configadd)
        self.widget.btconfigedit.clicked.connect(self.ReadyToRename)
        self.widget.btconfigfinish.clicked.connect(self.configrename)
        self.widget.ecbconfig.currentIndexChanged.connect(self.configchange)

    def setlock(self, lock: bool):
        try:
            if lock:
                self.widget.btconfiglock.show()
                self.widget.btconfigunlock.hide()
                self.widget.btconfigdelete.hide()
                self.widget.btconfigadd.show()
                sg.mainconfig.ConfigLock = True
                self.configchange()
            else:
                self.widget.btconfiglock.hide()
                self.widget.btconfigunlock.show()
                self.widget.btconfigdelete.show()
                self.widget.btconfigadd.hide()
                sg.mainconfig.ConfigLock = False
            sg.mainconfig.ConfigLock = lock
        except Exception as e:
            _str = GetTracebackInfo(e) + "切换锁定流程异常"
            logger.error(_str)
            self.infoAdd(f"切换锁定流程异常")

    def configchange(self):
        try:
            num = self.widget.ecbconfig.currentIndex()
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
            seq = self.widget.boxmodule.currentIndex()
            self.widget.skmodule.setCurrentIndex(seq)
            _path = sg.modules.GetInfosT()[-1][seq]
            self.widget.picicon.setIcon(_path)
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
            self.widget.boxmodule.setDisabled(True)
            self.widget.boxmodule.setCurrentIndex(seq)
            self.widget.skmodule.setCurrentIndex(seq)
            if not sg.modules.WidgetsLoad[seq]:
                sg.modules.GetWidgets()[seq].LoadWidget()
                sg.modules.WidgetsLoad[seq] = True
            self.widget.boxmodule.setDisabled(False)
            sg.info.OtherConfig = sg.mainconfig.OtherConfig
            sg.modules.GetWidgets()[seq].SetWidget(subconfig)
            _path = sg.modules.GetInfosT()[-1][seq]
            self.widget.picicon.setIcon(_path)
            self.widget.boxmodule.setCurrentIndex(seq)
            # self.module.skmodule.setCurrentIndex(seq)
        except Exception as e:
            _str = GetTracebackInfo(e) + "载入子配置流程异常"
            logger.error(_str)
            self.infoAdd(f"载入子配置流程异常")

    def configdelete(self):
        try:
            num = self.widget.ecbconfig.currentIndex()
            ck, name, mk = sg.subconfig.GetFiles()[num]
            filepath = f"personal/config/{ck}{name}.json"
            del sg.subconfig.filelist[num]
            self.widget.ecbconfig.removeItem(num)
            remove(filepath)
            nn = num+1
            for i in range(10):
                getattr(self.wdtime, f"text{i}").removeItem(nn)
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
            self.widget.ecbconfig.addItem("默认配置")
            sg.subconfig.filelist.append([key, "默认配置", 0])
            self.widget.ecbconfig.setCurrentIndex(len(sg.subconfig.filelist) - 1)
            for i in range(10):
                getattr(self.wdtime, f"text{i}").addItem("默认配置")
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
            _text = self.widget.ecbconfig.currentText()
            self.widget.ecbconfig.hide()
            self.widget.edlconfig.setText(_text)
            self.widget.edlconfig.show()
            self.widget.btconfigfinish.show()
            self.widget.btconfigedit.hide()
            self.widget.btconfigunlock.setDisabled(True)
            self.widget.btconfiglock.setDisabled(True)
            self.widget.btstart.setDisabled(True)
            self.widget.btpause.setDisabled(True)
            self.widget.btconfigadd.setDisabled(True)
            self.widget.btconfigdelete.setDisabled(True)
        except Exception as e:
            _str = GetTracebackInfo(e) + "子配置准备更名流程异常"
            logger.error(_str)
            self.infoAdd(f"子配置准备更名流程异常")

    def configrename(self):
        try:
            num = self.widget.ecbconfig.currentIndex()
            oldname = self.widget.ecbconfig.currentText()
            newname = self.widget.edlconfig.text()
            if newname != oldname:
                _dict = sg.subconfig.Read(num)
                self.widget.ecbconfig.setItemText(num, newname)
                fl = sg.subconfig.GetFiles()
                fl[num][1] = newname
                sg.subconfig.filelist = fl
                configkey = sg.mainconfig.ConfigKey
                oldpath = path.join(sg.info.Workdir, f"personal/config/{configkey}{oldname}.json")
                newpath = path.join(sg.info.Workdir, f"personal/config/{configkey}{newname}.json")

                _dict["ConfigName"] = newname
                replace(oldpath, newpath)
                sg.subconfig.Save(_dict)
                old_index = num + 1
                for i in range(10):
                    getattr(self.wdtime, f"text{i}").setItemText(old_index, newname)
                if sg.modules.WidgetsLoad[0]:
                    _wdlist = sg.modules.GetWidgets()[0].wdlist
                    for i in range(1, 9):
                        getattr(_wdlist, f"task0{i}").setItemText(old_index, newname)
                self.infoHead()
                self.infoAdd(f"重命名配置：{configkey}")
                self.infoAdd(f"  {oldname} -> {newname}", False)
                self.infoEnd()
            self.widget.edlconfig.hide()
            self.widget.ecbconfig.show()
            self.widget.btconfigfinish.hide()
            self.widget.btconfigedit.show()
            self.widget.btconfigunlock.setEnabled(True)
            self.widget.btconfiglock.setEnabled(True)
            self.widget.btstart.setEnabled(True)
            self.widget.btpause.setEnabled(True)
            self.widget.btconfigadd.setEnabled(True)
            self.widget.btconfigdelete.setEnabled(True)
        except Exception as e:
            _str = GetTracebackInfo(e) + "子配置确认更名流程异常"
            logger.error(_str)
            self.infoAdd(f"子配置确认更名流程异常")
