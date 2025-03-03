from .PPOCR_api import GetOcrApi
from PIL import Image
from io import BytesIO
from os import path, walk, makedirs
from main.mainenvironment import sme, logger


class OCR:
    def __init__(self):
        self.logger = logger
        self.exe_path = sme.ocrdir
        self.workdir = sme.workdir
        if sme.cpu_feature:
            self.exe_name = "PaddleOCR-json.exe"
            self.logger.debug("CPU 支持 AVX2 指令集，使用 PaddleOCR-json")
        else:
            self.exe_name = "RapidOCR-json.exe"
            self.logger.debug("CPU 不支持 AVX2 指令集，使用 RapidOCR-json")
        self.running = None
        self.isrunning = False

    def check(self):
        if self.exe_path:
            if path.exists(self.exe_path):
                if path.basename(self.exe_path) == self.exe_name:
                    return True
            self.logger.debug(f"OCR组件路径无效:{self.exe_path}")
            return False
        else:
            _dir = self.workdir + "\\ocr_json"
            if not path.exists(_dir):
                makedirs(_dir)
                return False
            for root, dirs, files in walk(_dir):
                if self.exe_name in files:
                    self.exe_path = path.join(root, self.exe_name)
                    return True
            self.logger.debug(f"OCR组件缺失")
            return False

    def enable(self):
        if self.isrunning:
            self.logger.debug("OCR早已启用")
            return True
        else:
            try:
                self.logger.debug("开始初始化OCR...")
                self.running = GetOcrApi(self.exe_path)
                self.isrunning = True
                self.logger.debug("初始化OCR完成")
                return True
            except Exception as e:
                self.logger.error(f"初始化OCR失败:{e}")
                self.running = None
                _str = (f"初始化OCR失败:{e}\n"
                        f"请尝试重新下载或解压OCR组件\n"
                        f"若 Win7 报错计算机中丢失 VCOMP140.DLL,请安装 VC运行库\n"
                        f"https://aka.ms/vs/17/release/vc_redist.x64.exe")
                sme.send_messagebox(_str)
                return False

    def disable(self):
        if self.isrunning:
            self.running.exit()
            self.isrunning = False
            self.logger.debug("关闭OCR完成")
        else:
            self.logger.debug("OCR早已关闭")

    @staticmethod
    def convert_format(result):
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

    def run(self, image):
        # self.instance_ocr()
        try:
            if isinstance(image, Image.Image):
                pass
            elif isinstance(image, str):
                return self.running.run(path.abspath(image))
            else:  # 默认为 np.ndarray，避免需要import numpy
                image = Image.fromarray(image)
            image_stream = BytesIO()
            image.save(image_stream, format="PNG")
            image_bytes = image_stream.getvalue()
            return self.running.runBytes(image_bytes)
        except Exception as e:
            self.logger.error(e)
            return r"{}"

    def recognize_single_line(self, image, blacklist=None):
        results = self.convert_format(self.run(image))
        if results:
            for i in range(len(results)):
                line_text = results[i][1][0] if results and len(results[i]) > 0 else ""
                if blacklist and any(char == line_text for char in blacklist):
                    continue
                else:
                    return line_text, results[i][1][1]
        return None

    def output(self, image):
        if isinstance(image, Image.Image):
            pass
        elif isinstance(image, str):
            return self.running.run(path.abspath(image))
        else:  # 默认为 np.ndarray，避免需要import numpy
            image = Image.fromarray(image)
        image_stream = BytesIO()
        image.save(image_stream, format="PNG")
        image_bytes = image_stream.getvalue()
        result = self.running.runBytes(image_bytes)
        if result['code'] == 101:
            return None
        elif result['code'] != 100:
            self.logger.debug(result)
            return False
        converted_result = []
        for item in result['data']:
            box = item['box']
            text = item['text']
            score = item['score']
            converted_item = [[box[0], box[1], box[2], box[3]], (text, score)]
            converted_result.append(converted_item)
        return converted_result


smo = OCR()
