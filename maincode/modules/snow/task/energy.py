from maincode.tools.main import logger


def FightCommon(self, common):
    self.ctler.clickChange((1690, 470), zone=(1552, 468, 1626, 515))
    pos = self.ctler.waitTo("行动", (1575, 538, 1844, 657))
    self.ctler.clickChange(pos, zone=(1575, 538, 1844, 657))
    self.ctler.waitTo("百足", (626, 782, 818, 868))
    if common == 0:
        self.ctler.clickChange((267, 495), zone=(64, 1003, 225, 1057))
        self.ctler.wait(0.8)
    elif common == 1:
        self.ctler.clickChange((707, 497), zone=(64, 1003, 225, 1057))
        self.ctler.wait(0.8)
    elif common == 2:
        self.ctler.clickChange((1165, 478), zone=(64, 1003, 225, 1057))
        self.ctler.wait(0.8)
    elif common == 3:
        self.ctler.clickChange((1617, 502), zone=(64, 1003, 225, 1057))
        self.ctler.wait(0.8)
    elif common == 4:
        for t in range(3):
            self.ctler.roll((1002, 581), -3500)
            self.ctler.wait(0.8)
            pos = self.ctler.findtext("冬之", (0, 767, 1920, 891))
            if pos:
                self.ctler.clickChange(pos, zone=(64, 1003, 225, 1057))
                self.ctler.wait(0.8)
                break
    elif common == 5:
        for t in range(3):
            self.ctler.roll((1002, 581), -3500)
            self.ctler.wait(0.8)
            pos = self.ctler.findtext("火之", (0, 767, 1920, 891))
            if pos:
                self.ctler.clickChange(pos, zone=(64, 1003, 225, 1057))
                self.ctler.wait(0.8)
                break
        if not self.para["CommonLogistics"][:-2] in self.ctler.ocr((164, 923, 350, 982))[0]:
            pos = self.ctler.waitTo("小", (38, 890, 154, 1025))
            self.ctler.clickChange(pos, zone=(829, 12, 1101, 130))
            self.ctler.waitTo("小", (825, 10, 1111, 129))
            pos = self.ctler.findtext(self.para["CommonLogistics"][:-2], (158, 174, 903, 941))
            self.ctler.clickChange(pos, zone=(1488, 193, 1619, 237))
            self.ctler.clickChange((1823, 52), zone=(1811, 40, 1846, 79))
        pos = self.ctler.findtext("接收", (977, 954, 1094, 1011))
        if pos:
            self.ctler.clickChange(pos, zone=(966, 872, 1107, 1032))
            self.ctler.waitTo("获得道具", (809, 40, 1113, 147))
            self.ctler.pressTo("esc", "小", (34, 959, 159, 1013))
    elif common == 6:
        for t in range(3):
            self.ctler.roll((1002, 581), -3500)
            self.ctler.wait(0.8)
            pos = self.ctler.findtext("心之", (0, 767, 1920, 891))
            if pos:
                self.ctler.clickChange(pos, zone=(64, 1003, 225, 1057))
                self.ctler.wait(0.8)
                break
        if not (self.para["ActivityLogistics"][:-2] in self.ctler.ocr((147, 962, 288, 1012))[0]):
            pos = self.ctler.waitTo("小", (38, 890, 154, 1025))
            self.ctler.clickChange(pos, zone=(829, 12, 1101, 130))
            self.ctler.waitTo("小", (825, 10, 1111, 129))
            print(self.para["ActivityLogistics"][:-2])
            pos = self.ctler.findtext(self.para["ActivityLogistics"][:-2], (158, 174, 903, 941))
            if not pos:
                self.ctler.roll((679, 494), 20000)
                self.ctler.wait(0.5)
                for i in range(5):
                    pos = self.ctler.findtext(self.para["ActivityLogistics"][:-2], (158, 174, 903, 941))
                    if pos:
                        break
                    self.ctler.roll((679, 494), -2500)
                    self.ctler.wait(0.5)
                else:
                    self.send("未找到目标后勤")
                    self.ctler.pressTo("esc", "resources/snow/picture/home.png", (1504, 0, 1771, 117))
                    return 0
            self.ctler.clickChange(pos, zone=(1488, 193, 1619, 237))
            self.ctler.clickChange((1823, 52), zone=(1811, 40, 1846, 79))
        pos = self.ctler.findtext("接收", (847, 988, 981, 1041))
        if pos:
            self.ctler.clickChange(pos, zone=(966, 872, 1107, 1032))
            self.ctler.waitTo("获得道具", (809, 40, 1113, 147))
            self.ctler.pressTo("esc", "小", (32, 995, 142, 1039))
    elif common == 7:
        for t in range(3):
            self.ctler.roll((1002, 581), -3500)
            self.ctler.wait(0.8)
            pos = self.ctler.findtext("兵之", (0, 767, 1920, 891))
            if pos:
                self.ctler.clickChange(pos, zone=(64, 1003, 225, 1057))
                self.ctler.wait(0.8)
                break
    if not (common in [6, 7]):
        self.ctler.roll((1002, 581), -5500)
        self.ctler.wait(0.5)
        self.ctler.clickChange((872, 607), zone=(1387, 945, 1599, 1075))
    pos = self.ctler.waitTo("速战", (1387, 945, 1599, 1075))
    self.ctler.clickChange(pos, zone=(861, 804, 1057, 871))
    self.ctler.wait(0.6)
    self.ctler.click((1280, 711))
    self.ctler.wait(0.6)
    self.ctler.clickChange(target="开始", zone=(858, 801, 1072, 875))
    self.ctler.wait(0.5)
    self.ctler.pressTo("esc", "任务", (1455, 324, 1533, 380))
    self.ctler.wait(0.5)


def snowEnergy(self):
    if self.para["Email"]:
        self.ctler.clickChange((113, 465), zone=(91, 451, 131, 477))
        self.ctler.wait(0.5)
        pos = self.ctler.findtext("领取", (308, 967, 516, 1044))
        self.ctler.click(pos)
        self.ctler.wait(0.5)
        self.send("完成:领取邮件完成")
        self.ctler.pressTo("esc", "任务", (1455, 324, 1533, 380))
        self.ctler.wait(0.5)
    if self.para["EnergyExchange"]:
        self.ctler.clickChange((326, 484), zone=(317, 475, 340, 497))
        self.ctler.wait(0.5)
        if "收" in self.ctler.ocr((1705, 993, 1880, 1066))[0]:
            self.ctler.clickChange(target="收", zone=(1705, 993, 1880, 1066))
            self.ctler.wait(2)
            self.send(f"完成:感知互赠")
        # assert 0
        self.ctler.pressTo("esc", "任务", (1455, 324, 1533, 380))
    if self.para["DailyEnergyPack"]:
        self.ctler.clickChange((147, 556), zone=(151, 560, 217, 592))
        pos, sim = self.ctler.findpic("resources/snow/picture/supply.png", zone=(0, 170, 93, 714))
        if sim:
            self.ctler.clickChange(pos, zone=(303, 62, 374, 94))
        else:
            raise ValueError("每日配给识别错误")
        if "每日" in self.ctler.ocr((176, 621, 558, 676))[0]:
            pos = self.ctler.findtext("每日", (223, 606, 504, 692))
            if pos:
                self.ctler.clickChange(pos, zone=(653, 516, 759, 613))
                self.ctler.clickChange(target="购买", zone=(1243, 735, 1402, 819))
                self.send(f"完成:领取每日物资配给箱")
            self.ctler.pressTo("esc", "任务", (1455, 324, 1533, 380))
        else:
            self.send(f"每日物资配给箱 暂无")
            self.ctler.pressTo("esc", "任务", (1455, 324, 1533, 380))
    if self.para["EnergyDrug"]:
        self.ctler.clickChange((1055, 35), zone=(1031, 17, 1078, 53))
        sc = self.ctler.screenshot()
        pt = self.ctler.ocr((293, 312, 511, 379), sc)[0]
        used = False
        if "无" not in pt and pt:
            self.ctler.click((401, 451))
            self.ctler.wait(0.6)
            self.ctler.clickTo((1285, 729), "选择", (843, 512, 1099, 565))
            self.ctler.clickChange((1356, 837), zone=(1257, 804, 1413, 864))
            self.ctler.pressTo("esc", "任务", (1455, 324, 1533, 380))
            self.send(f"使用限时试剂(中)")
            used = True
        yt = self.ctler.ocr((558, 309, 778, 378), sc)[0]
        if "无" not in yt and yt:
            if used:
                self.ctler.clickChange((1055, 35), zone=(1031, 17, 1078, 53))
            self.ctler.click((669, 454))
            self.ctler.wait(0.6)
            self.ctler.clickTo((1285, 729), "选择", (843, 512, 1099, 565))
            self.ctler.clickChange((1356, 837), zone=(1257, 804, 1413, 864))
            self.ctler.pressTo("esc", "任务", (1455, 324, 1533, 380))
            self.send(f"使用限时试剂(大)")
            used = True
        if not used:
            self.ctler.clickChange((1055, 35), zone=(1031, 17, 1078, 53))
            self.send(f"暂无限时试剂可用")

    def ReadCons():
        _sc = self.ctler.screenshot()
        _str1 = self.ctler.ocr((901, 12, 1028, 60), _sc)[0]
        _str2 = _str1.replace(" ", "")[:-4]
        if _str2.isdigit():
            return int(_str2)
        else:
            self.send(f"感知数量识别异常")
            _path = self.ctler.SaveShot(_sc, "")
            logger.error(f"截图导出: {_path}")
            logger.error(f"value: {_str1}")
            return 0

    if self.para["LevelsChoose"] == 8:
        while 1:
            cons = ReadCons()
            if cons < 30:
                self.send(f"感知剩余：{cons}")
                break
            if self.ctler.ocr((1378, 420, 1460, 457))[0]:
                try:
                    self.ctler.clickChange((1499, 538), zone=(1402, 463, 1499, 505))
                    self.ctler.waitTo("resources/snow/picture/home.png", (1633, 6, 1718, 91))
                except TimeoutError:
                    self.send(f"活动未开启")
                    break
                self.ctler.wait(0.3)
                pos = self.ctler.findtext("材料")
                cpos = (246, 621)  # 备用点位
                vername = "合题诗篇"
                if pos:
                    self.send("识别到：材料")
                    self.ctler.clickChange(pos, zone=(1732, 920, 1829, 1013))
                else:
                    self.send(f"未识别到：材料，尝试备用点位：{vername}")
                    self.ctler.click(cpos)
                    self.ctler.wait(0.5)
                self.ctler.waitTo("resources/snow/picture/home.png", (1633, 6, 1718, 91))
                self.ctler.wait(0.5)
                pos = self.ctler.findtext("深渊")
                cpos = (1339, 320)  # 备用点位
                if pos:
                    self.send("识别到：深渊")
                    self.ctler.clickChange(pos, zone=(1387, 945, 1599, 1075))
                else:
                    self.send(f"未识别到：深渊，尝试备用点位：{vername}")
                    self.ctler.click(cpos)
                    self.ctler.wait(1)
                    if "深渊" in self.ctler.ocr((1394, 76, 1843, 179))[0]:
                        pass
                    else:
                        self.send("未找到“深渊”, 版本未适配")
                        self.ctler.clickChange(target="resources/snow/picture/home.png", zone=(1504, 0, 1771, 117))
                        self.ctler.wait(0.5)
                        self.send("检查完成：感知扫荡")
                        return True
                pos = self.ctler.findtext("速战", (1387, 945, 1599, 1075))
                self.ctler.clickChange(pos, zone=(858, 801, 1072, 875))
                self.ctler.wait(0.6)
                self.ctler.click((1280, 711))
                self.ctler.wait(0.6)
                self.ctler.clickChange(target="开始", zone=(858, 801, 1072, 875))
                self.send(f"完成:扫荡 活动材料关卡")
                self.ctler.wait(0.5)
                self.ctler.pressTo("esc", "任务", (1455, 324, 1533, 380))
                self.ctler.wait(0.5)
            else:
                self.send(f"本期活动已关闭")

        self.send(f"扫荡活动材料关卡完成")
    else:
        while 1:
            cons = ReadCons()
            if cons < 40:
                self.send(f"感知剩余：{cons}")
                break
            FightCommon(self, self.para["LevelsChoose"])
        _str = ["通用银", "角色经验素材", "武器经验素材",
                "武器突破素材", "角色神经素材", "后勤获取",
                "活动后勤获取", "活动武器获取",
                "活动材料关卡"][self.para["LevelsChoose"]]
        self.send(f"完成:扫荡 {_str}")
