from tools.environment import *
from ..default_task import Task


class Fight(Task):
    def __init__(self):
        super().__init__()
        
    def snow_fight(self):
        self.indicate("开始检查：感知扫荡")
        if self.task["感知互赠"]:
            click_change((326, 484), (317, 475, 340, 497))
            if "收" in ocr((1705, 993, 1880, 1066))[0]:
                click_text("收", (1705, 993, 1880, 1066))
                wait(2000)
            self.indicate(f"感知互赠完成")
            click_pic(r"assets\snow\picture\home.png", zone=(1504, 0, 1771, 117))
        if self.task["每日配给"]:
            click_change((147, 556), (151, 560, 217, 592))
            pos, sim = find_pic(r"assets\snow\picture\supply.png", zone=(0, 170, 93, 714))
            if sim:
                click_change(pos, (303, 62, 374, 94))
            else:
                raise RuntimeError("每日配给识别错误")
            if "每日" in ocr((176, 621, 558, 676))[0]:
                click_text("每日", (223, 606, 504, 692))
                click_change((1313, 773), (1269, 750, 1355, 798))
                self.indicate(f"每日物资配给箱 领取完成")
                click_change((1668, 49), (1646, 24, 1697, 72))
                click_pic(r"assets\snow\picture\home.png", zone=(1504, 0, 1771, 117))
            else:
                self.indicate(f"每日物资配给箱 暂无")
                click_pic(r"assets\snow\picture\home.png", zone=(1504, 0, 1771, 117))
        if self.task["使用试剂"]:
            self.indicate(f"检查限时试剂")
            click_change((1055, 35), (1031, 17, 1078, 53))
            sc = scshot()
            pt = ocr((293, 312, 511, 379), sc)[0]
            used = False
            if "无" not in pt and pt:
                click((401, 451))
                wait(600)
                click_to_text((1285, 729), "选择", (843, 512, 1099, 565))
                click_change((1356, 837), (1257, 804, 1413, 864))
                wait_text("获得道具", (809, 40, 1113, 147))
                press_to_text("esc", "任务", (1458, 330, 1529, 379))
                self.indicate(f"使用限时试剂(中)")
                used = True
            yt = ocr((558, 309, 778, 378), sc)[0]
            if "无" not in yt and yt:
                if used:
                    click_change((1055, 35), (1031, 17, 1078, 53))
                click((669, 454))
                wait(600)
                click_to_text((1285, 729), "选择", (843, 512, 1099, 565))
                click_change((1356, 837), (1257, 804, 1413, 864))
                wait_text("获得道具", (809, 40, 1113, 147))
                press_to_text("esc", "任务", (1458, 330, 1529, 379))
                self.indicate(f"使用限时试剂(大)")
                used = True
            if not used:
                click_change((1055, 35), (1031, 17, 1078, 53))
                self.indicate(f"暂无限时试剂可用")
            del sc
        sc = scshot()
        _str1 = ocr((901, 12, 1028, 60), sc)[0]
        _str2 = _str1.replace(" ", "")[:-4]
        try:
            cons = int(_str2)
        except ValueError:
            self.indicate(f"感知数量识别异常")
            _path = errorsc_save(sc)
            logger.error(f"截图导出: {_path}")
            logger.error(f"_str1: {_str1}")
            return 0
        if self.task["行动选择"] == 8:
            if cons >= 30:
                if ocr((1378, 420, 1460, 457))[0]:
                    click_change((1499, 538), (1402, 463, 1499, 505))
                    wait_pic(r"assets\snow\picture\home.png", (1633, 6, 1718, 91))
                    wait(300)
                    pos = find_text("材料")
                    cpos = (222, 340)  # 漠北寻风
                    if pos:
                        click_change(pos, (1732, 920, 1829, 1013))
                    else:
                        click(cpos)
                        wait(500)

                    wait_pic(r"assets\snow\picture\home.png", (1633, 6, 1718, 91))
                    wait(500)
                    pos = find_text("深渊")
                    cpos = (1372, 370)  # 漠北寻风
                    if pos:
                        click_change(pos, (1387, 945, 1599, 1075))
                        wait_text("速战", (1387, 945, 1599, 1075))
                    else:
                        click(cpos)
                        wait(1000)
                        if "深渊" in ocr((1394, 76, 1843, 179))[0]:
                            pass
                        else:
                            self.indicate("未找到“深渊”, 版本未适配")
                            click_pic(r"assets\snow\picture\home.png", zone=(1504, 0, 1771, 117))
                            wait(500)
                            self.indicate("检查完成：感知扫荡")
                            return True
                    click_text("速战", (1387, 945, 1599, 1075))
                    click((1280, 711))
                    wait(600)
                    click_text("开始", (858, 801, 1072, 875))
                    press_to_pic("esc", r"assets\snow\picture\home.png", (1504, 0, 1771, 117))
                    self.indicate(f"扫荡活动材料关卡完成")
                    click_pic(r"assets\snow\picture\home.png", zone=(1504, 0, 1771, 117))
                    wait(500)
                else:
                    self.indicate(f"本期活动已关闭")
            else:
                self.indicate(f"感知不足30：{cons}")
        else:
            if cons >= 40:
                self.fight_common(self.task["行动选择"])
            else:
                self.indicate(f"感知不足40：{cons}")
        self.indicate("检查完成：感知扫荡")

    def fight_common(self, common):
        click_change((1690, 470), (1552, 468, 1626, 515))
        pos = wait_text("行动", (1575, 538, 1844, 657))
        click_change(pos, (1575, 538, 1844, 657))
        wait_text("百足", (626, 782, 818, 868))
        if common == 0:
            click_change((267, 495), (64, 1003, 225, 1057))
            wait(800)
        elif common == 1:
            click_change((707, 497), (64, 1003, 225, 1057))
            wait(800)
        elif common == 2:
            click_change((1165, 478), (64, 1003, 225, 1057))
            wait(800)
        elif common == 3:
            click_change((1617, 502), (64, 1003, 225, 1057))
            wait(800)
        elif common == 4:
            for t in range(3):
                roll((1002, 581), -35)
                wait(800)
                pos = find_text("冬之", (0, 767, 1920, 891))
                if pos:
                    click_change(pos, (64, 1003, 225, 1057))
                    wait(800)
                    break
        elif common == 5:
            for t in range(3):
                roll((1002, 581), -35)
                wait(800)
                pos = find_text("火之", (0, 767, 1920, 891))
                if pos:
                    click_change(pos, (64, 1003, 225, 1057))
                    wait(800)
                    break
            pos = find_text("接收", (977, 954, 1094, 1011))
            if pos:
                click_change(pos, (966, 872, 1107, 1032))
                wait_text("获得道具", (809, 40, 1113, 147))
                press_to_text("esc", "小", (34, 959, 159, 1013))
            if not self.task["后勤选择"][:-2] in ocr((164, 923, 350, 982))[0]:
                click_text("小", (38, 890, 154, 1025))
                wait_text("小", (825, 10, 1111, 129))
                pos = find_text(self.task["后勤选择"][:-2], (158, 174, 903, 941))
                click_change(pos, (1488, 193, 1619, 237))
                click_change((1823, 52), (1811, 40, 1846, 79))
        elif common == 6:
            for t in range(3):
                roll((1002, 581), -35)
                wait(800)
                pos = find_text("心之", (0, 767, 1920, 891))
                if pos:
                    click_change(pos, (64, 1003, 225, 1057))
                    wait(800)
                    break
            pos = find_text("接收", (847, 988, 981, 1041))
            if pos:
                click_change(pos, (966, 872, 1107, 1032))
                wait_text("获得道具", (809, 40, 1113, 147))
                press_to_text("esc", "小", (32, 995, 142, 1039))
            if not (self.task["活动后勤选择"][:-2] in ocr((147, 962, 288, 1012))[0]):
                click_text("小", (38, 890, 154, 1025))
                wait_text("小", (825, 10, 1111, 129))
                print(self.task["活动后勤选择"][:-2])
                pos = find_text(self.task["活动后勤选择"][:-2], (158, 174, 903, 941))
                if not pos:
                    roll((679, 494), -35)
                    wait(500)
                    pos = find_text(self.task["活动后勤选择"][:-2], (158, 174, 903, 941))
                click_change(pos, (1488, 193, 1619, 237))
                click_change((1823, 52), (1811, 40, 1846, 79))
        elif common == 7:
            for t in range(3):
                roll((1002, 581), -35)
                wait(800)
                pos = find_text("兵之", (0, 767, 1920, 891))
                if pos:
                    click_change(pos, (64, 1003, 225, 1057))
                    wait(800)
                    break
        if not (common in [6, 7]):
            roll((1002, 581), -55)
            wait(500)
            click_change((872, 607), (1387, 945, 1599, 1075))
        wait_text("速战", (1387, 945, 1599, 1075))
        click_text("速战", (1387, 945, 1599, 1075))
        click((1280, 711))
        wait(600)
        click_text("开始", (858, 801, 1072, 875))
        press_to_pic("esc", r"assets\snow\picture\home.png", (1504, 0, 1771, 117))
        self.indicate(f"扫荡常规行动关卡完成")
        click_pic(r"assets\snow\picture\home.png", zone=(1504, 0, 1771, 117))
        wait(500)
