from cv2 import (imread, resize,
                 matchTemplate, minMaxLoc, TM_CCOEFF_NORMED,
                 cvtColor, COLOR_BGR2HSV)
from colorsys import rgb_to_hsv
from win32api import SetCursorPos
from PIL import ImageGrab
import time
import os
from .system import *
color_zone = {"red": [[156, 180], [0, 10], 43, 255, 46, 255], 
              "orange": [11, 25, 43, 255, 46, 255],
              "yellow": [26, 34, 43, 255, 46, 255],
              "green": [35, 77, 43, 255, 46, 255],
              "cyan": [78, 99, 43, 255, 46, 255],
              "blue": [100, 124, 43, 255, 46, 255],
              "purple": [125, 155, 43, 255, 46, 255],
              "white": [0, 180, 0, 300, 221, 255],
              "black": [0, 180, 0, 255, 0, 45],
              "grey": [0, 180, 0, 43, 46, 220]}


class Image(System):
    @staticmethod
    def center(zone):
        x1, y1, x2, y2 = zone
        return int((x1+x2)/2), int((y1+y2)/2)

    def screenshot(self, zone: list = "WINDOW"):
        SetCursorPos((1, 1))
        time.sleep(0.01)
        if zone == "WINDOW":
            shot = ImageGrab.grab(self.frame)
        elif isinstance(zone, tuple):
            (x1, y1, x2, y2) = zone
            (scx1, scy1), (scx2, scy2) = self.axis_zoom(x1, y1), self.axis_zoom(x2, y2)
            xf1, yf1, xf2, yf2 = self.frame
            shot = ImageGrab.grab((xf1 + scx1, yf1 + scy1, xf1 + scx2, yf1 + scy2))  # 截取屏幕指定区域的图像
        elif zone == "FULL":
            shot = ImageGrab.grab()
        else:
            print("error:\"zone\"需要是列表。")
            return None
        path = r"cache\%s.png" % (str(time.time())[-5:])
        shot.save(path)
        return path

    def find_pic(self, template_path, zone="ALL", search_path: str = "",
                 delete_flag: int = 1, method=TM_CCOEFF_NORMED):
        if search_path:
            if not os.path.isfile(search_path):
                print("error: findpic 参数 search_path 为无效路径。")
        else:
            search_path = self.screenshot()
            if delete_flag in [0, 1]:
                delete_flag = 0
        search = imread(search_path)
        if zone == "ALL":
            (x1, y1, x2, y2) = (0, 0, 0, 0)
        else:
            (x1, y1, x2, y2) = zone
            (scx1, scy1), (scx2, scy2) = self.axis_zoom(x1, y1), self.axis_zoom(x2, y2)
            search = search[scy1:scy2, scx1:scx2]
        template = imread(template_path)
        tem_h, tem_w, num = template.shape
        if self.zoom == 1.0:
            pass
        elif self.zoom < 1.0:
            tem_w, tem_h = tem_w * self.zoom, tem_h * self.zoom
            template = resize(template, (int(tem_w), int(tem_h)))
        else:
            search_h, search_w, num = search.shape
            search = resize(search,
                            (int(search_w / self.zoom),
                             int(search_h / self.zoom)))
        match_res = matchTemplate(search, template, method)
        min_sim, max_sim, min_loc, max_loc = minMaxLoc(match_res)
        if (min_sim >= -0.6) and (max_sim <= 0.6):
            centre, sim = ((0, 0), 0)
        else:
            min_sim = min_sim * -1
            if max_sim >= min_sim:
                (rel_x, rel_y), sim = max_loc, max_sim
            else:
                (rel_x, rel_y), sim = min_loc, min_sim
            if self.zoom == 1.0:
                pass
            elif self.zoom < 1.0:
                (rel_x, rel_y) = (int(rel_x / self.zoom), int(rel_y / self.zoom))
            elif self.zoom > 1.0:
                (rel_x, rel_y) = (int(rel_x*self.zoom), int(rel_y*self.zoom))
            x = x1 + rel_x + int(tem_w / 2)
            y = y1 + rel_y + int(tem_h / 2)
            centre = (x, y)
        if not delete_flag:
            os.remove(search_path)
        return centre, sim

    def find_color(self, color_list, zone="ALL", search_path: str = "",
                   delete_flag: int = 1):
        if search_path:
            if not os.path.isfile(search_path):
                print("error: findcolor 参数 search_path 为无效路径。")
        else:
            search_path = self.screenshot()
            if delete_flag in [0, 1]:
                delete_flag = 0
        search = imread(search_path)
        if zone == "ALL":
            (x1, y1, x2, y2) = (0, 0, 0, 0)
        else:
            (x1, y1, x2, y2) = zone
            (scx1, scy1), (scx2, scy2) = self.axis_zoom(x1, y1), self.axis_zoom(x2, y2)
            search = search[scy1:scy2, scx1:scx2]
        search_h, search_w, num = search.shape
        hsv = cvtColor(search, COLOR_BGR2HSV)
        if not delete_flag:
            os.remove(search_path)
        for color in color_list.split("+"):
            if color == "red":
                [h_down_min, h_down_max], [h_up_min, h_up_max], s_min, s_max, v_min, v_max = color_zone[color]
                for rel_x in range(search_w):
                    for rel_y in range(search_h):
                        h, s, v = hsv[rel_y, rel_x]
                        # hex = ('{:02X}' * 3).format(r, g, b)
                        if h_down_min < h < h_down_max or h_up_min < h < h_up_max:
                            if s_min < s < s_max:
                                if s_min < s < s_max:
                                    rel_x = x1 + int(rel_x / self.zoom)
                                    rel_y = y1 + int(rel_y / self.zoom)
                                    return (rel_x, rel_y), True
            else:
                if color in ["orange", "yellow", "green", "cyan", "blue", "purple", "white", "black", "grey"]:
                    h_min, h_max, s_min, s_max, v_min, v_max = color_zone[color]
                else:
                    b, g, r = tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
                    h, s, v = rgb_to_hsv(r, g, b)
                    if h < 0.061:
                        h += 1
                    h_min, h_max, s_min, s_max, v_min, v_max = h*180-2, h*180+2, s*255-3, s*255+3, v-3, v+3
                for rel_x in range(search_w):
                    for rel_y in range(search_h):
                        h, s, v = hsv[rel_y, rel_x]
                        # hex = ('{:02X}' * 3).format(r, g, b)
                        if h_min < h < h_max:
                            if s_min < s < s_max:
                                if s_min < s < s_max:
                                    rel_x = x1 + int(rel_x / self.zoom)
                                    rel_y = y1 + int(rel_y / self.zoom)
                                    return (rel_x, rel_y), True
        return (0, 0), False

    def ocr(self, zone="ALL", search_path: str = "", mode: int = 0,
            delete_flag: int = 1):
        if self.OCR is None:
            print("error: ocr 未启用。")
            return 0
        if search_path:
            if not os.path.isfile(search_path):
                print("error: ocr 参数 search_path 为无效路径。")
        else:
            search_path = self.screenshot()
            if delete_flag in [0, 1]:
                delete_flag = 0
        search = imread(search_path)
        if zone == "ALL":
            (x1, y1) = (0, 0)
        else:
            (x1, y1, x2, y2) = zone
            (scx1, scy1), (scx2, scy2) = self.axis_zoom(x1, y1), self.axis_zoom(x2, y2)
            search = search[scy1:scy2, scx1:scx2]
        _list = self.OCR.output(search)
        if mode == 0:  # 简单单行识字
            if _list:
                text, gross, weight = "", 0, 0
                for i in _list:
                    tem_text = i[1][0]
                    tem_num = len(tem_text)
                    weight = tem_num * i[1][1]
                    gross += tem_num
                    text += tem_text
                _list = text, weight / gross
            else:
                _list = "", 0
        elif mode == 1:  # 分析文本及其位置形状
            if _list:
                _l = []
                for i in _list:
                    xy1, xy2 = ([u / self.zoom for u in i[0][0]],
                                [o / self.zoom for o in i[0][2]])
                    zone = ([x + y for x, y in zip([x1, y1], xy1)] +
                            [x + y for x, y in zip([x1, y1], xy2)])
                    _l += [[i[1][0], zone, i[1][1]]]
                _list = _l
            else:
                _list = [["", None, 0]]
        elif mode == 2:  # 输出原始结果
            pass
        else:
            print("error: ocr 参数 mode 无效模式。")
        if not delete_flag:
            os.remove(search_path)
        return _list

    def find_text(self, text, zone="ALL", search_path: str = "", delete_flag: int = 1):
        _list = self.ocr(zone, search_path=search_path, mode=1, delete_flag=delete_flag)
        for t in _list:
            if text in t[0]:
                return self.center(t[1])
        return False

    def match_text(self, text, zone="ALL", search_path: str = "", delete_flag: int = 1):
        _list = self.ocr(zone, search_path=search_path, mode=1, delete_flag=delete_flag)
        for t in _list:
            if text == t[0]:
                return self.center(t[1])
        return False

    def wait_pic(self, template_path, zone="ALL", wait_time=(1000, 10), similar=0.7):
        while 1:
            for i in range(wait_time[1]):
                p, s = self.find_pic(template_path, zone)
                if s >= similar:
                    return p
                else:
                    sleep(wait_time[0] / 1000)
            if self.soft.isforeground():
                raise RuntimeError("识别超时")
            else:
                self.soft.foreground()
                self.logger("切换顶层窗口")

    def wait_text(self, text, zone="ALL", wait_time=(1000, 10)):
        while 1:
            for i in range(wait_time[1]):
                _list = self.ocr(zone, mode=1)
                for t in _list:
                    if text in t[0]:
                        return self.center(t[1])
                else:
                    sleep(wait_time[0] / 1000)
            if self.soft.isforeground():
                raise RuntimeError("识别超时")
            else:
                self.soft.foreground()
                self.logger("切换顶层窗口")


if __name__ == '__main__':
    # env = Environment(1920, 1080)
    # result = ocr(search_path=r"D:\Kin\Pictures\court.png")
    # print(result)
    exe_path = r"tools\ocr\PaddleOCR-json_v.1.3.1\PaddleOCR-json.exe"
    abs_path = os.path.join(os.getcwd(), exe_path)
    print(abs_path)
    # print(os.path.exists(abs_path))
