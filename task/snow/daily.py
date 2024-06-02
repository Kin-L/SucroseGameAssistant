# -*- coding:gbk -*-
import os

from tools.environment import *
from ..default_task import Task


class Daily(Task):
    def __init__(self):
        super().__init__()

    def snow_daily(self):
        self.indicate("开始检查：日常周常")
        if self.task["个人故事"][0]:
            click((1728, 531))
            wait(2500)
            click((843, 848))
            wait(2000)
            _u = 0
            for i in self.task["个人故事"][2:]:
                if i != "未选择":
                    _num = int(ocr((1470, 38, 1540, 68))[0].replace(" ", "")[:-3])
                    if _num == 0 and self.task["个人故事"][1] and _u < 2:
                        _u += 1
                        click((1566, 51))
                        wait(2000)
                        click((1221, 626))
                        wait(800)
                        click((1420, 768))
                        wait(2000)
                        click((668, 66))
                        wait(1500)
                    elif _num > 2:
                        pass
                    else:
                        self.indicate(f"记忆嵌片不足: {_num}")
                        break
                    if i == "缄默":
                        _r = "默"
                    elif i == "咎冠":
                        _r = "冠"
                    elif i == "悖谬":
                        _r = "谬"
                    else:
                        _r = i
                    _f = False
                    for o in range(8):
                        pos = find_text(_r)
                        if pos:
                            click((pos[0], 900))
                            break
                        elif o == 7:
                            roll((1002, 581), 250)
                            wait(800)
                            _f = True
                            self.indicate(f"未识别到角色: {i}")
                        else:
                            roll((1002, 581), -25)
                            wait(800)
                    if _f:
                        continue
                    wait(2500)
                    click((1280, 711))
                    wait(1000)
                    click((955, 826))
                    wait(4000)
                    click((932, 993))
                    wait(1500)
                    self.indicate(f"完成个人故事扫荡 {i}")
            click((1674, 44))
            wait(2000)
        if self.task["拟境扫荡"]:
            click((1728, 531))
            wait(2500)
            click((288, 507))
            wait(1500)
            x, y = find_text("精神", (150, 770, 1779, 848))
            clickto((x, 462), 2000, (r"assets\snow\picture\imitate.png", (218, 863, 339, 968), 0.7))
            for _p in [(223, 253), (216, 394)]:
                click(_p)
                wait(1500)
                for i in range(4):
                    sc = screenshot()
                    if ("快速" in ocr((1351, 977, 1512, 1052), sc)[0] and
                            int(ocr((1791, 576, 1852, 611), sc)[0].replace(" ", "")[:-2]) > 0):
                        os.remove(sc)
                        click((1415, 999))
                        wait(2500)
                        click((1375, 773))
                        wait(2000)
                        self.indicate("拟境扫荡一次")
                    else:
                        os.remove(sc)
                        break
            if find_color("yellow", (188, 869, 195, 876))[1]:
                click((137, 914))
                wait(2000)
                click((1742, 1001))
                wait(2000)
                click((1742, 1001))
                wait(2000)
                self.indicate("领取评测奖励")
                click((1862, 87))
                wait(2000)
            click((1615, 48))
            wait(2000)
        if self.task["商店购物"][0]:
            print(self.task["商店购物"])
            click((1790, 1029))
            wait(2000)
            _f1 = False
            _f2 = False
            t1 = self.task["商店购物"][1]
            t2 = self.task["商店购物"][2]
            if self.task["商店购物"][1] == "芳烃塑料×3":
                t1 = "芳烃塑料"
                _f1 = True
            if self.task["商店购物"][2] == "芳烃塑料×3":
                t2 = "芳烃塑料"
                _f2 = True
            if not click_text(t1):
                click_text(t2)
                wait(1000)
                if _f2:
                    click((1832, 853))
                    wait(500)
            else:
                wait(1000)
                if _f1:
                    click((1832, 853))
                    wait(500)
            click((1710, 1011))
            wait(1500)
            click((1710, 1011))
            wait(1000)
            self.indicate("商店购物一次")
            click((1615, 48))
            wait(2000)
        if self.task["武器升级"]:
            click((1612, 1024))
            wait(2000)
            click((73, 1025))
            wait(2000)
            click((585, 327))
            wait(1000)
            click((585, 327))
            wait(1000)
            click((1316, 840))
            wait(1500)

            click((425, 191))
            wait(2000)
            click((985, 774))
            wait(2000)
            click((181, 300))
            wait(2000)
            click((1383, 717))
            wait(1500)
            click((119, 168))
            wait(1000)
            click((1701, 1015))
            wait(2000)
            click((1619, 49))
            wait(2000)
            self.indicate("武器升级一次")
            click((1619, 49))
            wait(2000)
        if self.task["领取日常"]:
            click((1582, 392))
            wait(1500)
            click((116, 157))
            wait(1500)
            if "领取" in ocr((55, 973, 197, 1023))[0]:
                click((131, 999))
                wait(2000)
                click((131, 999))
                wait(2000)
                self.indicate("领取日常奖励")
            for i in range(5):
                if "执行度" in ocr((311, 894, 430, 937))[0]:
                    break
                else:
                    click((119, 991))
                    wait(2000)
            click((101, 257))
            wait(1500)
            if "领取" in ocr((55, 973, 197, 1023))[0]:
                click((131, 999))
                wait(2000)
                click((131, 999))
                wait(2000)
                self.indicate("领取定期奖励")
            click((1674, 44))
            wait(2000)
        if self.task["领取凭证"] and find_color("yellow", (331, 481, 340, 491))[1]:
            click((269, 514))
            wait(2000)
            for _p in [(1272, 1025), (1512, 1027), (1052, 1029)]:
                click(_p)
                wait(800)
                if "领取" in ocr((76, 1000, 220, 1045))[0]:
                    click((149, 1015))
                    wait(2000)
                    click((149, 1015))
                    wait(2000)
                    self.indicate("领取凭证奖励")
            click((1674, 44))
            wait(2000)
        if self.task["活动每日"]:
            click((1502, 540))
            wait(1500)
            for i in range(10):
                if "剩余时间" in ocr((893, 128, 1016, 170))[0]:
                    self.indicate("领取活动每日")
                    click((473, 948))
                    wait(2500)
                    if click_text("领取", (3, 844, 319, 1072)):
                        wait(2500)
                        click((155, 921))
                        wait(1500)
                        self.indicate("领取已完成的活动任务")
                    else:
                        self.indicate("暂无已完成的活动任务可领取")
                    click((1668, 48))
                    wait(1500)
                    break
                elif "任务" in ocr((1552, 364, 1618, 409))[0]:
                    self.indicate("未识别到活动界面")
                    break
                else:
                    wait(1500)
        self.indicate("检查完成：日常周常")
