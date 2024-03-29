from .operate import Operate
from .system import *


def text_match(res, text, domain=(0, 0, 1920, 1080), border=False):
    if text in res[0]:
        rx1, ry1, rx2, ry2 = res[1]
        dx1, dy1, dx2, dy2 = domain
        if border:
            if dx1 <= rx1 and dy1 <= ry1 and rx2 <= dx2 and ry2 <= dy2:
                return int((rx1+rx2)//2), int((ry1+ry2)//2)
            else:
                return False
        else:
            if dx1 < rx1 and dy1 < ry1 and rx2 < dx2 and ry2 < dy2:
                return int((rx1+rx2)//2), int((ry1+ry2)//2)
            else:
                return False
    else:
        return False


class Environment(Operate):
    def __init__(self, wide, high):
        super().__init__()
        self.get_user_admin()
        self.get_workdir()
        self.set_compile(wide, high)
        (self.resolution_origin,
         self.resolution_now,
         self.zoom_desktop) = get_resolution_zoom()
        self.mode()
        from tools.ocr.ocr import OCR
        self.OCR = OCR(self.logger, self.workdir)

    # 键鼠及识图缩放模式（全屏复刻模式：0， 软件窗口模式：1， 全屏普通模式：2）
    def mode(self, mode_num: int = 0):
        if mode_num == 0:
            self.frame = (0, 0) + self.resolution_origin
            self.zoom = self.resolution_origin[0] / self.resolution_compile[0]
            return True
        elif mode_num == 1:
            if self.soft.hwnd:
                if self.soft.get_window_information():
                    self.frame, self.zoom = self.soft.frame, self.soft.zoom
                    self.logger.debug(f"mode 1: {self.frame}*{self.zoom}")
                    return True
                else:
                    return False
            else:
                self.logger.error("未识别到软件/未开启软件")
                return False
        elif mode_num == 2:
            self.frame = (0, 0) + self.resolution_origin
            self.zoom = 1
            return True
        else:
            self.logger.error("无效参数 mode_num")
            return False

    def clickto(self, pos, wait_time, mat, path: str = ""):
        target, zone, sim = mat
        if sim == 0:
            while 1:
                for i in range(15):
                    self.click(pos)
                    self.wait(wait_time)
                    if xy := self.find_text(target, zone, path):
                        return xy
                if not self.soft.isforeground():
                    self.soft.foreground()
                else:
                    raise RuntimeError("执行超时：clickto")
        elif 0 < sim < 1:
            while 1:
                for i in range(15):
                    self.click(pos)
                    self.wait(wait_time)
                    xy, val = self.find_pic(target, zone, path)
                    if val >= sim:
                        return xy
                if not self.soft.isforeground():
                    self.soft.foreground()
                else:
                    raise RuntimeError("执行超时：clickto")
        elif sim == 1:
            while 1:
                for i in range(15):
                    self.click(pos)
                    self.wait(wait_time)
                    if xy := self.match_text(target, zone, path):
                        return xy
                if not self.soft.isforeground():
                    self.soft.foreground()
                else:
                    raise RuntimeError("执行超时：clickto")
        elif sim == -1:
            while 1:
                for i in range(15):
                    self.click(pos)
                    self.wait(wait_time)
                    if not self.match_text(target, zone, path):
                        return 0, 0
                if not self.soft.isforeground():
                    self.soft.foreground()
                else:
                    raise RuntimeError("执行超时：clickto")

    def pressto(self, key, wait_time, mat, path: str = ""):
        target, zone, sim = mat
        while 1:
            for i in range(15):
                press(key)
                self.wait(wait_time)
                if sim:
                    pos, val = self.find_pic(target, zone, path)
                    if val >= sim:
                        return pos
                else:
                    if pos := self.find_text(target, zone, path):
                        return pos
            if not self.soft.isforeground():
                self.soft.foreground()
            else:
                raise RuntimeError("执行超时：clickto")


env = Environment(1920, 1080)
logger = env.logger
axis_zoom, axis_translation, axis_change = env.axis_zoom, env.axis_translation, env.axis_change
move, click, drag, roll, roll_h = env.move, env.click, env.drag, env.roll, env.roll_h
press, keydown, keyup, key_add, wait = env.press, env.keydown, env.keyup, env.key_add, env.wait
ocr, screenshot, find_pic, find_color, find_text = env.ocr, env.screenshot, env.find_pic, env.find_color, env.find_text
center, click_pic, click_text, clickto, pressto = env.center, env.click_pic, env.click_text, env.clickto, env.pressto
wait_pic, wait_text = env.wait_pic, env.wait_text
