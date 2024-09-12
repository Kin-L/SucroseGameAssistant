# -*- coding:gbk -*-
from tools.environment import *
from ..default_task import Task
import os


class Fight(Task):
    def __init__(self):
        super().__init__()
        
    def snow_fight(self):
        self.indicate("开始检查：感知扫荡")
        if self.task["感知互赠"] and find_color("yellow", (371, 465, 381, 475))[1]:
            click((326, 484))
            wait(2000)
            click((1780, 1030))
            wait(500)
            click((1780, 1030))
            wait(500)
            click((1780, 1030))
            wait(500)
            self.indicate(f"感知互赠完成")
            click((1674, 44))
            wait(2000)
        if self.task["每日配给"]:
            click((155, 576))
            wait(1500)
            click_pic(r"assets\snow\picture\supply.png", zone=(0, 251, 89, 624))
            wait(1500)
            if "每日物资配给箱" in ocr((176, 621, 558, 676))[0]:
                click((365, 651))
                wait(2000)
                click((1355, 768))
                wait(2000)
                self.indicate(f"每日物资配给箱 领取完成")
                click((1674, 44))
                wait(2000)
                click((1674, 44))
                wait(2000)
            else:
                self.indicate(f"每日物资配给箱 暂无")
                click((1674, 44))
                wait(2000)
        if self.task["使用试剂"]:
            self.indicate(f"检查限时试剂")
            while 1:
                click((1052, 33))
                wait(2500)
                sc = screenshot()
                pt = ocr((293, 312, 511, 379), sc)[0]
                pn = int(ocr((340, 530, 474, 578), sc)[0].replace(" ", "").split("/")[-1])
                if "无" not in pt and pn > 0:
                    os.remove(sc)
                    click((401, 451))
                    wait(800)
                    click((1285, 729))
                    wait(800)
                    click((1356, 837))
                    wait(2000)
                    click((1383, 502))
                    wait(2000)
                    self.indicate(f"使用限时试剂(中)")
                else:
                    yt = ocr((558, 309, 778, 378), sc)[0]
                    yn = int(ocr((602, 532, 735, 578), sc)[0].replace(" ", "").split("/")[-1])
                    os.remove(sc)
                    if "无" not in yt and yn > 0:
                        click((669, 454))
                        wait(800)
                        click((1285, 729))
                        wait(800)
                        click((1356, 837))
                        wait(2000)
                        click((1383, 502))
                        wait(2000)
                        self.indicate(f"使用限时试剂(大)")
                    else:
                        click((770, 962))
                        wait(1500)
                        self.indicate(f"暂无限时试剂可用")
                        break
        cons = int(ocr((901, 12, 1028, 60))[0].replace(" ", "")[:-4])

        if self.task["行动选择"] == 8:
            cons = int(ocr((901, 12, 1028, 60))[0].replace(" ", "")[:-4])
            if cons >= 30:
                click((1499, 538))
                wait(1000)
                wait_pic(r"assets\snow\picture\home.png", (1633, 6, 1718, 91))
                wait(500)
                click_text("材料")
                wait(3000)
                # click_text("深渊")
                click((1646, 359))
                wait(1500)
                click((1489, 1006))
                wait(2000)
                click((1280, 711))
                wait(1000)
                click((955, 826))
                wait(2500)
                while 1:
                    pos, sim = find_pic(r"assets\snow\picture\home.png", (1633, 6, 1718, 91))
                    if sim:
                        click(pos)
                        wait(2000)
                        self.indicate(f"感知扫荡：活动关卡")
                        break
                    click((932, 993))
                    wait(1500)
            else:
                self.indicate(f"感知不足30：{cons}")
        else:
            if cons >= 40:
                self.fight_common(self.task["行动选择"])
            else:
                self.indicate(f"感知不足40：{cons}")
        self.indicate("检查完成：感知扫荡")

    def fight_common(self, common, once=False):
        click((1728, 531))
        wait(2500)
        click((1682, 599))
        wait(1500)
        if common == 0:
            click((267, 495))
            wait(2500)
        elif common == 1:
            click((707, 497))
            wait(2500)
        elif common == 2:
            click((1165, 478))
            wait(2500)
        elif common == 3:
            click((1617, 502))
            wait(2500)
        elif common == 4:
            for t in range(3):
                roll((1002, 581), -35)
                wait(800)
                if click_text("冬之"):
                    break
            wait(2500)
        elif common == 5:
            for t in range(3):
                roll((1002, 581), -35)
                wait(800)
                if click_text("火之"):
                    break
            wait(2500)
            click((1037, 951))
            wait(500)
            click((1037, 951))
            wait(500)
            if not self.task["后勤选择"] in ocr((901, 12, 1028, 60))[0]:
                click((94, 935))
                wait(2000)
                click_text(self.task["后勤选择"])
                wait(1000)
                click((1823, 52))
                wait(800)
        elif common == 6:
            for t in range(3):
                roll((1002, 581), -35)
                wait(800)
                if click_text("心之"):
                    break
            wait(2500)
            click((1037, 951))
            wait(500)
            click((1037, 951))
            wait(500)
            if not self.task["活动后勤选择"] in ocr((149, 965, 313, 1006))[0]:
                click((95, 985))
                wait(2000)
                if not click_text(self.task["活动后勤选择"]):
                    roll((679, 494), -35)
                    wait(500)
                    click_text(self.task["活动后勤选择"])
                wait(1000)
                click((1826, 60))
                wait(800)
        elif common == 7:
            for t in range(3):
                roll((1002, 581), -35)
                wait(800)
                if click_text("兵之"):
                    break
            wait(2500)
        roll((1002, 581), -55)
        wait(500)
        click((872, 607))
        wait(1500)
        click((1489, 1006))
        wait(2000)
        if not once:
            click((1280, 711))
            wait(1000)
        click((955, 826))
        wait(2500)
        while 1:
            pos, sim = find_pic(r"assets\snow\picture\home.png", (1633, 6, 1718, 91))
            if sim:
                click(pos)
                wait(2000)
                break
            click((932, 993))
            wait(1500)
