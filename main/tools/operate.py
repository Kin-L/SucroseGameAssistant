import keyboard
import numpy as np
import cv2
from .image import screenshot, target_load, save_image
from .ocr.main import smo
from main.mainenvironment import sme
from time import sleep
from .sautogui import moveto, clickonce, regzone, decvec


def click_text(_target, _zone=None, wait_time=(0.8, 10, 0.8),
               _trigger=(None, 0, "left")):
    _time, _num, _wait = wait_time
    _zone, _position = regzone(_zone)
    _clicknum = 0
    _curclicked = False
    for i in range(_num):
        _template = screenshot(_zone)
        _dict = smo.running.run(_template)
        if _dict['code'] == 100:
            _clicked = False
            for item in _dict['data']:
                if _target in item['text']:
                    _pos, _mode, _cli = _trigger
                    # _mode = 0 点击box坐标
                    # _mode = 1 点击_pos变换坐标
                    # _mode = 2 点击box的_pos变换相对坐标
                    if _mode == 0:
                        _box = item['box']
                        moveto((np.divide(np.add(_box[0], _box[2]), 2) + _position, True))
                        clickonce(_cli)
                    elif _mode == 1:
                        moveto(_pos)
                        clickonce(_cli)
                    elif _mode == 2:
                        _box = item['box']
                        moveto((np.divide(np.add(_box[0], _box[2]), 2) + _position + decvec(_pos), True))
                        clickonce(_cli)
                    else:
                        raise ValueError("error: click_text \"_mode\" 无效参数")
                    _clicked = True
                    _clicknum += 1
                    break
            if _clicked:
                _curclicked = True
            else:
                if _curclicked:
                    return True
        elif _dict['code'] == 101:
            if _curclicked:
                return True
        else:
            _code = _dict['code']
            raise RuntimeError(f"error: ocr 识别失败 code = {_code}")
        if _curclicked:
            sleep(_wait)
        else:
            sleep(_time)
    save_image(_template, "_template")
    raise RuntimeError(f"error: click_text 等待超时 _clicknum = {_clicknum}")


def click_pic(_target, _zone=None, wait_time=(0.8, 10, 0.8),
              _trigger=(None, 0, "left"), _minsim=sme.sim):
    _time, _num, _wait = wait_time
    _zone, _position = regzone(_zone)
    _target = target_load(_target)[0]
    _clicknum = 0
    _curclicked = False
    for i in range(_num):
        _template = screenshot(_zone)
        match_res = cv2.matchTemplate(_template, _target, cv2.TM_CCOEFF_NORMED)
        min_sim, _sim, min_loc, _loc = cv2.minMaxLoc(match_res)
        if _sim >= _minsim:
            _pos, _mode, _cli = _trigger
            # _mode = 0 点击box坐标
            # _mode = 1 点击_pos变换坐标
            # _mode = 2 点击box的_pos变换相对坐标
            if _mode == 0:
                moveto((np.rint(np.add(_loc, _position)), True))
                clickonce(_cli)
            elif _mode == 1:
                moveto(_pos)
                clickonce(_cli)
            elif _mode == 2:
                moveto((np.rint(np.add(_loc, _position)) + decvec(_pos), True))
                clickonce(_cli)
            else:
                raise ValueError("error: click_pic \"_mode\" 无效参数")
            _clicknum += 1
            _curclicked = True
            sleep(_wait)
            continue
        elif _curclicked:
            return True
        sleep(_time)
    save_image(_template, "_template")
    raise RuntimeError(f"error: click_pic 等待超时 _clicknum = {_clicknum}")
    

def press_text(_target, _zone=None, wait_time=(0.8, 10, 0.8),
               _trigger="esc"):
    _time, _num, _wait = wait_time
    _zone, _position = regzone(_zone)
    _pressnum = 0
    _curpressed = False
    for i in range(_num):
        _template = screenshot(_zone)
        _dict = smo.running.run(_template)
        if _dict['code'] == 100:
            _pressed = False
            for item in _dict['data']:
                if _target in item['text']:
                    keyboard.send(_trigger)
                    _pressed = True
                    _pressnum += 1
                    break
            if _pressed:
                _curpressed = True
            else:
                if _curpressed:
                    return True
        elif _dict['code'] == 101:
            if _curpressed:
                return True
        else:
            _code = _dict['code']
            raise RuntimeError(f"error: ocr 识别失败 code = {_code}")
        if _curpressed:
            sleep(_wait)
        else:
            sleep(_time)
    save_image(_template, "_template")
    raise RuntimeError(f"error: press_text 等待超时 _pressnum = {_pressnum}")


def press_pic(_target, _zone=None, wait_time=(0.8, 10, 0.8),
              _trigger="esc", _minsim=sme.sim):
    _time, _num, _wait = wait_time
    _zone, _position = regzone(_zone)
    _target = target_load(_target)[0]
    _pressnum = 0
    _curpressed = False
    for i in range(_num):
        _template = screenshot(_zone)
        match_res = cv2.matchTemplate(_template, _target, cv2.TM_CCOEFF_NORMED)
        min_sim, _sim, min_loc, _loc = cv2.minMaxLoc(match_res)
        if _sim >= _minsim:
            keyboard.send(_trigger)
            _pressnum += 1
            _curpressed = True
            sleep(_wait)
            continue
        elif _curpressed:
            return True
        sleep(_time)
    save_image(_template, "_template")
    raise RuntimeError(f"error: press_pic 等待超时 _pressnum = {_pressnum}")


def click_to_text(_target, _zone=None, wait_time=(0.8, 10),
                  _trigger=(None, "left")):
    _time, _num = wait_time
    _zone, _position = regzone(_zone)
    _clicknum = 0
    _pos, _cli = _trigger
    for i in range(_num):
        _template = screenshot(_zone)
        _dict = smo.running.run(_template)
        if _dict['code'] == 100:
            _clicked = False
            for item in _dict['data']:
                if _target in item['text']:
                    return True
        elif _dict['code'] == 101:
            pass
        else:
            _code = _dict['code']
            raise RuntimeError(f"error: ocr 识别失败 code = {_code}")
        if _pos:
            moveto(_pos)
        clickonce(_cli)
        _clicknum += 1
        sleep(_time)
    save_image(_template, "_template")
    raise RuntimeError(f"error: click_to_text 等待超时 _clicknum = {_clicknum}")


def click_to_pic(_target, _zone=None, wait_time=(0.8, 10),
                 _trigger=(None, "left"), _minsim=sme.sim):
    _time, _num = wait_time
    _zone, _position = regzone(_zone)
    _target = target_load(_target)[0]
    _clicknum = 0
    _pos, _cli = _trigger
    for i in range(_num):
        _template = screenshot(_zone)
        match_res = cv2.matchTemplate(_template, _target, cv2.TM_CCOEFF_NORMED)
        min_sim, _sim, min_loc, _loc = cv2.minMaxLoc(match_res)
        if _sim >= _minsim:
            return True
        if _pos:
            moveto(_pos)
        clickonce(_cli)
        _clicknum += 1
        sleep(_time)
    save_image(_template, "_template")
    raise RuntimeError(f"error: click_to_pic 等待超时 _clicknum = {_clicknum}")


def press_to_text(_target, _zone=None, wait_time=(0.8, 10),
                  _trigger="esc"):
    _time, _num = wait_time
    _zone, _position = regzone(_zone)
    _pressnum = 0
    for i in range(_num):
        _template = screenshot(_zone)
        _dict = smo.running.run(_template)
        if _dict['code'] == 100:
            _pressed = False
            for item in _dict['data']:
                if _target in item['text']:
                    return True
        elif _dict['code'] == 101:
            pass
        else:
            _code = _dict['code']
            raise RuntimeError(f"error: ocr 识别失败 code = {_code}")
        keyboard.send(_trigger)
        _pressnum += 1
        sleep(_time)
    save_image(_template, "_template")
    raise RuntimeError(f"error: press_to_text 等待超时 _pressnum = {_pressnum}")


def press_to_pic(_target, _zone=None, wait_time=(0.8, 10),
                 _trigger="esc", _minsim=sme.sim):
    _time, _num = wait_time
    _zone, _position = regzone(_zone)
    _target = target_load(_target)[0]
    _pressnum = 0
    for i in range(_num):
        _template = screenshot(_zone)
        match_res = cv2.matchTemplate(_template, _target, cv2.TM_CCOEFF_NORMED)
        min_sim, _sim, min_loc, _loc = cv2.minMaxLoc(match_res)
        if _sim >= _minsim:
            return True
        keyboard.send(_trigger)
        _pressnum += 1
        sleep(_time)
    save_image(_template, "_template")
    raise RuntimeError(f"error: press_to_pic 等待超时 _pressnum = {_pressnum}")


def click_change(_trigger=(None, "left"), _zone=None,
                 wait_time=(0.8, 10), _minsim=sme.sim):
    _time, _num = wait_time
    _zone, _position = regzone(_zone)
    _clicknum = 0
    _pos, _cli = _trigger
    _past = screenshot(_zone)
    for i in range(_num):
        if _pos:
            moveto(_pos)
        clickonce(_cli)
        _clicknum += 1
        sleep(_time)
        _last = screenshot(_zone)
        match_res = cv2.matchTemplate(_past, _last, cv2.TM_CCOEFF_NORMED)
        min_sim, _sim, min_loc, _loc = cv2.minMaxLoc(match_res)
        if _sim < _minsim:
            return True
    save_image(_past, "_past")
    save_image(_last, "_last")
    raise RuntimeError(f"error: click_change 等待超时 _clicknum = {_clicknum}")


def press_change(_trigger="esc", _zone=None,
                 wait_time=(0.8, 10), _minsim=sme.sim):
    _time, _num = wait_time
    _zone, _position = regzone(_zone)
    _pressnum = 0
    _past = screenshot(_zone)
    for i in range(_num):
        keyboard.send(_trigger)
        _pressnum += 1
        sleep(_time)
        _last = screenshot(_zone)
        match_res = cv2.matchTemplate(_past, _last, cv2.TM_CCOEFF_NORMED)
        min_sim, _sim, min_loc, _loc = cv2.minMaxLoc(match_res)
        if _sim < _minsim:
            return True
    save_image(_past, "_past")
    save_image(_last, "_last")
    raise RuntimeError(f"error: press_change 等待超时 _pressnum = {_pressnum}")
