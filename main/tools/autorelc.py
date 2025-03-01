from win32api import mouse_event, SetCursorPos
from time import sleep


def move(xy, duration, steps=10):
    x, y = xy
    delay = duration / steps
    dx = x / steps
    dy = y / steps
    for i in range(steps):
        mouse_event(0x0001, dx, dy, 0, 0)
        sleep(delay)


def moveto(xy):
    SetCursorPos(xy)
    sleep(0.01)


def click(xy):
    x, y = xy
    SetCursorPos(xy)
    sleep(0.01)
    mouse_event(2, x, y)
    sleep(0.01)
    mouse_event(4, x, y)
    sleep(0.01)


def drag(pos, mov, duration, steps=10):
    x, y = mov
    SetCursorPos(pos)
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
    SetCursorPos(xy)
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
    SetCursorPos(xy)
    sleep(0.01)
    if clicks > 0:
        for _ in range(clicks):
            mouse_event(0x1000, 0, 0, 120, 0)
            sleep(0.05)
    else:
        for _ in range(clicks):
            mouse_event(0x1000, 0, 0, -120, 0)
            sleep(0.05)


if __name__ == '__main__':
    pass
