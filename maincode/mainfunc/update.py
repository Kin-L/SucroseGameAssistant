from maincode.tools.system.other import CmdRun
from maincode.tools.system.notification import GetTracebackInfo
from maincode.tools.core.logger import logger
from os import path, makedirs, remove
from maincode.config.configctrl import scc
from urllib.request import urlretrieve
from shutil import unpack_archive, copytree, rmtree
from PyQt5.QtWidgets import QApplication


def update(self):
    try:
        # 确保缓存目录存在
        if not path.exists("cache"):
            makedirs("cache")

        temp_path = path.join(scc.info.Workdir, "cache")
        safe_filename = path.basename(self.para["name"])
        load_path = path.join(temp_path, safe_filename)

        # 下载文件
        urlretrieve(self.para["browser_download_url"], load_path)
        self.send("下载完成")

        # 解压文件
        unpack_archive(load_path, temp_path)
        self.send("解压完成")

        # 替换文件
        extract_folder = path.splitext(load_path)[0]
        cover_folder = scc.info.Workdir
        copytree(extract_folder, cover_folder, dirs_exist_ok=True)
        self.send("替换完成")

        # 清理临时文件
        remove(load_path)
        rmtree(extract_folder)
        self.send("删除临时文件完成,准备重启")
        logger.info("更新成功")

        # 重启程序
        CmdRun("start \"\" /d \"personal/script\" start-SGA.vbs")
        app = QApplication.instance()
        if app:
            app.quit()
    except Exception as e:
        scc.TaskError = False
        logger.error("更新异常：%s", GetTracebackInfo(e))
        return
