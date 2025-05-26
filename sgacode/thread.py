from PyQt5.QtCore import QObject, pyqtSignal, pyqtBoundSignal
from sgacode.configclass import SGAMainConfig
from sgacode.ui.module.moduleclass import SGAModuleGroup
from sgacode.tools.main import (GetTracebackInfo, SendMessageBox,
                                logger, env, CmdRun)
from time import sleep, localtime
from typing import Optional
from requests import get
from json import loads
from os import path, makedirs, remove


class SGAMainThread(QObject):
    """
    info: 发送信息到指示栏（str)；
          默认在信息前添加时间前缀（默认值True），可使用False取消时间前缀 "%H:%M:%S "
    infoHead: 添加日期行  "%Y-%m-%d"
    infoEnd: 添加结束行 "-" * n
    """
    info: pyqtBoundSignal = pyqtSignal(str, bool)
    infoHead: pyqtBoundSignal = pyqtSignal()
    infoEnd: pyqtBoundSignal = pyqtSignal()

    def __init__(self, smc: SGAMainConfig, smg: SGAModuleGroup):
        super().__init__()
        self.SMC = smc
        self.SMG = smg
        self.triggerflag = False
        self.count = 5
        self.currentday = localtime()[0:3]
        self.downloadurl = {}

    def run(self):
        self.info.emit("")
        errornum = 0
        try:
            if self.SMC['AutoUpdate']:
                self.updatecheck()
        except Exception as err:
            _str = GetTracebackInfo(err)
            logger.error(_str + "检测更新异常")
        while 1:
            try:
                self.cycle()
            except Exception as err:
                errornum += 1
                _str = GetTracebackInfo(err)
                if errornum == 3:
                    SendMessageBox(_str)
                    break
                logger.error(_str + "循环线程异常，2s后重试")
                sleep(2)
            finally:
                errornum = 0
        exit(1)

    def cycle(self):
        if self.triggerflag:  # 手动触发更新，手动启动实时任务
            pass
        else:
            if self.count == 0:
                self.count = 15
                y, M, d, h, m, _, w = localtime()[0:7]
                if self.SMC['AutoUpdate'] and ((y, M, d) != self.currentday):
                    self.updatecheck()
                    h, m, _, w = localtime()[3:7]
                nowtup = ((w+2, (h, m)), (1, (h, m)))
                tc = self.SMC['TimerConfig']
                timetup = tuple(*zip(tc['Execute'], tc['Time']))
                for n, ti in enumerate(timetup):
                    if ti in nowtup:
                        self.taskrun(tc['Name'])
                        self.count = 61-localtime()[5]
                        break
        sleep(1)
        self.count -= 1

    def taskrun(self, name: Optional[str]):
        pass

    def updatecheck(self):
        url = "https://gitee.com/api/v5/repos/huixinghen/SucroseGameAssistant/releases/latest"
        for i in range(3):
            response = get(url, timeout=10)
            if response.status_code == 200:
                data = loads(response.text)
                newversion = data["tag_name"]
                if env.version != newversion:
                    assets = data["assets"]
                    for d in assets:
                        if "replace" in d["name"]:
                            self.downloadurl = d
                            break
        if self.downloadurl:
            self.update()
    
    def update(self):
        try:
            from urllib.request import urlretrieve
            if not path.exists("cache"):
                makedirs("cache")
            temp_path = path.join(env.wordir, "cache")
            load_path = path.join(temp_path, self.downloadurl["name"])
            urlretrieve(self.downloadurl["browser_download_url"], load_path)
        except Exception as e:
            _str = GetTracebackInfo(e)
            logger.error(_str + "更新异常：下载异常")
            return
        # noinspection PyBroadException
        try:
            from shutil import unpack_archive
            unpack_archive(load_path, temp_path)
        except Exception as e:
            _str = GetTracebackInfo(e)
            logger.error(_str + "更新异常：解压异常")
            return
        # noinspection PyBroadException
        try:
            from shutil import copytree
            extract_folder = path.splitext(load_path)[0]
            cover_folder = env.wordir
            copytree(extract_folder, cover_folder, dirs_exist_ok=True)
        except Exception as e:
            _str = GetTracebackInfo(e)
            logger.error(_str + "更新异常：替换异常")
            return
        # noinspection PyBroadException
        try:
            from shutil import rmtree
            remove(load_path)
            rmtree(extract_folder)
        except Exception as e:
            _str = GetTracebackInfo(e)
            logger.error(_str + "更新异常：删除临时文件异常")
        else:
            CmdRun("start "" /d \"personal/bat\" restart.vbs")
            input("111")
            exit()

