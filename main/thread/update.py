from main.mainwindows import smw
from traceback import format_exc
from os.path import join, splitext
from os import remove
from requests import get
from json import loads
from time import sleep
from sys import exit as sysexit
from main.mainenvironment import sme, logger
from subprocess import run as cmd_run


def check_update():
    smw.sendbox(mode=1)
    # noinspection PyBroadException
    try:  # cur_ver = "2.0.0"   ver_lit = [2, 0, 0]
        url = "https://gitee.com/api/v5/repos/huixinghen/SucroseGameAssistant/releases/latest"
        for i in range(3):
            response = get(url, timeout=10)
            if response.status_code == 200:
                data = loads(response.text)
                _new_version = data["tag_name"]
                if sme.version == _new_version:
                    smw.indicate(f"已为最新版本: {sme.version}")
                    smw.sendbox(mode=3)
                    return False
                else:
                    smw.indicate(f"发现新版本: {sme.version} -> {_new_version}")
                    smw.indicate(f"可通过此链接进行手动更新: https://gitee.com/huixinghen/SucroseGameAssistant/releases")
                    smw.indicate(data["body"])
                    assets = data["assets"]
                    for d in assets:
                        if "replace" in d["name"]:
                            sme.download = d
                            return True
            sleep(2)
        raise ConnectionError("检查更新异常")
    except Exception:
        smw.indicate("检查更新异常")
        logger.error("检查更新异常:\n%s\n" % format_exc())
        smw.sendbox(mode=3)
        return False


def update_procedure():
    smw.indicate("开始更新,更新完成后将自动重启SGA")
    # noinspection PyBroadException
    try:
        from urllib.request import urlretrieve
        temp_path = join(sme.workdir, "cache")
        load_path = join(temp_path, sme.download["name"])
        urlretrieve(sme.download["browser_download_url"], load_path)
        smw.indicate("下载完成")
    except Exception:
        smw.sendbox("下载异常")
        logger.error("下载异常:\n%s\n" % format_exc())
        smw.sendbox(mode=3)
        return False
    # noinspection PyBroadException
    try:
        from shutil import unpack_archive
        unpack_archive(load_path, temp_path)
    except Exception:
        smw.sendbox("解压异常")
        logger.error("解压异常:\n%s\n" % format_exc())
        smw.sendbox(mode=3)
        return False
    # noinspection PyBroadException
    try:
        from shutil import copytree
        extract_folder = splitext(load_path)[0]
        cover_folder = sme.workdir
        copytree(extract_folder, cover_folder, dirs_exist_ok=True)
    except Exception:
        smw.sendbox("替换异常")
        logger.error("替换异常:\n%s\n" % format_exc())
        smw.sendbox(mode=3)
        return False
    # noinspection PyBroadException
    try:
        from shutil import rmtree
        remove(load_path)
        rmtree(extract_folder)
    except Exception:
        smw.sendbox("删除临时文件异常")
        logger.error("删除临时文件异常:\n%s\n" % format_exc())
        smw.sendbox(mode=3)
        return False
    # 弹窗重启
    smw.indicate("更新成功,进行重启")
    smw.sendbox(mode=3)
    cmd_run("start "" /d \"personal/bat\" restart.vbs", shell=True)
    sysexit(0)
    
            