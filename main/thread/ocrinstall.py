def install_ocr(self):
    # noinspection PyBroadException
    try:
        from urllib.request import urlretrieve
        import requests
        import json
        if not path.exists(r"cache"):
            _path = sme.workdir + "/cache"
            makedirs(_path)
        temp_path = path.join(sme.workdir, "cache")
        temp_name = path.basename(sme.OCR.exe_name + ".zip")
        load_path = path.join(temp_path, temp_name)
        _load = "https://github.moeyy.xyz/"
        response = requests.get(_load, timeout=10)
        if response.status_code == 200:
            urlretrieve(sme.OCR.load_url, load_path)
            smw.indicate("下载完成,开始安装")
        else:
            smw.indicate(f"连接错误(code {response.status_code})")
            raise ValueError(f"连接错误(code {response.status_code})")
    except Exception:
        smw.indicate("下载异常")
        logger.error("下载异常:\n%s\n" % format_exc())
        return False
    # noinspection PyBroadException
    try:
        from shutil import unpack_archive
        unpack_archive(load_path, temp_path)
    except Exception:
        smw.indicate("解压异常")
        logger.error("解压异常:\n%s\n" % format_exc())
        return False
    # noinspection PyBroadException
    try:
        from shutil import copytree
        extract_folder = path.splitext(load_path)[0]
        cover_folder = path.join(sme.workdir, "3rd_package", sme.OCR.exe_name)
        copytree(extract_folder, cover_folder, dirs_exist_ok=True)
    except Exception:
        smw.indicate("替换异常")
        logger.error("替换异常:\n%s\n" % format_exc())
        return False
    # noinspection PyBroadException
    try:
        from shutil import rmtree
        remove(load_path)
        rmtree(extract_folder)
    except Exception:
        smw.indicate("删除临时文件异常")
        logger.error("删除临时文件异常:\n%s\n" % format_exc())
        return False
    # 弹窗重启
    smw.indicate(f"安装成功:{cover_folder}")
    return True