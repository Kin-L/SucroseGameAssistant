import keyboard
from time import sleep
from win32api import mouse_event

press = keyboard.send
keydown = keyboard.press
keyup = keyboard.release
wait = sleep
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
