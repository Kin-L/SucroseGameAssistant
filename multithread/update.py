# coding:utf-8
from PyQt5.QtCore import QThread, pyqtSignal
from tools.environment import *
import traceback
import os


class Update(QThread):
    send = pyqtSignal(str, int, bool, bool)

    def __init__(self, ui):  # mode true:集成运行 false:独立运行
        super(Update, self).__init__()
        self.ui = ui
        self.version = ui.state["version"]
        self._url = ("https://github.moeyy.xyz/"
                     "https://github.com/Kin-L/SGA-Sucrose_Game_Assistant/"
                     "releases/download/%s/%s.zip")

    def run(self):
        wait(500)
        self.check()
        self.ui.overall.button_update.setEnabled(True)

    def check(self):
        # noinspection PyBroadException
        try:
            cur_ver = self.version
            cur_ver_num = cur_ver.split(" ")[-1]
            new_ver_num = self.check_update(cur_ver_num)
            if new_ver_num:
                self.indicate(f"发现新版本: {cur_ver_num} -> {new_ver_num}")
            else:
                self.indicate(f"已为最新版本: {cur_ver_num}", 3)
                return 1
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
            temp_name = os.path.basename(new_ver_num + "_replace.zip")
            load_path = os.path.join(temp_path, temp_name)

            urlretrieve(self._url % (new_ver_num, new_ver_num + "_replace"), load_path)
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
        import requests # cur_ver = "2.0.0"   ver_lit = [2, 0, 0]
        _list = []
        for i in cur_ver.split("."):
            _list += [int(i)]
        _cur = _list.copy()

        def int_to_str(int_lit):
            a = []
            for s in int_lit:
                a += [str(s)]
            return '.'.join(a)
        while 1:
            _l = _list.copy()
            _l[-1] = _l[-1] + 1
            _str = int_to_str(_l)
            r = requests.get(self._url % (_str, _str + "_replace"), timeout=timeout)
            if r.status_code == 200:
                print(_l, _str, 2)
                _list = _l
                continue
            _l = _list.copy()
            _l[-2] = _l[-2] + 1
            _l = _l[:-1]
            _str = int_to_str(_l)
            r = requests.get(self._url % (_str, _str + "_replace"), timeout=timeout)
            if r.status_code == 200:
                _list = _l
                continue
            _l = _list.copy()
            _l += [1]
            _str = int_to_str(_l)
            r = requests.get(self._url % (_str, _str + "_replace"), timeout=timeout)
            if r.status_code == 200:
                _list = _l
                continue
            print(_cur, _list)
            if _cur == _list:
                return False
            else:
                return int_to_str(_list)
