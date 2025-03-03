import cv2
from colorsys import rgb_to_hsv
from win32api import SetCursorPos
from PIL import ImageGrab, Image
from os import path
from time import sleep
import numpy as np
from .sautogui import frame_change, coordinate_zoom
from main.mainenvironment import sme
from .ocr.main import smo


def screenshot(_zone="WINDOW"):
    SetCursorPos((1, 1))
    sleep(0.01)
    if isinstance(_zone, tuple):
        return ImageGrab.grab(frame_change(_zone))  # 截取屏幕指定区域的图像
    elif _zone == "WINDOW":
        return ImageGrab.grab(sme.frame)
    elif _zone == "FULLSCREEN":
        return ImageGrab.grab()
    else:
        raise RuntimeError("error:\"_zone\" 无效参数")


def ocr(_zone="ALL", _template: str = "", mode: int = 0):
    if smo.isrunning:
        raise RuntimeError("error: ocr 未启用")
    if isinstance(_template, Image.Image):
        pass
    elif _template == "":
        _template = screenshot()
    else:
        if path.exists(_template):
            _template = Image.open(_template)
        else:
            raise RuntimeError("error: ocr \"_template\" 无效参数")
    if _zone == "ALL":
        _position = (0, 0)
    else:
        _position = _zone[0:2]
        scx1, scy1, scx2, scy2 = coordinate_zoom(_zone)
        _template = _template[scy1:scy2, scx1:scx2]
    _dict = smo.running.run(_template)
    if _dict['code'] == 100:
        if mode == 0:  # 简单单行识字
            _line = _dict['data'][0]
            return _line['text'], _line['score']
        elif mode == 1:  # 分析文本及其位置形状
            _list = []
            for item in _dict['data']:
                _box = item['box']
                _list += [item['text'], _box[0]+_box[2], item['score']]
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


def find_color(_rgb, _zone="ALL", _template: str = "", _tolerance=5):
    if isinstance(_template, Image.Image):
        _hsv = cv2.cvtColor(np.asarray(_template), cv2.COLOR_RGB2HSV)
    elif isinstance(_template, np.ndarray):
        _hsv = _template
    elif _template == "":  # 截取实时窗口
        _hsv = cv2.cvtColor(np.asarray(screenshot()), cv2.COLOR_RGB2HSV)
    else:  # 路径
        if path.exists(_template):
            _hsv = cv2.cvtColor(cv2.imread(_template), cv2.COLOR_BGR2HSV)
        else:
            raise RuntimeError("error:find_pic \"_template\" 无效参数")
    if _zone == "ALL":
        _position = (0, 0)
    else:
        _position = _zone[0:2]
        scx1, scy1, scx2, scy2 = coordinate_zoom(_zone)
        _template = _template[scy1:scy2, scx1:scx2]
    _template = cv2.cvtColor(_template, cv2.COLOR_BGR2HSV)

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
        return np.divide(np.add(_position, (x, y))+np.divide((w, h), 2), sme.zoom)
    else:
        return False


def find_text(_target, _zone="ALL", _template: str = "", wait_time=(1, 10)):
    if smo.isrunning:
        raise RuntimeError("error: ocr 未启用")
    if _template == "":
        if _zone == "ALL":
            _position = (0, 0)
        else:
            _position = _zone[0:2]
        _time, _num = wait_time
        for i in range(_num):
            _template = screenshot()
            if _zone != "ALL":
                scx1, scy1, scx2, scy2 = coordinate_zoom(_zone)
                _template = _template[scy1:scy2, scx1:scx2]
            _dict = smo.running.run(_template)
            if _dict['code'] == 100:
                for item in _dict['data']:
                    if _target in item['text']:
                        _box = item['box']
                        return np.divide(np.divide(np.add(_box[0], _box[2]), 2) + _position, sme.zoom)
            elif _dict['code'] == 101:
                pass
            else:
                _code = _dict['code']
                raise RuntimeError(f"error: ocr 识别失败 code = {_code}")
            sleep(_time)
        raise RuntimeError("error: find_text 识别超时")
    elif isinstance(_template, Image.Image):
        pass
    else:
        if path.exists(_template):
            _template = Image.open(_template)
        else:
            raise RuntimeError("error: ocr \"_template\" 无效参数")
    if _zone == "ALL":
        _position = (0, 0)
    else:
        _position = _zone[0:2]
        scx1, scy1, scx2, scy2 = coordinate_zoom(_zone)
        _template = _template[scy1:scy2, scx1:scx2]
    _dict = smo.running.run(_template)
    if _dict['code'] == 100:
        for item in _dict['data']:
            if _target in item['text']:
                _box = item['box']
                return np.divide(np.divide(np.add(_box[0], _box[2]), 2) + _position, sme.zoom)
        return False
    elif _dict['code'] == 101:
        return False
    else:
        _code = _dict['code']
        raise RuntimeError(f"error: ocr 识别失败 code = {_code}")


def find_pic(_target, _zone="ALL", _template: str = "", wait_time=(1, 10), _minsim=sme.sim):
    # _target加载处理
    if isinstance(_target, Image.Image):
        _template = cv2.cvtColor(np.asarray(_target), cv2.COLOR_RGB2BGR)
    elif isinstance(_target, np.ndarray):
        pass
    elif path.exists(_target):
        _target = cv2.imread(_target)
    else:
        raise ValueError("error: find_pic \"_target\" 无效参数")
    _tgwh = _target.shape[0:2]
    if sme.zoom == 1.0:
        pass
    elif sme.zoom > 1.0:
        _tgh, _tgw = coordinate_zoom(_tgwh)
        _target = cv2.resize(_target, _tgw, _tgh, interpolation=cv2.INTER_CUBIC)
    elif sme.zoom < 1.0:
        _tgh, _tgw = coordinate_zoom(_tgwh)
        _target = cv2.resize(_target, _tgw, _tgh, interpolation=cv2.INTER_AREA)
    # _template加载处理
    if _template == "":
        if _zone == "ALL":
            _position = (0, 0)
        else:
            _position = _zone[0:2]
        _time, _num = wait_time
        for i in range(_num):
            _template = cv2.cvtColor(np.asarray(screenshot()), cv2.COLOR_RGB2BGR)
            if _zone != "ALL":
                scx1, scy1, scx2, scy2 = coordinate_zoom(_zone)
                _template = _template[scy1:scy2, scx1:scx2]
            match_res = cv2.matchTemplate(_template, _target, cv2.TM_CCOEFF_NORMED)
            min_sim, _sim, min_loc, _loc = cv2.minMaxLoc(match_res)
            if _sim >= _minsim:
                if sme.zoom != 1.0:
                    _loc = np.divide(_loc, sme.zoom)
                centre = np.rint(_loc + np.divide(_tgwh, 2) + _position)
                return centre
        raise RuntimeError("error: find_pic 识别超时")
    elif isinstance(_template, Image.Image):
        _template = cv2.cvtColor(np.asarray(_template), cv2.COLOR_RGB2BGR)
    elif isinstance(_template, np.ndarray):
        pass
    else:  # 路径
        if path.exists(_template):
            _template = cv2.imread(_template)
        else:
            raise RuntimeError("error:find_pic \"_template\" 无效参数")
    if _zone == "ALL":
        _position = (0, 0)
    else:
        _position = _zone[0:2]
        scx1, scy1, scx2, scy2 = coordinate_zoom(_zone)
        _template = _template[scy1:scy2, scx1:scx2]
    match_res = cv2.matchTemplate(_template, _target, cv2.TM_CCOEFF_NORMED)
    min_sim, _sim, min_loc, _loc = cv2.minMaxLoc(match_res)
    if _sim < _minsim:
        return False
    else:
        if sme.zoom != 1.0:
            _loc = np.divide(_loc, sme.zoom)
        centre = np.rint(_loc+np.divide(_tgwh, 2)+_position)
        return centre


if __name__ == '__main__':
    print()
    # env = Environment(1920, 1080)
    # result = ocr(big_pic=r"D:\Kin\Pictures\court.png")
    # print(result)
    # exe_path = r"tools\ocr\PaddleOCR-json_v.1.3.1\PaddleOCR-json.exe"
    # abs_path = os.path.join(os.getcwd(), exe_path)
    # print(abs_path)
    # print(os.path.exists(abs_path))
