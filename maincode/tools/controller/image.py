import cv2
from PIL import Image
from os import path, remove
import numpy as np
from maincode.tools.core.baseclass import CtrlBase
from maincode.tools.core.logger import logger
from maincode.tools.controller.ocr import OCR


class SGAImage(CtrlBase):
    def __init__(self):
        self.OCR = OCR

    def screenshot(self, zone="FULL", save=False):
        ...

    def readpic(self, template, delete=False, zone=None) -> Image.Image:
        if template is None:
            template = self.screenshot()
        elif isinstance(template, Image.Image):
            pass
        elif isinstance(template, str) and path.isfile(template):
            template_path = str(template)
            template = Image.open(template)
            if delete:
                try:
                    remove(template_path)
                except Exception as e:
                    logger.warning(f"删除文件失败: {e}")
        else:
            raise ValueError("error: template 参数无效")
        if zone is not None:
            template = template.crop(zone)
        return template

    @staticmethod
    def _convert_to_cv2(image: Image.Image) -> np.ndarray:
        """将PIL图像转换为OpenCV图像"""
        return cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)

    def findpic(self, target, zone: tuple = None, template=None, delete=False, method=cv2.TM_CCOEFF_NORMED):
        """
        :param target: 目标模板小图
        :param zone: 区域
        :param template: 匹配区域图
        :param delete: 如果template传入字符串为图片路径， 是否路径所在图片
        :param method: 模板匹配模式
        :return: center, sim
        """
        origin = (0, 0) if zone is None else zone[:2]
        zone = self.convert(zone)
        template = self.readpic(template, delete, zone)
        size = template.size
        template = self._convert_to_cv2(template)
        template = cv2.resize(template, self.convertVectorR(size)) if self.ZoomW != 1.0 else template
        target = self.readpic(target)
        size = target.size
        target = self._convert_to_cv2(target)
        match_res = cv2.matchTemplate(template, target, method)
        min_sim, max_sim, min_loc, max_loc = cv2.minMaxLoc(match_res)
        if (min_sim >= -0.6) and (max_sim <= 0.6):
            return (0, 0), 0
        else:
            min_sim *= -1
            rel, sim = (max_loc, max_sim) if max_sim >= min_sim else (min_loc, min_sim)
            pos = tuple(o + r + int(s / 2) for o, r, s in zip(origin, rel, size))
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
        template = self._convert_to_cv2(template)
        rgb = target[0:2], target[2:4], target[4:6]
        target_bgr = list(int(i, 16) for i in rgb)[::-1]
        lower = np.array([max(0, x - tolerance) for x in target_bgr], dtype=np.uint8)
        upper = np.array([min(255, x + tolerance) for x in target_bgr], dtype=np.uint8)
        # 创建颜色掩膜
        mask = cv2.inRange(template, lower, upper)
        cnts, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        if cnts:
            cnts_sort = sorted(cnts, key=cv2.contourArea, reverse=True)  # 将轮廓包含面积从大到小排列
            x, y, w, h = cv2.boundingRect(cnts_sort[0])
            pos = (o + r + int(s / 2) for o, r, s in zip(origin, (x, y), (w, h)))
            return self.LocTuple(pos)
        else:
            return None

    def _ocr_resize(self, template: Image.Image) -> tuple:
        """OCR缩放处理"""
        Zoom = min(self.ZoomW, self.ZoomH)
        if Zoom > 0.84:
            Zoom = Zoom * 1920 / 1600
            x, y = template.size
            template = template.resize((int(x / Zoom), int(y / Zoom)))
        else:
            Zoom = 1
        return template, Zoom

    def ocr(self, zone=None, template=None, mode: int = 0, delete=False):
        self.OCR.enable() if not self.OCR.isrunning else 1
        zone = self.convert(zone)
        origin = zone[:2]
        template = self.readpic(template, delete, zone)
        template, Zoom = self._ocr_resize(template)
        _dict = self.OCR.run(template)
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
                for item in _dict['data']:
                    _box = item['box']
                    possize = _box[0], _box[2]
                    possize = np.round(np.array(possize) * Zoom +
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
        template, Zoom = self._ocr_resize(template)
        _dict = self.OCR.run(template)
        if _dict['code'] == 100:
            for item in _dict['data']:
                if target in item['text']:
                    _box = item['box']
                    pos = self.Zone(*_box[0], *_box[2]).center
                    pos = map(int, np.array(pos) * Zoom +
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
