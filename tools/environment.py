from .operate import Operate
from .system import *
from numpy import ndarray
from cv2 import imread, imwrite
from os.path import isfile, exists, split, splitext, join, basename
from traceback import format_exc
from os import listdir, remove
from time import strftime, localtime
from shutil import copyfile
from json import load, dump
from yaml import load as yload
from yaml import dump as ydump
from yaml import FullLoader
from os import rename
import os
import numpy as np


def errorsc_save(sc):
    import time
    now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    new_path = f"personal/errorsc/{now}.png"
    if not os.path.exists(r"personal/errorsc"):
        os.makedirs("personal/errorsc")
    if isinstance(sc, np.ndarray):
        imwrite(new_path, sc)
    else:
        rename(sc, new_path)
    return new_path


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
                self.soft.foreground()
                if self.soft.get_window_information(True):
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
        elif mode_num == 3:
            if self.soft.hwnd:
                self.soft.foreground()
                if self.soft.get_window_information(False):
                    self.frame, self.zoom = self.soft.frame, self.soft.zoom
                    self.logger.debug(f"mode 3: {self.frame}*{self.zoom}")
                    return True
                else:
                    return False
            else:
                self.logger.error("未识别到软件/未开启软件")
                return False
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

    def click_to_pic(self, pos, target, zone="ALL", sim: float = 0.9,
                     wait_time=(800, 10)):
        if isinstance(target, ndarray):
            _target = target
        elif target:
            if not isfile(target):
                print("error: findpic 参数 small_pic 为无效路径。")
                raise ValueError("error: findpic 参数 small_pic 为无效路径。")
            else:
                _target = imread(target)
        else:
            print("error: findpic 参数 small_pic 为无效路径。")
            raise ValueError("error: findpic 参数 small_pic 为无效路径。")
        while 1:
            for i in range(wait_time[1]):
                self.click(pos)
                sleep(wait_time[0] / 1000)
                p, s = self.find_pic(_target, zone)
                if s >= sim:
                    return p
            if self.soft.isforeground():
                raise RuntimeError("识别超时")
            else:
                self.soft.foreground()
                self.logger.info("切换顶层窗口")

    def click_to_text(self, pos, target: str, zone="ALL",
                      wait_time=(800, 10)):
        while 1:
            for i in range(wait_time[1]):
                self.click(pos)
                sleep(wait_time[0] / 1000)
                _list = self.ocr(zone, mode=1)
                result = str_find(target, _list)
                if result:
                    return result
            if self.soft.isforeground():
                raise RuntimeError("识别超时")
            else:
                self.soft.foreground()
                self.logger.info("切换顶层窗口")

    def click_change(self, pos, zone="ALL", sim: float = 0.9,
                     wait_time=(800, 10)):
        bef = self.scshot(zone)
        for i in range(wait_time[1]):
            self.click(pos)
            sleep(wait_time[0] / 1000)
            aft = self.scshot(zone)
            p, s = self.find_pic(bef, template=aft)
            # print(s)
            if s < sim:
                return True
        raise RuntimeError("click_change点击超时")

    def press_to_pic(self, key, target, zone="ALL", sim: float = 0.9,
                     wait_time=(800, 10)):
        if isinstance(target, ndarray):
            _target = target
        elif target:
            if not isfile(target):
                print("error: findpic 参数 small_pic 为无效路径。")
                raise ValueError("error: findpic 参数 small_pic 为无效路径。")
            else:
                _target = imread(target)
        else:
            print("error: findpic 参数 small_pic 为无效路径。")
            raise ValueError("error: findpic 参数 small_pic 为无效路径。")
        while 1:
            for i in range(wait_time[1]):
                press(key)
                sleep(wait_time[0] / 1000)
                p, s = self.find_pic(_target, zone)
                if s >= sim:
                    return p
            if self.soft.isforeground():
                raise RuntimeError("识别超时")
            else:
                self.soft.foreground()
                self.logger.info("切换顶层窗口")

    def press_to_text(self, key, target: str, zone="ALL",
                      wait_time=(800, 10)):
        while 1:
            for i in range(wait_time[1]):
                press(key)
                sleep(wait_time[0] / 1000)
                _list = self.ocr(zone, mode=1)
                result = str_find(target, _list)
                if result:
                    return result
            if self.soft.isforeground():
                raise RuntimeError("识别超时")
            else:
                self.soft.foreground()
                self.logger.info("切换顶层窗口")

    def press_change(self, key, zone="ALL", sim: float = 0.9,
                     wait_time=(800, 10)):
        bef = self.scshot(zone)
        for i in range(wait_time[1]):
            press(key)
            sleep(wait_time[0] / 1000)
            aft = self.scshot(zone)
            p, s = self.find_pic(bef, template=aft)
            # print(s)
            if s < sim:
                return True
        raise RuntimeError("click_change点击超时")


env = Environment(1920, 1080)
logger = env.logger
axis_zoom, axis_translation, axis_change = env.axis_zoom, env.axis_translation, env.axis_change
move, click, drag, roll, roll_h = env.move, env.click, env.drag, env.roll, env.roll_h
press, keydown, keyup, key_add, wait = env.press, env.keydown, env.keyup, env.key_add, env.wait
add_press, clickdown, clickup = env.add_press, env.clickdown, env.clickup
screenshot, scshot, moveto = env.screenshot, env.scshot, env.moveto
ocr, find_pic, find_color, find_text = env.ocr, env.find_pic, env.find_color, env.find_text
click_pic, click_text, clickto, pressto = env.click_pic, env.click_text, env.clickto, env.pressto
click_to_pic, click_to_text, click_change = env.click_to_pic, env.click_to_text, env.click_change
press_to_pic, press_to_text, press_change = env.press_to_pic, env.press_to_text, env.press_change
wait_pic, wait_text, match_text = env.wait_pic, env.wait_text, env.match_text
