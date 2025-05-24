from sgacode.tools.main import (logger, env, gethwnd,
                                checkadmin, sendmessagebox,
                                gettracebackinfo)
from sgacode.tools.myclass import SGAMainConfig
from sgacode.ui.main import SGAQMainWindow
from os import path, makedirs, listdir
from sgacode.ui.control import (Picture, Line, Stack, Widget,
                                PicButton, InfoBox, OverallButton)
import json
from shutil import copyfile
from sys import argv
import keyboard
from time import sleep
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor, QMovie, QPixmap
from sgacode.ui.overall.main import OverallWindow
from sgacode.ui.module.main import ModuleWindow
from sgacode.ui.module.moduleclass import SGAModuleInstances
from typing import Union


class SGAMAIN:
    def __init__(self):
        super().__init__()
        self.SMC = SGAMainConfig()  # 加载主配置信息
        self.LoadSubConfig()  # 加载子配置信息
        self.SmI = SGAModuleInstances()
        if not self.SmI.Class.CheckConfig(self.SMC['CurrentConfig']):
            self.SMC['CurrentConfig'] = self.SmI.Mix.Config.getdefault()
        # 运行路径变化时，基础文件初始化
        if env.workdir != self.SMC["WorkDir"]:
            self.SMC["WorkDir"] = env.workdir
            self.BasisFileInit()

        self.SQMW = SGAQMainWindow()  # 显示窗口初始化界面
        self.ForegroundMainWindow()  # 窗口显现
        self.SMW = Widget()
        self.LoadMainWindow()  # 加载窗口
        self.SQMW.loading.hide()
        self.load_main_connect()  # 加载线程和状态链接
        self.show_main_window()  # 加载线程和状态链接

    @staticmethod
    def LoadSubConfig():
        # 读取子设置信息
        _subconfigs = []
        _configdirpath = "personal/config"
        if not path.exists(_configdirpath):
            makedirs(_configdirpath)
        _listdir = listdir(_configdirpath)
        if _listdir:
            for file in _listdir:
                name, suffix = path.splitext(file)
                seq, name = name[:4], name[4:]
                if suffix == ".json":
                    _path = path.join(_configdirpath, file)
                    with open(_path, 'r', encoding='utf-8') as c:
                        _config = json.load(c)
                        modulekey: Union[int, None] = _config.get("模块", None)
                    if modulekey is not None:
                        allow = True
                        for item in _subconfigs:
                            if seq in item:
                                allow = False
                        if allow:
                            _subconfigs += [[seq, modulekey, name]]
        env.value["SubConfigs"] = _subconfigs  # 储存设置文件信息，文件名和类型

    @staticmethod
    def BasisFileInit():
        cachedir = "cache"
        scdir = "personal/script"
        rstpath = "resources/main/schtasks.json"
        pstpath = "personal/schtasks.json"
        rrspath = "resources/main/script/restart.bat"
        prspath = "personal/script/restart.bat"
        if not path.exists(cachedir):
            makedirs(cachedir)
        if not path.exists(scdir):
            makedirs(scdir)
        with open(rstpath, 'r', encoding='utf-8') as m:
            xml_dir = json.load(m)
        xml_list = xml_dir["part2"]
        xml_list[32] = f"      <Command>{env.workdir}\\SGA.exe</Command>\n"
        xml_list[34] = "      <WorkingDirectory>" + env.workdir + "</WorkingDirectory>\n"
        xml_dir["part2"] = xml_list
        with open(pstpath, 'w', encoding='utf-8') as x:
            json.dump(xml_dir, x, ensure_ascii=False, indent=1)

        f = open(rrspath, 'r', encoding='utf-8')
        start_list = f.readlines()
        f.close()
        start_list[2] = "start /d \"%s\" SGA.exe\n" % env.workdir
        f = open(prspath, 'w', encoding='utf-8')
        f.writelines(start_list)
        f.close()

        f = open("resources/main/script/maacreate.bat", 'r', encoding='ansi')
        bat_list = f.readlines()
        f.close()
        bat_list[1] = f" cd. > \"{env.workdir}/cache/maacomplete.txt\""
        f = open("personal/script/maacreate.bat", 'w', encoding='ansi')
        f.writelines(bat_list)
        f.close()
        
        rstvpath = "resources/main/script/restart.vbs"
        prsv = "personal/script/restart.vbs"
        pss = "personal/script/start-SGA.vbs"
        if not path.exists(prsv):
            copyfile(rstvpath, prsv)
        if not path.exists(pss):
            copyfile(rstvpath, pss)

    def ForegroundMainWindow(self):
        self.SQMW.show()
        env.hwnd = gethwnd(True, "Qt5152QWindowIcon", "砂糖代理")
        if len(argv) <= 1:
            env.foreground()
        elif argv[1] != "True":
            env.foreground()

    def LoadMainWindow(self):
        _mw = self.SMW
        self.SQMW.setCentralWidget(_mw)  # 关键步骤！
        _mw.sksetting = Stack(_mw, (5, 0, 620, 570))
        # 指示图标
        # waitpath = r"resources/main/button/state/wait.png"
        # _mw.picstate = Picture((485, 430, 150, 150), waitpath)
        Line(_mw, (5, 38, 625, 3))
        # 全局/模块 设置按钮
        _mw.btsetting = OverallButton(_mw)
        # 历史信息按钮
        historypath = r"resources/main/button/history.png"
        _mw.bthistory = PicButton(_mw, (555, 0, 35, 35), historypath, (25, 25))
        # 指示信息窗口
        _mw.infobox = InfoBox(_mw)
        # 全局设置窗口
        _mw.overall = OverallWindow()
        _mw.sksetting.addWidget(_mw.overall)
        # # 全局设置窗口
        # _mw.module = ModuleWindow(self.SmI)
        # _mw.sksetting.addWidget(_mw.module)

    def load_main_connect(self):
        pass

    def show_main_window(self):
        pass


try:
    checkadmin()
    env.hwnd = gethwnd(True, "Qt5152QWindowIcon", "砂糖代理")
    if env.hwnd:
        env.foreground()
        exit(0)
    else:
        print("")
        logger.info("================SGA开始启动================")
        # 唤醒屏幕
        keyboard.send("numlock")
        sleep(0.01)
        keyboard.send("numlock")
        env.logger_environment_info()
        # SGA窗口初始化
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
        application = QApplication(argv)
        sgamain = SGAMAIN()
except Exception as e:
    _str = gettracebackinfo(e) + "\nSGA加载失败"
    logger.critical(_str)
    sendmessagebox(_str)
    exit(1)
application.exec_()
logger.info("==================SGA关闭=================\n\n")

if __name__ == "__main__":
    pass
