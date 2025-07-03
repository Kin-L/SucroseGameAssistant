import cv2
from PIL import ImageGrab, Image
from os import path, remove, makedirs
import numpy as np
from .keymouse import KeyMouse
from time import time, localtime
from maincode.tools.main import GetTracebackInfo, logger
from ..ocr.main import OCR
import subprocess
import io


class SGAImage(KeyMouse):
    def __init__(self):
        self.OCR = OCR()
        self.OCR.check()

    def screenshot(self, zone="FULL", save=False):
        ...

    def screenshot_win(self, zone="FULL", save=False) -> [Image.Image, str]:
        self.checkrun()
        if zone == "WINDOW":
            shot = ImageGrab.grab(self.Operate.zone)
        elif isinstance(zone, tuple):
            shot = ImageGrab.grab(zone)  # 截取屏幕指定区域的图像
        elif zone == "FULL":
            shot = ImageGrab.grab()
        else:
            raise ValueError(f"zone参数异常： {zone}")
        if save:
            if isinstance(save, str):
                try:
                    shot.save(save)
                    return save
                except Exception as e:
                    _path = r"cache\%s.png" % (str(time())[-5:])
                    _str = GetTracebackInfo(e) + f"保存截图错误，进行默认路径保存：{_path}"
                    logger.debug(_str)
            else:
                _path = r"cache\%s.png" % (str(time())[-5:])
            shot.save(_path)
            return _path
        else:
            return shot

    def screenshot_adb(self, zone=None, save=False) -> [Image.Image, str]:
        self.checkrun()
        process = subprocess.Popen(
            [self.adb_path, "-s", self.device_serial, 'exec-out', 'screencap'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=2 ** 22
        )
        stdout, error = process.communicate()

        # 将二进制数据转换为Pillow图像
        try:

            header = stdout[:12]
            width = int.from_bytes(header[0:4], byteorder='little')
            height = int.from_bytes(header[4:8], byteorder='little')
            format_code = int.from_bytes(header[8:12], byteorder='little')

            # 验证格式 (通常为RGBA或RGBX)
            if format_code not in [1, 3, 4]:
                raise RuntimeError(f"不支持的像素格式: {format_code}")

            # 提取像素数据 (跳过16字节头部)
            pixel_data = stdout[16:]

            # 转换为numpy数组
            if format_code == 1:  # RGBA
                img_array = np.frombuffer(pixel_data, dtype=np.uint8).reshape((height, width, 4))
                mode = 'RGBA'
            else:  # RGBX或其他格式
                img_array = np.frombuffer(pixel_data, dtype=np.uint8).reshape((height, width, 4))
                mode = 'RGBX'

            # 转换为Pillow图像
            shot = Image.fromarray(img_array, mode)
        except Exception as e:
            raise RuntimeError(f"图像转换失败: {str(e)}")
        if isinstance(zone, tuple):
            shot = shot.crop(zone)
        if save:
            if isinstance(save, str):
                try:
                    shot.save(save)
                    return save
                except Exception as e:
                    _path = r"cache\%s.png" % (str(time())[-5:])
                    _str = GetTracebackInfo(e) + f"保存截图错误，进行默认路径保存：{_path}"
                    logger.debug(_str)
            else:
                _path = r"cache\%s.png" % (str(time())[-5:])
            shot.save(_path)
            return _path
        else:
            return shot

    @staticmethod
    def SaveShot(image, name):
        if isinstance(image, Image.Image):
            import time
            now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
            name = name + now
            _path = f"personal/errorsc/{name}.png"
            if not path.exists(r"personal/errorsc"):
                makedirs("personal/errorsc")
            image.save(_path)
            logger.info(f"保存图片：{_path}")
            return _path
        else:
            logger.error(f"error: SaveShot 无效传入 {type(image)}")
            logger.error(image)

    def readpic(self, template, delete=False, zone=None) -> Image.Image:
        if template is None:
            template = self.screenshot()
        elif isinstance(template, Image.Image):
            pass
        elif isinstance(template, str) and path.isfile(template):
            template_path = str(template)
            template = Image.open(template)
            if delete:
                remove(template_path)
        else:
            raise ValueError("error: template 参数无效")
        if zone is not None:
            template = template.crop(zone)
        return template

    def findpic(self, target, zone: tuple = None, template=None, delete=False, method=cv2.TM_CCOEFF_NORMED):
        """
        :param target: 目标模板小图
        :param zone: 区域
        :param template: 匹配区域图
        :param delete: 如果template传入字符串为图片路径， 是否路径所在图片
        :param method: 模板匹配模式
        :return: center, sim
        """
        # self.Operate.pos + self.convert(zone) + self.convertVector(*target.size))
        origin = (0, 0) if zone is None else zone[:2]
        zone = self.convert(zone)
        template = self.readpic(template, delete, zone)
        size = template.size
        template = cv2.cvtColor(np.asarray(template), cv2.COLOR_RGB2BGR)
        # print(*self.convertVectorR(size))
        template = cv2.resize(template, self.convertVectorR(size)) if self.ZoomW != 1.0 else template
        target = self.readpic(target)
        size = target.size
        target = cv2.cvtColor(np.asarray(target), cv2.COLOR_RGB2BGR)
        match_res = cv2.matchTemplate(template, target, method)
        min_sim, max_sim, min_loc, max_loc = cv2.minMaxLoc(match_res)
        if (min_sim >= -0.6) and (max_sim <= 0.6):
            return (0, 0), 0
        else:
            min_sim *= -1
            rel, sim = (max_loc, max_sim) if max_sim >= min_sim else (min_loc, min_sim)
            # print(origin, rel, size)
            pos = tuple(o + r + int(s/2) for o, r, s in zip(origin, rel, size))
            # print("pos", pos)
            return self.convert(pos), sim

    def findcolor(self, target, zone=None, template=None, delete=False, tolerance=7):
        """
        :param delete:
        :param zone:
        :param template:
        :param target: 十六进制RGB颜色码 示例：494CF0
        :param tolerance: 容差
        :return: center中心坐标, False是否找到
        """
        zone = self.convert(zone)
        origin = zone[:2]
        template = self.readpic(template, delete, zone)
        template = cv2.cvtColor(np.asarray(template), cv2.COLOR_RGB2BGR)
        rgb = target[0:2], target[2:4], target[4:6]
        target_bgr = list(int(i, 16) for i in rgb)[::-1]
        lower = np.array([max(0, x - tolerance) for x in target_bgr], dtype=np.uint8)
        upper = np.array([min(255, x + tolerance) for x in target_bgr], dtype=np.uint8)
        # 创建颜色掩膜
        mask = cv2.inRange(template, lower, upper)
        cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # print(cnts)
        if cnts:
            cnts_sort = sorted(cnts, key=cv2.contourArea, reverse=True)  # 将轮廓包含面积从大到小排列
            x, y, w, h = cv2.boundingRect(cnts_sort[0])
            pos = (o + r + int(s / 2) for o, r, s in zip(origin, (x, y), (w, h)))
            return self.LocTuple(pos)
        else:
            return None

    def ocr(self, zone=None, template=None, mode: int = 0, delete=False):
        self.OCR.enable() if not self.OCR.isrunning else 1
        zone = self.convert(zone)
        origin = zone[:2]
        template = self.readpic(template, delete, zone)
        Zoom = min(self.ZoomW, self.ZoomH)
        # print(zone)
        if Zoom > 0.84:
            Zoom = Zoom*1920/1600
            x, y = template.size
            template = template.resize((int(x / Zoom), int(y / Zoom)))
        else:
            Zoom = 1
        _dict = self.OCR.run(template)
        # print(_dict)
        if _dict['code'] == 100:
            if mode == 0:  # 简单单行识字
                _str = ""
                _sc = 0
                for line in _dict['data']:
                    _str += line['text']
                    _sc += line['score']
                _sc = _sc / len(_dict['data'])
                return _str, _sc
            elif mode == 1:  # 分析文本及其位置形状
                _list = []
                # print(_dict['data'])
                for item in _dict['data']:
                    _box = item['box']
                    possize = _box[0], _box[2]
                    possize = np.round(np.array(possize) * Zoom +
                                       # np.array(self.Operate.pos) +
                                       np.array(origin)).flatten().tolist()
                    _list += [[item['text'], self.LocTuple(possize), item['score']]]
                return _list
            elif mode == 2:  # 输出原始结果
                return _dict
            else:
                raise ValueError(f"error: ocr 无效参数 mode = {mode}")
        elif _dict['code'] == 101:
            if mode == 0:
                return "", 0
            elif mode == 1:
                return [["", None, 0]]
            elif mode == 2:
                return _dict
            else:
                raise ValueError(f"error: ocr 无效参数 mode = {mode}")
        else:
            _code = _dict['code']
            raise RuntimeError(f"error: ocr 识别失败 code = {_code}")

    def findtext(self, target, zone=None, template=None, delete=False):
        self.OCR.enable() if not self.OCR.isrunning else 1
        zone = self.convert(zone)
        origin = zone[:2]
        template = self.readpic(template, delete, zone)
        # print("zone:", zone)
        Zoom = min(self.ZoomW, self.ZoomH)
        # print("Zoom", Zoom)
        if Zoom > 0.84:
            Zoom = Zoom * 1920 / 1600
            x, y = template.size
            template = template.resize((int(x / Zoom), int(y / Zoom)))
        else:
            Zoom = 1
        _dict = self.OCR.run(template)
        # print(_dict)
        if _dict['code'] == 100:
            for item in _dict['data']:
                if target in item['text']:
                    _box = item['box']
                    pos = self.Zone(*_box[0], *_box[2]).center
                    pos = map(int, np.array(pos) * Zoom +
                              # np.array(self.Operate.pos) +
                              np.array(origin).flatten().tolist())
                    return self.LocTuple(pos)
            return None
        elif _dict['code'] == 101:
            return None
        else:
            _code = _dict['code']
            logger.debug(f"error: ocr 识别失败 code = {_code}")

    @staticmethod
    def StrFind(target, _list):
        for t in _list:
            if target in t[0]:
                x1, y1, x2, y2 = t[1]
                return int((x1 + x2) / 2), int((y1 + y2) / 2)
        return False


if __name__ == '__main__':
    print()
