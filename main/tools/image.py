import cv2
from colorsys import rgb_to_hsv
from win32api import SetCursorPos
from PIL import ImageGrab, Image
from os import path, makedirs
from time import sleep
import numpy as np
from .sautogui import deczone, tuple_zoom, regzone
from main.mainenvironment import sme, logger
from .ocr.main import smo


# _template: str
# _template: None None代表实时截图
# _template: Image.Image
# _zone = tuple or None or (tuple, bool) （None代表ALL）


def screenshot(_zone=sme.rcgmode):
    SetCursorPos((1, 1))
    sleep(0.01)
    if isinstance(_zone, tuple):
        return ImageGrab.grab(deczone(_zone))  # 截取屏幕指定区域的图像
    elif _zone == "WINDOW":
        return ImageGrab.grab(sme.frame)
    elif _zone == "SCREEN":
        return ImageGrab.grab()
    else:
        raise RuntimeError("error:\"_zone\" 无效参数")


def target_load(_target):
    # _target加载处理
    if isinstance(_target, Image.Image):
        _target = cv2.cvtColor(np.asarray(_target), cv2.COLOR_RGB2BGR)
    elif path.exists(_target):
        _target = cv2.imread(_target)
    else:
        raise ValueError("error: target_load \"_target\" 无效参数")
    _tgwh = _target.shape[0:2]
    if sme.zoom == 1.0:
        pass
    elif sme.zoom > 1.0:
        _tgwh = tuple_zoom(_tgwh)
        _tgh, _tgw = _tgwh
        _target = cv2.resize(_target, _tgw, _tgh, interpolation=cv2.INTER_CUBIC)
    else:
        _tgwh = tuple_zoom(_tgwh)
        _tgh, _tgw = _tgwh
        _target = cv2.resize(_target, _tgw, _tgh, interpolation=cv2.INTER_AREA)
    return _target, _tgwh


def save_image(image, name):
    if isinstance(image, Image.Image):
        import time
        now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        name = name + now
        _path = f"personal/errorsc/{name}.png"
        if not path.exists(r"personal/errorsc"):
            makedirs("personal/errorsc")
        image.save(_path)
        logger.info(f"保存图片：{_path}")
    elif isinstance(image, np.ndarray):
        import time
        now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        name = name + now
        _path = f"personal/errorsc/{name}.png"
        if not path.exists(r"personal/errorsc"):
            makedirs("personal/errorsc")
        cv2.imwrite(_path, image)
        logger.info(f"保存图片：{_path}")
    else:
        logger.error(f"error: save_image 无效传入 {type(image)}")
        logger.error(image)


def ocr(_zone=None, _template=None, mode: int = 0):
    if smo.isrunning:
        raise RuntimeError("error: ocr 未启用")
    if isinstance(_template, str):
        if path.exists(_template):
            _template = Image.open(_template)
        else:
            raise RuntimeError("error:find_pic \"_template\" 无效参数")
        if _zone is None:
            _position = (0, 0)
        elif isinstance(_zone[1], int):
            _position = _zone[0:2]
            _template = _template.crop(_zone)
        else:
            raise RuntimeError("error: ocr \"_zone\" 无效参数")
    else:
        _zone, _position = regzone(_zone)
        if _template is None:  # else: Image.Image
            _template = screenshot(_zone)
        else:
            if isinstance(_zone, tuple):
                _template = _template.crop(_zone)
            elif _zone == "WINDOW":
                _template = _template.crop(sme.frame)
    _dict = smo.running.run(_template)
    if _dict['code'] == 100:
        if mode == 0:  # 简单单行识字
            _line = _dict['data'][0]
            return _line['text'], _line['score']
        elif mode == 1:  # 分析文本及其位置形状
            _list = []
            for item in _dict['data']:
                _box = item['box']
                _list += [item['text'], _box[0] + _box[2], item['score']]
            return _list
        elif mode == 2:  # 输出原始结果
            return _dict
        else:
            raise ValueError(f"error: ocr 无效参数 mode = {mode}")
    elif _dict['code'] == 101:
        if mode == 0:
            return False, 0
        elif mode == 1:
            return [[False, None, 0]]
        elif mode == 2:
            return _dict
        else:
            raise ValueError(f"error: ocr 无效参数 mode = {mode}")
    else:
        _code = _dict['code']
        raise RuntimeError(f"error: ocr 识别失败 code = {_code}")


def find_color(_rgb, _zone=None, _template=None, _tolerance=5):
    if isinstance(_template, str):
        if path.exists(_template):
            _template = cv2.cvtColor(cv2.imread(_template), cv2.COLOR_BGR2HSV)
        else:
            raise RuntimeError("error:find_color \"_template\" 无效参数")
        if _zone is None:
            _position = (0, 0)
        elif isinstance(_zone[1], int):
            scx1, scy1, scx2, scy2 = _zone
            _template = _template[scy1:scy2, scx1:scx2]
            _position = scx1, scy1
        else:
            raise RuntimeError("error: find_color \"_zone\" 无效参数")
    else:
        _zone, _position = regzone(_zone)
        if _template is None:  # else: Image.Image
            _template = screenshot(_zone)
        else:
            if isinstance(_zone, tuple):
                _template = _template.crop(_zone)
            elif _zone == "WINDOW":
                _template = _template.crop(sme.frame)
        _template = cv2.cvtColor(np.asarray(_template), cv2.COLOR_RGB2HSV)

    r, g, b = _rgb
    h, s, v = rgb_to_hsv(r, g, b)
    hsv = np.array((h * 255, s * 255, v))
    lower_bound = np.clip(hsv - _tolerance, 0, 255)
    upper_bound = np.clip(hsv + _tolerance, 0, 255)
    _img = cv2.inRange(_template, lower_bound, upper_bound)
    cnts, _ = cv2.findContours(_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if cnts:
        cnts_sort = sorted(cnts, key=cv2.contourArea, reverse=True)  # 将轮廓包含面积从大到小排列
        x, y, w, h = cv2.boundingRect(cnts_sort[0])
        return np.add(_position, (x, y)) + np.divide((w, h), 2), True
    else:
        return None, False


def find_text(_target, _zone=None, _template=None, wait_time=(1, 10)):
    if smo.isrunning:
        raise RuntimeError("error: ocr 未启用")

    def find_text_temp(_target, _template, _position):
        _dict = smo.running.run(_template)
        if _dict['code'] == 100:
            for item in _dict['data']:
                if _target in item['text']:
                    _box = item['box']
                    return np.divide(np.add(_box[0], _box[2]), 2) + _position, True
            return None, False
        elif _dict['code'] == 101:
            return None, False
        else:
            _code = _dict['code']
            raise RuntimeError(f"error: ocr 识别失败 code = {_code}")

    if _template is None:
        _zone, _position = regzone(_zone)
        _time, _num = wait_time
        for i in range(_num):
            res = find_text_temp(_target, screenshot(_zone), _position)
            if res[1]:
                return res
            sleep(_time)
        save_image(_template, "_template")
        raise RuntimeError("error: find_text 识别超时")
    elif isinstance(_template, Image.Image):
        _zone, _position = regzone(_zone)
        if isinstance(_zone, tuple):
            _template = _template.crop(_zone)
        elif _zone == "WINDOW":
            _template = _template.crop(sme.frame)
        return find_text_temp(_target, _template, _position)
    else:
        if path.exists(_template):
            _template = Image.open(_template)
        else:
            raise RuntimeError("error:find_text \"_template\" 无效参数")
        if _zone is None:
            _position = (0, 0)
        elif isinstance(_zone[1], int):
            _position = _zone[0:2]
            _template = _template.crop(_zone)
        else:
            raise RuntimeError("error: find_text \"_zone\" 无效参数")
        return find_text_temp(_target, _template, _position)


def find_pic(_target, _zone=None, _template=None, wait_time=(1, 10), _minsim=sme.sim):
    _target, _tgwh = target_load(_target)

    def find_pic_temp(_target, _template, _position):
        match_res = cv2.matchTemplate(_template, _target, cv2.TM_CCOEFF_NORMED)
        min_sim, _sim, min_loc, _loc = cv2.minMaxLoc(match_res)
        if _sim >= _minsim:
            return np.rint(np.add(_loc, _position)), True
        else:
            return None, False

    if _template is None:
        _zone, _position = regzone(_zone)
        _time, _num = wait_time
        for i in range(_num):
            _template = cv2.cvtColor(np.asarray(screenshot(_zone)), cv2.COLOR_RGB2BGR)
            res = find_pic_temp(_target, _template, _position)
            if res[1]:
                return res
            sleep(_time)
        save_image(_template, "_template")
        raise RuntimeError("error: find_pic 识别超时")
    elif isinstance(_template, Image.Image):
        _zone, _position = regzone(_zone)
        _position = np.divide(_tgwh, 2) + _position
        if isinstance(_zone, tuple):
            _template = _template.crop(_zone)
        elif _zone == "WINDOW":
            _template = _template.crop(sme.frame)
        _template = cv2.cvtColor(np.asarray(_template), cv2.COLOR_RGB2BGR)
        return find_pic_temp(_target, _template, _position)
    else:
        if path.exists(_template):
            _template = cv2.cvtColor(cv2.imread(_template), cv2.COLOR_RGB2BGR)
        else:
            raise RuntimeError("error:find_pic \"_template\" 无效参数")
        if _zone is None:
            _position = np.divide(_tgwh, 2)
        elif isinstance(_zone[1], int):
            scx1, scy1, scx2, scy2 = _zone
            _template = _template[scy1:scy2, scx1:scx2]
            _position = np.divide(_tgwh, 2) + (scx1, scy1)
        else:
            raise RuntimeError("error: find_pic \"_zone\" 无效参数")
        return find_pic_temp(_target, _template, _position)


if __name__ == '__main__':
    print()
