# coding:utf-8
from PyQt5.QtCore import QThread, pyqtSignal
from tools.environment import *
import traceback
import os
import requests
import json
import time


class Update(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui):  # mode true:集成运行 false:独立运行
        super(Update, self).__init__()
        self.ui = ui
        self.version = ui.state["version"]

    def run(self):
        wait(500)
        self.check()
        self.ui.overall.button_update.setEnabled(True)

    def check(self):
        # noinspection PyBroadException
        try:
            cur_ver = self.version
            new_ver, data = self.check_update(cur_ver)
            if new_ver == 100:
                self.indicate(f"已为最新版本: {cur_ver}", 3)
                return 1
            elif new_ver == 101:
                raise ConnectionError("新版本信息获取失败")
            elif new_ver == 102:
                raise ConnectionError("下载直链获取失败")
            else:
                self.indicate(f"发现新版本: {cur_ver} -> {new_ver}")
                lanzou = data["lanzou"]
                self.indicate(f"可通过此链接进行手动更新:{lanzou}")
        except Exception:
            self.indicate("检查更新异常", 3)
            logger.error("检查更新异常:\n%s\n" % traceback.format_exc())
            return 0
        self.indicate("开始更新,更新完成后将自动重启SGA")
        # noinspection PyBroadException
        try:
            from urllib.request import urlretrieve
            import tempfile
            temp_path = tempfile.gettempdir()
            load_path = os.path.join(temp_path, data["name"])
            urlretrieve(data["down"], load_path)
            self.indicate("下载完成,开始替换文件")
        except Exception:
            self.indicate("下载异常", 3)
            logger.error("下载异常:\n%s\n" % traceback.format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import unpack_archive
            unpack_archive(load_path, temp_path)
        except Exception:
            self.indicate("解压异常", 3)
            logger.error("解压异常:\n%s\n" % traceback.format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import copytree
            extract_folder = os.path.splitext(load_path)[0]
            cover_folder = env.workdir
            copytree(extract_folder, cover_folder, dirs_exist_ok=True)
        except Exception:
            self.indicate("替换异常", 3)
            logger.error("替换异常:\n%s\n" % traceback.format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import rmtree
            os.remove(load_path)
            rmtree(extract_folder)
        except Exception:
            self.indicate("删除临时文件异常", 3)
            logger.error("删除临时文件异常:\n%s\n" % traceback.format_exc())
            return 0
        # 弹窗重启
        self.indicate("更新成功", 3)
        self.ui.panel_restart.widget.show()

    def indicate(self, msg: str, mode=2, his=True, log=True):
        self.send.emit(msg, mode, his, log)

    def check_update(self, cur_ver, timeout=5):
         # cur_ver = "2.0.0"   ver_lit = [2, 0, 0]
        url = "https://gitee.com/huixinghen/sga_sucrose_game_assistant/raw/master/version.json"
        
        for i in range(3):
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = json.loads(response.text)
                new_ver, new_url = data["version"], data["url"]
                if cur_ver == new_ver:
                    return 100, None
                else:
                    break
            elif i < 2:
                time.sleep(2)
            else:
                return 101, None
        _url = f"https://api.7585.net.cn/lanzou/api.php?url={new_url}"
        for i in range(3):
            response = requests.get(_url, timeout=10)
            if response.status_code == 200:
                data = json.loads(response.text)
                data["lanzou"] = new_url
                return new_ver, data
            elif i < 2:
                time.sleep(2)
            else:
                return 102, None
            