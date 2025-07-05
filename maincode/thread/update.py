from maincode.tools.main import (GetTracebackInfo, logger, CmdRun)
from os import path, makedirs, remove
from maincode.main.maingroup import sg


def update(self):
    try:
        from urllib.request import urlretrieve
        if not path.exists("cache"):
            makedirs("cache")
        temp_path = path.join(sg.info.Workdir, "cache")
        load_path = path.join(temp_path, self.para["name"])
        urlretrieve(self.para["browser_download_url"], load_path)
    except Exception as e:
        sg.TaskError = False
        _str = GetTracebackInfo(e)
        logger.error(_str + "更新异常：下载异常")
        return
    else:
        self.send("下载完成")
    # noinspection PyBroadException
    try:
        from shutil import unpack_archive
        unpack_archive(load_path, temp_path)
    except Exception as e:
        sg.TaskError = False
        _str = GetTracebackInfo(e)
        logger.error(_str + "更新异常：解压异常")
        return
    else:
        self.send("解压完成")
    # noinspection PyBroadException
    try:
        from shutil import copytree
        extract_folder = path.splitext(load_path)[0]
        cover_folder = sg.info.Workdir
        copytree(extract_folder, cover_folder, dirs_exist_ok=True)
    except Exception as e:
        sg.TaskError = False
        _str = GetTracebackInfo(e)
        logger.error(_str + "更新异常：替换异常")
        return
    else:
        self.send("替换完成")
    # noinspection PyBroadException
    try:
        from shutil import rmtree
        remove(load_path)
        rmtree(extract_folder)
    except Exception as e:
        sg.TaskError = False
        _str = GetTracebackInfo(e)
        logger.error(_str + "更新异常：删除临时文件异常")
    else:
        self.send("删除临时文件完成,准备重启")
        logger.info("更新成功")
        CmdRun("start "" /d \"personal/script\" start-SGA.vbs")
        exit()
