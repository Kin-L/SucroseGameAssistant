from PyQt5.QtCore import QThread, pyqtSignal
from main.mainwindows import main_windows as mw
from traceback import format_exc
from os.path import join, splitext
from os import remove
from requests import get
from json import loads
from time import sleep
from sys import exit as sysexit
from main.tools.environment import env, logger
from subprocess import run as cmd_run


class Update(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui):  # mode true:集成运行 false:独立运行
        super(Update, self).__init__()
        self.ui = ui
        env.version = ui.state["version"]
        self.mode = None
        self.download = None

    def run(self):
        if self.mode == 0:
            self.check()
        elif self.mode == 1:
            self.load_add_update()
        elif self.mode == 2:  # 自动检查并更新
            sleep(0.5)
            if self.check():
                self.load_add_update()
            mw.overall.button_check.setEnabled(True)

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
                    if env.version == new_version:
                        mw.indicate(f"已为最新版本: {env.version}", 3)
                        if not self.mode:
                            mw.overall.button_check.setEnabled(True)
                        return 0
                    else:
                        mw.indicate(f"发现新版本: {env.version} -> {new_version}")
                        mw.indicate(f"可通过此链接进行手动更新: https://gitee.com/huixinghen/SucroseGameAssistant/releases")
                        mw.indicate(data["body"], 3)
                        assets = data["assets"]
                        for d in assets:
                            if "replace" in d["name"]:
                                self.download = d

                        if not self.mode:
                            mw.overall.button_check.hide()
                            mw.overall.button_update.show()
                            mw.overall.button_update.setEnabled(True)
                        return 1
                elif i < 2:
                    sleep(2)
                else:
                    raise ConnectionError("检查更新异常")
        except Exception:
            mw.indicate("检查更新异常", 3)
            logger.error("检查更新异常:\n%s\n" % format_exc())
            return 0

    def load_add_update(self):
        mw.indicate("开始更新,更新完成后将自动重启SGA")
        # noinspection PyBroadException
        try:
            from urllib.request import urlretrieve
            temp_path = join(env.workdir, "cache")
            load_path = join(temp_path, self.download["name"])
            urlretrieve(self.download["browser_download_url"], load_path)
            mw.indicate("下载完成")
        except Exception:
            mw.sendbox("下载异常")
            logger.error("下载异常:\n%s\n" % format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import unpack_archive
            unpack_archive(load_path, temp_path)
        except Exception:
            mw.sendbox("解压异常")
            logger.error("解压异常:\n%s\n" % format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import copytree
            extract_folder = splitext(load_path)[0]
            cover_folder = env.workdir
            copytree(extract_folder, cover_folder, dirs_exist_ok=True)
        except Exception:
            mw.sendbox("替换异常")
            logger.error("替换异常:\n%s\n" % format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import rmtree
            remove(load_path)
            rmtree(extract_folder)
        except Exception:
            mw.sendbox("删除临时文件异常")
            logger.error("删除临时文件异常:\n%s\n" % format_exc())
            return 0
        # 弹窗重启
        mw.indicate("更新成功,进行重启", 3)
        if self.mode == 1:
            mw.overall.button_check.show()
            mw.overall.button_check.setEnabled(True)
            mw.overall.button_update.hide()
        cmd_run("start "" /d \"personal/bat\" restart.vbs", shell=True)
        sysexit(0)
        
            