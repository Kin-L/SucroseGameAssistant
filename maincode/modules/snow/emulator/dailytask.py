from maincode.tools.main import logger


def snowDailyTask(self):
    self.send("开始检查：日常任务")
    if self.para["StoryEnable"]:
        self.ctler.clickChange((1690, 470), zone=(1552, 468, 1626, 515))
        self.ctler.wait(0.5)
        self.ctler.clickChange(target="个人", zone=(733, 812, 947, 891))
        _u = 0
        for i in self.para["StoryList"]:
            self.ctler.waitTo("行动", (357, 1000, 474, 1051))
            if i != "未选择":
                if i == "缄默":
                    _r = "默"
                elif i == "咎冠":
                    _r = "冠"
                elif i == "悖谬":
                    _r = "谬"
                elif i == "魔术师":
                    _r = "术师"
                elif i == "驰掣":
                    _r = "驰"
                elif i == "冥河代理人":
                    _r = "代理"
                else:
                    _r = i
                _f = False
                cl = False
                for o in range(8):
                    pos = self.ctler.findtext(_r, (0, 731, 1417, 858))
                    if pos:
                        (_x, _y) = self.ctler.convertR(pos)
                        _str = self.ctler.ocr((_x+247, 177,  _x+447, 233))[0]
                        if _str[-3] == "0":
                            self.send(f"今日已完成：角色 {i}")
                            _f = True
                        elif _str[-3] == "1":
                            pass
                        else:
                            cl = True
                        break
                    elif o == 7:
                        self.ctler.roll((1002, 581), 60000, True)
                        self.ctler.wait(0.8)
                        _f = True
                        self.send(f"未识别到角色: {i}")
                    else:
                        self.ctler.roll((1002, 581), -5620, True)
                        self.ctler.wait(0.8)
                if _f:
                    continue
                sc = self.ctler.screenshot()
                _str1 = self.ctler.ocr((1459, 27, 1540, 77), sc)[0]
                _str2 = _str1.split("/")[0].strip(" ")
                if _str2.isdigit():
                    _num = int(_str2)
                else:
                    self.send(f"记忆嵌片数量识别异常")
                    _path = self.ctler.SaveShot(sc, "")
                    logger.error(f"value: {_str1}")
                    logger.error(f"截图导出: {_path}")
                    return 0
                if _num == 0 and self.para["StoryUsePackage"] and _u < 2:
                    _u += 1
                    try:
                        self.ctler.clickChange((1566, 51), zone=(1547, 38, 1584, 69), wait_time=(800, 5))
                    except TimeoutError:
                        self.send(f"补嵌包不足")
                        break
                    self.ctler.wait(0.5)
                    if cl:
                        self.ctler.clickChange((1221, 626), zone=(934, 595, 990, 656))

                    self.ctler.clickChange((1457, 768), zone=(1354, 717, 1552, 817))
                    self.ctler.clickChange((1037, 951), zone=(809, 40, 1113, 147))
                elif _num > 2:
                    pass
                else:
                    self.send(f"记忆嵌片不足: {_num}")
                    break
                self.ctler.clickChange((_x, 900), zone=(858, 801, 1072, 875))
                if cl:
                    self.ctler.clickChange((1168, 718), zone=(875, 685, 945, 749))
                self.ctler.clickChange(target="开始", zone=(858, 801, 1072, 875))
                self.send(f"完成个人故事扫荡 {i}")
                self.ctler.pressTo("esc", "resources/snow/picture/home.png", (1504, 0, 1771, 117))
        self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
        self.ctler.wait(0.5)

    if self.para["ShopEnable"]:
        self.ctler.clickChange(target="商店", zone=(1756, 997, 1852, 1061))
        self.ctler.roll((1241, 380), -2000)
        self.ctler.wait(0.5)
        for i in self.para["ShopList"]:
            _f = False
            if "×" in i:
                i = i.split("×")[0]
                _f = True
            pos = self.ctler.findtext(i, (323, 213, 1860, 1003))
            if pos:
                self.ctler.clickChange(pos, zone=(1723, 981, 1840, 1044))
                if _f:
                    self.ctler.clickChange((1832, 853), zone=(1545, 834, 1582, 874))
                break
        self.ctler.clickChange((1782, 1014), zone=(1504, 0, 1771, 117))
        self.SnowHome(self)
        self.send("商店购物一次")
    if self.para["WeaponUp"]:
        self.ctler.clickChange(target="背包", zone=(1599, 994, 1692, 1063))
        self.ctler.wait(0.5)
        # 排序
        self.ctler.clickChange((73, 1025), zone=(50, 1011, 111, 1056))
        self.ctler.wait(0.5)
        self.ctler.clickChange((585, 327), zone=(625, 303, 681, 349))
        self.ctler.clickChange((585, 327), zone=(625, 303, 681, 349))
        self.ctler.clickChange((1316, 840), zone=(1302, 798, 1435, 893))
        # 升级
        self.ctler.clickChange((425, 191), zone=(50, 1011, 111, 1056))
        self.ctler.clickChange((985, 774), zone=(50, 1011, 111, 1056))
        self.ctler.clickChange((181, 300), zone=(123, 263, 248, 332))
        pos = self.ctler.waitTo("升级", (1691, 981, 1818, 1053))
        self.ctler.clickChange((1383, 717), zone=(123, 263, 248, 332))
        self.ctler.clickChange((119, 168), zone=(1341, 675, 1431, 766))
        self.ctler.clickChange(pos, zone=(1691, 981, 1818, 1053))
        self.send("武器升级一次")
        self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
        self.ctler.wait(0.5)
    if self.para["DailyTaskReceive"]:
        self.ctler.clickChange(target="任务", zone=(1440, 311, 1555, 403))
        self.ctler.wait(0.5)
        pos = self.ctler.findtext("领取", (55, 973, 197, 1023))
        if pos:
            self.ctler.clickChange(pos, zone=(18, 952, 242, 1040))
            self.ctler.clickTo(pos, "resources/snow/picture/home.png", (1504, 0, 1771, 117))
            self.send("领取日常奖励")
            self.ctler.wait(0.5)
        self.ctler.click((101, 257))
        self.ctler.wait(0.8)
        pos = self.ctler.findtext("领取", (55, 973, 197, 1023))
        if pos:
            self.ctler.clickChange(pos, zone=(18, 952, 242, 1040))
            self.ctler.clickTo(pos, "resources/snow/picture/home.png", (1504, 0, 1771, 117))
            self.send("领取周常奖励")
        self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
    if self.para["ProofReceive"] and self.ctler.findcolor("FFFF8B", (357, 540, 405, 577), tolerance=10):
        print(222)
        self.ctler.clickChange((311, 580), zone=(283, 560, 366, 599))
        for _p in [(1272, 1025), (1512, 1027), (1052, 1029)]:
            self.ctler.click(_p)
            self.ctler.wait(0.5)
            pos = self.ctler.findtext("领取", (76, 1000, 220, 1045))
            if pos:
                self.ctler.clickChange(pos, zone=(76, 1000, 220, 1045))
                self.send("领取凭证奖励")
                self.ctler.clickChange(pos, zone=(809, 40, 1113, 147))
        self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
    self.send("检查完成：日常任务")
