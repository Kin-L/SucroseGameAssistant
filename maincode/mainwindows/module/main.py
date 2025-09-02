from .widget import ModuleWidget
from maincode.config.configctrl import scc
from ...tools.system.notification import GetTracebackInfo
from ...tools.core.logger import logger
from os import path, remove, replace
from maincode.mainwindows.mainwindow import SGAQMainWindow
import random
_Range10 = range(10)
_Range9 = range(1, 9)


class SGAModule:
    def __init__(self, SQMW: SGAQMainWindow):
        self.infoHead = SQMW.infoHead
        self.infoAdd = SQMW.infoAdd
        self.infoEnd = SQMW.infoEnd
        self.wdtime = SQMW.overall.widget.timer.widgets.wdtime
        self.widget = ModuleWidget()
        for widget in scc.modules.GetWidgets():
            self.widget.skmodule.addWidget(widget)

        self._update_lock_ui(scc.mc.ConfigLock)
        self.widget.ecbconfig.addItems(scc.sc.GetFilesT()[1])
        self.widget.boxmodule.addItems(scc.modules.GetInfosT()[0])

        item = scc.sc.FindItem(scc.mc.ConfigKey)
        if item:
            seq = item[-1]
        else:
            seq = 0
            scc.mc.ConfigKey = str(scc.sc.filelist[0][0])
        self.widget.ecbconfig.setCurrentIndex(seq)
        self.widget.boxmodule.currentIndexChanged.connect(self.ChangePage)
        self.LoadSet(scc.mc.CurrentConfig)

        self.widget.btconfiglock.clicked.connect(lambda: self.setlock(False))
        self.widget.btconfigunlock.clicked.connect(lambda: self.setlock(True))
        self.widget.btconfigdelete.clicked.connect(self.configdelete)
        self.widget.btconfigadd.clicked.connect(self.configadd)
        self.widget.btconfigedit.clicked.connect(self.ReadyToRename)
        self.widget.btconfigfinish.clicked.connect(self.configrename)
        self.widget.ecbconfig.currentIndexChanged.connect(self.configchange)

    def _update_lock_ui(self, locked: bool):
        """更新锁定状态下的UI显示"""
        if locked:
            self.widget.btconfiglock.show()
            self.widget.btconfigunlock.hide()
            self.widget.btconfigdelete.hide()
            self.widget.btconfigadd.show()
        else:
            self.widget.btconfiglock.hide()
            self.widget.btconfigunlock.show()
            self.widget.btconfigdelete.show()
            self.widget.btconfigadd.hide()

    def _disable_buttons(self, disable: bool):
        """统一控制按钮启用/禁用"""
        buttons = [
            self.widget.btconfigunlock,
            self.widget.btconfiglock,
            self.widget.btstart,
            self.widget.btpause,
            self.widget.btconfigadd,
            self.widget.btconfigdelete,
        ]
        for btn in buttons:
            btn.setDisabled(disable)

    def setlock(self, lock: bool):
        try:
            self._update_lock_ui(lock)
            scc.mc.ConfigLock = lock
            if lock:
                self.configchange()
        except Exception as e:
            _str = GetTracebackInfo(e) + "切换锁定流程异常"
            logger.error(_str)
            self.infoAdd(f"切换锁定流程异常")

    def configchange(self):
        try:
            num = self.widget.ecbconfig.currentIndex()
            if scc.mc.ConfigLock:
                _config = scc.sc.Read(num)
                if scc.modules.CheckConfig(_config):
                    name = _config["ConfigName"]
                    configkey = _config["ConfigKey"]
                    self.infoHead()
                    self.infoAdd(f"载入配置：{configkey}{name}")
                    self.infoEnd()
                    self.LoadSet(_config)
            scc.mc.ConfigKey = scc.sc.filelist[num][0]
        except Exception as e:
            _str = GetTracebackInfo(e) + "子配置变换流程异常"
            logger.error(_str)
            self.infoAdd(f"子配置变换流程异常")

    def ChangePage(self):
        try:
            seq = self.widget.boxmodule.currentIndex()
            self.widget.skmodule.setCurrentIndex(seq)
            _path = scc.modules.GetInfosT()[-1][seq]
            self.widget.picicon.setIcon(_path)
            if not scc.modules.WidgetsLoad[seq]:
                scc.modules.GetWidgets()[seq].LoadWidget()
                scc.modules.WidgetsLoad[seq] = True
        except Exception as e:
            _str = GetTracebackInfo(e) + "切换模块子页面流程异常"
            logger.error(_str)
            self.infoAdd(f"切换模块子页面流程异常")

    def LoadSet(self, subconfig: dict):
        try:
            modulekey = subconfig["ModuleKey"]
            subconfig.update(scc.mc.OtherConfig)
            seq = scc.modules.FindItem(modulekey)[-1]
            self.widget.boxmodule.setDisabled(True)
            self.widget.boxmodule.setCurrentIndex(seq)
            self.widget.skmodule.setCurrentIndex(seq)
            if not scc.modules.WidgetsLoad[seq]:
                scc.modules.GetWidgets()[seq].LoadWidget()
                scc.modules.WidgetsLoad[seq] = True
            self.widget.boxmodule.setDisabled(False)
            scc.info.OtherConfig = scc.mc.OtherConfig
            scc.modules.GetWidgets()[seq].SetWidget(subconfig)
            _path = scc.modules.GetInfosT()[-1][seq]
            self.widget.picicon.setIcon(_path)
            self.widget.boxmodule.setCurrentIndex(seq)
        except Exception as e:
            _str = GetTracebackInfo(e) + "载入子配置流程异常"
            logger.error(_str)
            self.infoAdd(f"载入子配置流程异常")

    def configdelete(self):
        try:
            num = self.widget.ecbconfig.currentIndex()
            ck, name, mk = scc.sc.GetFiles()[num]
            filepath = path.join("personal/config", f"{ck}{name}.json")
            del scc.sc.filelist[num]
            self.widget.ecbconfig.removeItem(num)
            remove(filepath)
            nn = num + 1
            for i in _Range10:
                getattr(self.wdtime, f"text{i}").removeItem(nn)
            if scc.modules.WidgetsLoad[0]:
                _wdlist = scc.modules.GetWidgets()[0].wdlist
                for i in _Range9:
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
            default = scc.modules.GetConfig(0).model_dump()
            while True:
                key = f"{random.randint(0, 9999):04d}"
                if key not in scc.sc.GetFilesT()[0]:
                    break
            default['ConfigKey'] = key
            scc.sc.Save(default)
            self.widget.ecbconfig.addItem("默认配置")
            scc.sc.filelist.append([key, "默认配置", 0])
            self.widget.ecbconfig.setCurrentIndex(len(scc.sc.filelist) - 1)
            for i in _Range10:
                getattr(self.wdtime, f"text{i}").addItem("默认配置")
            if scc.modules.WidgetsLoad[0]:
                _wdlist = scc.modules.GetWidgets()[0].wdlist
                for i in _Range9:
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
            self._disable_buttons(True)
        except Exception as e:
            _str = GetTracebackInfo(e) + "子配置准备更名流程异常"
            logger.error(_str)
            self.infoAdd(f"子配置准备更名流程异常")

    def configrename(self):
        try:
            num = self.widget.ecbconfig.currentIndex()
            oldname = self.widget.ecbconfig.currentText()
            newname = self.widget.edlconfig.text()
            if not newname.strip():
                self.infoAdd("配置名称不能为空")
                return
            if newname != oldname:
                _dict = scc.sc.Read(num)
                self.widget.ecbconfig.setItemText(num, newname)
                fl = scc.sc.GetFiles()
                fl[num][1] = newname
                scc.sc.filelist = fl
                configkey = scc.mc.ConfigKey
                oldpath = path.join(scc.info.Workdir, "personal/config", f"{configkey}{oldname}.json")
                newpath = path.join(scc.info.Workdir, "personal/config", f"{configkey}{newname}.json")

                _dict["ConfigName"] = newname
                replace(oldpath, newpath)
                scc.sc.Save(_dict)
                old_index = num + 1
                for i in _Range10:
                    getattr(self.wdtime, f"text{i}").setItemText(old_index, newname)
                if scc.modules.WidgetsLoad[0]:
                    _wdlist = scc.modules.GetWidgets()[0].wdlist
                    for i in _Range9:
                        getattr(_wdlist, f"task0{i}").setItemText(old_index, newname)
                self.infoHead()
                self.infoAdd(f"重命名配置：{configkey}")
                self.infoAdd(f"  {oldname} -> {newname}", False)
                self.infoEnd()
            self.widget.edlconfig.hide()
            self.widget.ecbconfig.show()
            self.widget.btconfigfinish.hide()
            self.widget.btconfigedit.show()
            self._disable_buttons(False)
        except Exception as e:
            _str = GetTracebackInfo(e) + "子配置确认更名流程异常"
            logger.error(_str)
            self.infoAdd(f"子配置确认更名流程异常")
            self._disable_buttons(False)
