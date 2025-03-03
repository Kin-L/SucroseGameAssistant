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
def coordinate_zoom(_nl):
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


def move(xy, duration, steps=10):
    x, y = position_change(xy)
    delay = duration / steps
    dx = x / steps
    dy = y / steps
    for i in range(steps):
        mouse_event(0x0001, dx, dy, 0, 0)
        sleep(delay)


def moveto(xy):
    SetCursorPos(position_change(xy))
    sleep(0.01)


def click(xy):
    SetCursorPos(position_change(xy))
    sleep(0.01)
    mouse_event(2, 0, 0)
    sleep(0.01)
    mouse_event(4, 0, 0)
    sleep(0.01)


def drag(pos, mov, duration, steps=10):
    x, y = position_change(mov)
    SetCursorPos(position_change(pos))
    sleep(0.01)
    mouse_event(2, 0, 0)
    sleep(0.01)
    delay = duration / steps
    dx = x / steps
    dy = y / steps
    for i in range(steps):
        mouse_event(0x0001, dx, dy, 0, 0)
        sleep(delay)
    mouse_event(4, 0, 0)
    sleep(0.01)


def scroll(xy, clicks=1):
    SetCursorPos(position_change(xy))
    sleep(0.01)
    if clicks > 0:
        for _ in range(clicks):
            mouse_event(0x0800, 0, 0, 120, 0)
            sleep(0.05)
    else:
        for _ in range(clicks):
            mouse_event(0x0800, 0, 0, -120, 0)
            sleep(0.05)


def hscroll(xy, clicks=1):
    SetCursorPos(position_change(xy))
    sleep(0.01)
    if clicks > 0:
        for _ in range(clicks):
            mouse_event(0x1000, 0, 0, 120, 0)
            sleep(0.05)
    else:
        for _ in range(clicks):
            mouse_event(0x1000, 0, 0, -120, 0)
            sleep(0.05)
