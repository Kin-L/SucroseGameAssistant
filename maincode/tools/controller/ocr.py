from maincode.tools.core.PPOCR_api import GetOcrApi
from PIL import Image
from io import BytesIO
from os import path
from maincode.config.info import info
from maincode.tools.core.logger import logger
from maincode.tools.system.notification import SendMessageBox, GetTracebackInfo
from maincode.tools.system.process import GetPid, killprocess


class OCRControl:
    def __init__(self):
        self.logger = logger
        self.path = ""
        self.name = "PaddleOCR-json.exe" if info.CpuFeature else "RapidOCR-json.exe"
        self.running = None
        self.isrunning = False

    def clear(self):
        for _ in range(10):
            if v := GetPid(self.name):
                killprocess(v)
            else:
                return True
        self.logger.warning(f"尝试10次仍未成功终止进程 {self.name}")
        return False

    def check(self):
        if info.OcrPath:
            self.path = info.OcrPath
        else:
            self.path = path.join("ocr-json", self.name)
        if self.path and path.exists(self.path) and path.basename(self.path) == self.name:
            return True
        else:
            raise FileExistsError("未找到有效ocr-json.exe文件")

    def enable(self):
        if self.isrunning:
            self.logger.debug("OCR早已启用")
            return True
        else:
            try:
                self.logger.debug("开始初始化OCR...")
                self.running = GetOcrApi(self.path)
                self.isrunning = True
                self.logger.debug("初始化OCR完成")
                return True
            except Exception as e:
                _str = (GetTracebackInfo(e) +
                        (f"初始化OCR失败:{e}\n"
                         f"请尝试重新下载或解压OCR组件\n"
                         f"若 Win7 报错计算机中丢失 VCOMP140.DLL,请安装 VC运行库\n"
                         f"https://aka.ms/vs/17/release/vc_redist.x64.exe"))
                self.logger.error(_str)
                self.running = None
                SendMessageBox(_str)
                return False

    def disable(self):
        if self.isrunning:
            self.running.exit()
            self.isrunning = False
            self.logger.debug("关闭OCR完成")
        else:
            self.logger.debug("OCR早已关闭")

    @staticmethod
    def _convert_result(result):
        if result['code'] != 100:
            return False
        converted_result = []
        for item in result['data']:
            box = item['box']
            text = item['text']
            score = item['score']
            converted_item = [
                [box[0], box[1], box[2], box[3]],
                (text, score)
            ]
            converted_result.append(converted_item)
        return converted_result

    @staticmethod
    def _prepare_image_bytes(image):
        if isinstance(image, Image.Image):
            pass
        elif isinstance(image, str):
            return path.abspath(image), None
        else:  # 默认为 np.ndarray，避免需要import numpy
            image = Image.fromarray(image)
        image_stream = BytesIO()
        image.save(image_stream, format="PNG")
        image_bytes = image_stream.getvalue()
        return None, image_bytes

    def run(self, image):
        try:
            file_path, image_bytes = self._prepare_image_bytes(image)
            if file_path:
                return self.running.run(file_path)
            else:
                return self.running.runBytes(image_bytes)
        except Exception as e:
            self.logger.error(e)
            return r"{}"

    def recognize_single_line(self, image, blacklist=None):
        results = self._convert_result(self.run(image))
        if not results:
            return None
        for item in results:
            line_text, score = item[1]
            if blacklist and line_text in blacklist:
                continue
            return line_text, score
        return None

    def output(self, image):
        file_path, image_bytes = self._prepare_image_bytes(image)
        if file_path:
            result = self.running.run(file_path)
        else:
            result = self.running.runBytes(image_bytes)

        if result['code'] == 101:
            return None
        elif result['code'] != 100:
            self.logger.debug(result)
            return []  # 统一返回类型
        return self._convert_result(result)


OCR = OCRControl()
