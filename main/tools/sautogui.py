import keyboard
from time import sleep
from win32api import mouse_event, SetCursorPos
from main.mainenvironment import sme
import numpy as np
press = keyboard.send
keydown = keyboard.press
keyup = keyboard.release
click_down_map = {"left": 0x0002, "right": 0x0008, "middle": 0x0020}
click_up_map = {"left": 0x0004, "right": 0x0010, "middle": 0x0040}


def clickonce(_click):
    mouse_event(click_down_map[_click.lower()], 0, 0)
    sleep(0.01)
    mouse_event(click_up_map[_click.lower()], 0, 0)
    sleep(0.01)


def clickdown(_click):
    mouse_event(click_down_map[_click.lower()], 0, 0)
    sleep(0.01)


def clickup(_click):
    mouse_event(click_up_map[_click.lower()], 0, 0)
    sleep(0.01)


# 坐标缩放
def tuple_zoom(_nl):
    return np.rint(np.multiply(_nl, sme.zoom))


# 坐标移动
def position_trans(_xy):
    return np.add(_xy, sme.position)


def frame_trans(_zone):
    return np.add(_zone, sme.position+sme.position)


# 坐标缩放并移动
def position_change(_xy):
    return np.add(np.rint(np.multiply(_xy, sme.zoom)), sme.position)


def frame_change(_zone):
    return np.add(np.rint(np.multiply(_zone, sme.zoom)), sme.position+sme.position)


def decpos(pos):
    if isinstance(pos[1], bool):
        return pos[0]
    else:
        return np.add(np.rint(np.multiply(pos, sme.zoom)), sme.position)


def decvec(vec):
    if isinstance(vec[1], bool):
        return vec[0]
    else:
        return np.rint(np.multiply(vec, sme.zoom))


def deczone(zone):
    if isinstance(zone[1], bool):
        return zone[0]
    else:
        np.add(np.rint(np.multiply(zone, sme.zoom)), sme.position + sme.position)


def regzone(_zone):
    if _zone is None:
        _zone = sme.rcgmode
        _position = sme.position
    elif isinstance(_zone[1], int):
        _zone = deczone(_zone)
        _position = _zone[0:2]
    else:
        _zone = _zone[0]
        _position = _zone[0:2]
    return _zone, _position


def move(vec):
    x, y = decvec(vec)
    mouse_event(0x0001, x, y, 0, 0)
    sleep(0.01)


def moveto(pos):
    SetCursorPos(decpos(pos))
    sleep(0.01)


def click(pos):
    SetCursorPos(decpos(pos))
    sleep(0.01)
    mouse_event(2, 0, 0)
    sleep(0.01)
    mouse_event(4, 0, 0)
    sleep(0.01)


def drag(pos, vec, duration, steps=10, _click="left"):
    SetCursorPos(decpos(pos))
    sleep(0.01)
    mouse_event(click_down_map[_click.lower()], 0, 0)
    sleep(0.01)
    delay = duration / steps
    x, y = np.divide(decvec(vec), steps)
    for i in range(steps):
        mouse_event(0x0001, x, y, 0, 0)
        sleep(delay)
    mouse_event(click_up_map[_click.lower()], 0, 0)
    sleep(0.01)


def scroll(pos, clicks=1):
    SetCursorPos(decpos(pos))
    sleep(0.01)
    if clicks > 0:
        for _ in range(clicks):
            mouse_event(0x0800, 0, 0, 120, 0)
            sleep(0.05)
    else:
        for _ in range(clicks):
            mouse_event(0x0800, 0, 0, -120, 0)
            sleep(0.05)


def hscroll(pos, clicks=1):
    SetCursorPos(decpos(pos))
    sleep(0.01)
    if clicks > 0:
        for _ in range(clicks):
            mouse_event(0x1000, 0, 0, 120, 0)
            sleep(0.05)
    else:
        for _ in range(clicks):
            mouse_event(0x1000, 0, 0, -120, 0)
            sleep(0.05)
