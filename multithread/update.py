# coding:utf-8
from PyQt5.QtCore import QThread, pyqtSignal
from tools.environment import *
from traceback import format_exc
from os.path import join, splitext
from subprocess import run as cmd_run
from os import remove
from requests import get
from json import loads
from time import sleep
from sys import exit as sysexit


class Update(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui):  # mode true:集成运行 false:独立运行
        super(Update, self).__init__()
        self.ui = ui
        self.version = ui.state["version"]
        self.mode = None
        self.download = None

    def indicate(self, msg: str, mode=2, his=True, log=True):
        self.send.emit(msg, mode, his, log)

    def run(self):
        if self.mode == 0:
            self.check()
        elif self.mode == 1:
            self.load_add_update()
        elif self.mode == 2:  # 自动检查并更新
            wait(500)
            if self.check():
                self.load_add_update()
            self.ui.overall.button_check.setEnabled(True)

    def check(self):
        # noinspection PyBroadException
        try:
            # cur_ver = "2.0.0"   ver_lit = [2, 0, 0]
            url = "https://gitee.com/api/v5/repos/huixinghen/SucroseGameAssistant/releases/latest"
        
            for i in range(3):
                response = get(url, timeout=10)
                if response.status_code == 200:
                    data = loads(response.text)
                    new_version = data["tag_name"]
                    if self.version == new_version:
                        self.indicate(f"已为最新版本: {self.version}", 3)
                        if not self.mode:
                            self.ui.overall.button_check.setEnabled(True)
                        return 0
                    else:
                        self.indicate(f"发现新版本: {self.version} -> {new_version}")
                        self.indicate(f"可通过此链接进行手动更新: https://gitee.com/huixinghen/SucroseGameAssistant/releases")
                        self.indicate(data["body"], 3)
                        assets = data["assets"]
                        for d in assets:
                            if "replace" in d["name"]:
                                self.download = d

                        if not self.mode:
                            self.ui.overall.button_check.hide()
                            self.ui.overall.button_update.show()
                            self.ui.overall.button_update.setEnabled(True)
                        return 1
                elif i < 2:
                    sleep(2)
                else:
                    raise ConnectionError("检查更新异常")
        except Exception:
            self.indicate("检查更新异常", 3)
            logger.error("检查更新异常:\n%s\n" % format_exc())
            return 0

    def load_add_update(self):
        self.indicate("开始更新,更新完成后将自动重启SGA")
        # noinspection PyBroadException
        try:
            from urllib.request import urlretrieve
            temp_path = join(env.workdir, "cache")
            load_path = join(temp_path, self.download["name"])
            urlretrieve(self.download["browser_download_url"], load_path)
            self.indicate("下载完成")
        except Exception:
            self.indicate("下载异常", 3)
            logger.error("下载异常:\n%s\n" % format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import unpack_archive
            unpack_archive(load_path, temp_path)
        except Exception:
            self.indicate("解压异常", 3)
            logger.error("解压异常:\n%s\n" % format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import copytree
            extract_folder = splitext(load_path)[0]
            cover_folder = env.workdir
            copytree(extract_folder, cover_folder, dirs_exist_ok=True)
        except Exception:
            self.indicate("替换异常", 3)
            logger.error("替换异常:\n%s\n" % format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import rmtree
            remove(load_path)
            rmtree(extract_folder)
        except Exception:
            self.indicate("删除临时文件异常", 3)
            logger.error("删除临时文件异常:\n%s\n" % format_exc())
            return 0
        # 弹窗重启
        self.indicate("更新成功,进行重启", 3)
        if self.mode == 1:
            self.ui.overall.button_check.show()
            self.ui.overall.button_check.setEnabled(True)
            self.ui.overall.button_update.hide()
        cmd_run("start "" /d \"personal/bat\" restart.vbs", shell=True)
        sysexit(0)
        
            