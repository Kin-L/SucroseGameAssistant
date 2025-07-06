from .image import SGAImage
from time import sleep, time
from maincode.tools.main import logger
from os import path
import cv2
import numpy as np


class Operate(SGAImage):
    WaitTime = (0.4, 10)
    MinSim = 0.9
    
    def clickChange(self, pos=None, target=None, zone=None, wait=WaitTime, minsim=MinSim):
        zone = self.convert(zone)
        # print(zone)
        sec, num = wait
        flag = False
        if target is None:
            scbef = self.screenshot(zone)
            bef = cv2.cvtColor(np.asarray(scbef), cv2.COLOR_BGR2GRAY)
            self.click(pos)
            while num > 0:
                sleep(sec)
                scaft = self.screenshot(zone)
                aft = cv2.cvtColor(np.asarray(), cv2.COLOR_BGR2GRAY)
                min_sim, max_sim, _, _ = cv2.minMaxLoc(cv2.matchTemplate(aft, bef, cv2.TM_CCOEFF_NORMED))
                min_sim *= -1
                sim = max_sim if max_sim >= min_sim else min_sim
                if sim < minsim:
                    if flag:
                        return True
                    else:
                        flag = True
                else:
                    self.click(pos)
                    num -= 1
            _path1 = self.SaveShot(scbef, "bef")
            _path2 = self.SaveShot(scaft, "aft")
            logger.error(f"截图导出bef: {_path1}")
            logger.error(f"截图导出aft: {_path2}")
        elif isinstance(target, str):
            if path.isfile(target) and path.exists(target):

                while num > 0:
                    fpos, sim = self.findpic(target, zone)
                    # print(fpos, sim)
                    if sim:
                        flag = True
                        self.click(fpos if pos is None else pos)
                    else:
                        if flag:
                            return True
                        num -= 1
                    sleep(sec)
            else:
                while num > 0:
                    fpos = self.findtext(target, zone)
                    # print(fpos)
                    if fpos:
                        flag = True
                        self.click(fpos if pos is None else pos)
                    else:
                        if flag:
                            return True
                        num -= 1
                    sleep(sec)
        raise TimeoutError("clickChange点击超时")

    def pressChange(self, key, target=None, zone=None, wait=WaitTime, minsim=MinSim):
        zone = self.convert(zone)
        sec, num = wait
        flag = False
        if target is None:
            bef = cv2.cvtColor(np.asarray(self.screenshot(zone)), cv2.COLOR_RGB2BGR)
            while num > 0:
                self.press(key)
                sleep(sec)
                aft = cv2.cvtColor(np.asarray(self.screenshot(zone)), cv2.COLOR_RGB2BGR)
                sim = cv2.minMaxLoc(cv2.matchTemplate(aft, bef, cv2.TM_CCOEFF_NORMED))[1]
                if sim < minsim:
                    flag = True
                else:
                    if flag:
                        return True
                    num -= 1
            _path1 = self.SaveShot(bef, "bef")
            _path2 = self.SaveShot(aft, "aft")
            logger.error(f"截图导出bef: {_path1}")
            logger.error(f"截图导出aft: {_path2}")
        elif isinstance(target, str):
            if path.isfile(target) and path.exists(target):
                while num > 0:
                    fpos, sim = self.findpic(target, zone)
                    if sim:
                        flag = True
                        self.press(key)
                    else:
                        if flag:
                            return True
                        num -= 1
                    sleep(sec)
            else:
                while num > 0:
                    fpos = self.findtext(target, zone)
                    if fpos:
                        flag = True
                        self.press(key)
                    else:
                        if flag:
                            return True
                        num -= 1
                    sleep(sec)
        raise TimeoutError("clickChange点击超时")

    def clickTo(self, pos, target: str, zone=None, wait=WaitTime):
        zone = self.convert(zone)
        sec, num = wait
        flag = False
        if path.isfile(target) and path.exists(target):
            while num > 0:
                fpos, sim = self.findpic(target, zone)
                if sim:
                    if flag:
                        return True
                    flag = True
                else:
                    self.click(pos)
                    num -= 1
                sleep(sec)
        else:
            while num > 0:
                fpos = self.findtext(target, zone)
                if fpos:
                    if flag:
                        return True
                    flag = True
                else:
                    self.click(pos)
                    num -= 1
                sleep(sec)
        raise TimeoutError("clickTo点击超时")

    def pressTo(self, key, target=None, zone=None, wait=WaitTime):
        zone = self.convert(zone)
        sec, num = wait
        flag = False
        if path.isfile(target) and path.exists(target):
            while num > 0:
                fpos, sim = self.findpic(target, zone)
                if sim:
                    if flag:
                        return True
                    flag = True
                else:
                    self.press(key)
                    num -= 1
                sleep(sec)
        else:
            while num > 0:
                fpos = self.findtext(target, zone)
                if fpos:
                    if flag:
                        return True
                    flag = True
                else:
                    self.press(key)
                    num -= 1
                sleep(sec)
        raise TimeoutError("pressTo点击超时")
    
    def waitTo(self, target: str, zone="WINDOW", wait=WaitTime):
        zone = self.convert(zone)
        sec, num = wait
        flag = False
        if path.isfile(target) and path.exists(target):
            while num > 0:
                fpos, sim = self.findpic(target, zone)
                if sim:
                    if flag:
                        return fpos, sim
                    flag = True
                else:
                    num -= 1
                sleep(sec)
        else:
            while num > 0:
                fpos = self.findtext(target, zone)
                if fpos:
                    if flag:
                        return fpos
                    flag = True
                else:
                    num -= 1
                sleep(sec)
        raise TimeoutError("waitTo点击超时")

    def tapChange(self, para=None, target=None, zone=None, wait=WaitTime, minsim=MinSim):
        zone = self.convert(zone)
        sec, num = wait
        flag = False
        if target is None:
            bef = cv2.cvtColor(np.asarray(self.screenshot(zone)), cv2.COLOR_BGR2GRAY)
            self.tap(para)
            while num > 0:
                sleep(sec)
                aft = cv2.cvtColor(np.asarray(self.screenshot(zone)), cv2.COLOR_BGR2GRAY)
                min_sim, max_sim, _, _ = cv2.minMaxLoc(cv2.matchTemplate(aft, bef, cv2.TM_CCOEFF_NORMED))
                min_sim *= -1
                sim = max_sim if max_sim >= min_sim else min_sim
                if sim < minsim:
                    if flag:
                        return True
                    else:
                        flag = True
                else:
                    self.tap(para)
                    num -= 1
            _path1 = self.SaveShot(bef, "bef")
            _path2 = self.SaveShot(aft, "aft")
            logger.error(f"截图导出bef: {_path1}")
            logger.error(f"截图导出aft: {_path2}")
        elif isinstance(target, str):
            if path.isfile(target) and path.exists(target):
                while num > 0:
                    fpos, sim = self.findpic(target, zone)
                    # print(fpos, sim)
                    if sim:
                        flag = True
                        self.tap(fpos if para is None else para)
                    else:
                        if flag:
                            return True
                        num -= 1
                    sleep(sec)
            else:
                while num > 0:
                    fpos = self.findtext(target, zone)
                    # print(fpos)
                    if fpos:
                        flag = True
                        self.tap(fpos if para is None else para)
                    else:
                        if flag:
                            return True
                        num -= 1
                    sleep(sec)
        raise TimeoutError("tapChange点击超时")

    def tapTo(self, para, target: str, zone=None, wait=WaitTime):
        zone = self.convert(zone)
        sec, num = wait
        flag = False
        if path.isfile(target) and path.exists(target):
            while num > 0:
                fpos, sim = self.findpic(target, zone)
                if sim:
                    if flag:
                        return True
                    flag = True
                else:
                    self.tap(para)
                    num -= 1
                sleep(sec)
        else:
            while num > 0:
                fpos = self.findtext(target, zone)
                if fpos:
                    if flag:
                        return True
                    flag = True
                else:
                    self.tap(para)
                    num -= 1
                sleep(sec)
        raise TimeoutError("clickTo点击超时")
