from tools.environment import logger, env
from cpufeature import CPUFeature
import os
import traceback


class OCR:
    def __init__(self):
        if CPUFeature["AVX2"]:
            self.exe_name = "PaddleOCR-json_v.1.3.1(simplify)"
            self.load_url = ""
            self.exe_path = r"3rd_package\PaddleOCR-json_v.1.3.1(simplify)\PaddleOCR-json.exe"
            logger.debug("CPU 支持 AVX2 指令集，使用 PaddleOCR-json")
        else:
            self.exe_name = "RapidOCR-json_v0.2.0(simplify)"
            self.load_url = ""
            self.exe_path = r"3rd_package\RapidOCR-json_v0.2.0(simplify)\RapidOCR-json.exe"
            logger.debug("CPU 不支持 AVX2 指令集，使用 RapidOCR-json")
        if not os.path.isfile(os.path.join(env.workdir, self.exe_path)):
            logger.debug(f"OCR组件未安装，开始下载安装({self.exe_name})")
            logger.debug("下载中...")
            self.install_ocr()
            
    def install_ocr(self):
        # noinspection PyBroadException
        try:
            from urllib.request import urlretrieve
            import tempfile
            temp_path = tempfile.gettempdir()
            temp_name = os.path.basename(self.exe_name + ".zip")
            load_path = os.path.join(temp_path, temp_name)
            urlretrieve(self.load_url, load_path)
            logger.debug("下载完成,开始替换文件")
        except Exception:
            logger.debug("下载异常", 3)
            logger.error("下载异常:\n%s\n" % traceback.format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import unpack_archive
            unpack_archive(load_path, temp_path)
        except Exception:
            logger.debug("解压异常", 3)
            logger.error("解压异常:\n%s\n" % traceback.format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import copytree
            extract_folder = os.path.splitext(load_path)[0]
            cover_folder = os.path.join(env.workdir, "3rd_package")
            copytree(extract_folder, cover_folder, dirs_exist_ok=True)
        except Exception:
            logger.debug("替换异常", 3)
            logger.error("替换异常:\n%s\n" % traceback.format_exc())
            return 0
        # noinspection PyBroadException
        try:
            from shutil import rmtree
            os.remove(load_path)
            rmtree(extract_folder)
        except Exception:
            logger.debug("删除临时文件异常", 3)
            logger.error("删除临时文件异常:\n%s\n" % traceback.format_exc())
            return 0
        # 弹窗重启
        logger.debug(f"安装成功:{self.exe_name}", 3)