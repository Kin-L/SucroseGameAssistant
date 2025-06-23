
def snowOther(self):
    if self.para["Simulation"]:
        self.ctler.clickChange((1690, 470), zone=(1552, 468, 1626, 515))
        self.ctler.clickChange(target="特别", zone=(157, 464, 425, 560))
        pos = self.ctler.waitTo("精神", (150, 770, 1779, 848))
        x, y = self.ctler.convertR(pos)
        self.ctler.clickChange((x, 462), zone=(61, 998, 245, 1059))
        _cn = 0
        for _p in [(224, 253), (216, 394)]:
            self.ctler.click(_p)
            self.ctler.wait(0.8)
            for i in range(4):
                if _cn < 4 and "快速" in self.ctler.ocr((1351, 977, 1512, 1052))[0]:
                    self.ctler.clickChange((1415, 999), zone=(1358, 964, 1548, 1071))
                    self.ctler.wait(0.5)
                    self.ctler.clickChange((1375, 773), zone=(1358, 964, 1548, 1071))
                    self.ctler.wait(0.5)
                    _cn += 1
                    self.send("拟境扫荡一次")
                else:
                    break
        if self.ctler.findcolor("FFFF8B", (188, 869, 195, 876)):
            self.ctler.clickChange((137, 914), zone=(16, 51, 240, 128))
            self.ctler.clickChange((1742, 1001), zone=(1670, 971, 1830, 1022))
            self.send("领取评测奖励")
        self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
        self.ctler.wait(0.5)
    if self.para["ActivityDaily"]:
        if self.ctler.ocr((1378, 420, 1460, 457))[0]:
            self.ctler.clickChange((1499, 538), zone=(1402, 463, 1499, 505))
            self.ctler.waitTo("resources/snow/picture/home.png", (1504, 0, 1771, 117))
            self.ctler.wait(0.3)
            pos = self.ctler.findtext("任务")
            cpos = (607, 1031)  # 罅隙轨迹
            if pos:
                x, y = self.ctler.convertR(pos)
                self.ctler.clickChange(pos, zone=(x-10, y-10, x+10,  y+10))
                pos = self.ctler.findtext("领取", (0, 605, 578, 1080))

            else:
                self.ctler.click(cpos)
                self.ctler.wait(1)
                pos = self.ctler.findtext("领取", (0, 605, 578, 1080))
                if pos:
                    pass
                else:
                    self.send("未找到“任务”, 版本未适配")
                    self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
                    self.ctler.wait(0.5)
                    self.send("检查完成：日常周常")
                    return True
            self.ctler.clickChange(pos, zone=(76, 1000, 220, 1045))
            self.send("领取已完成的活动任务")
            self.ctler.clickChange(pos, zone=(809, 40, 1113, 147))
            self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
            self.ctler.wait(0.5)
        else:
            self.send(f"本期活动已关闭")
    if self.para["InfoFragment"]:
        self.ctler.clickChange((1629, 710), zone=(1570, 675, 1689, 751))
        self.ctler.pressTo("esc", "分析员", (1716, 156, 1811, 207), (0.4, 40))
        self.ctler.clickChange((1619, 1038), zone=(1514, 1022, 1611, 1067))
        self.ctler.wait(0.5)
        self.ctler.clickChange((1471, 765), zone=(1383, 733, 1547, 798))
        self.ctler.wait(0.8)
        if not self.ctler.findtext("分析员", (1716, 156, 1811, 207)):
            self.ctler.waitTo("谢谢", (852, 804, 1065, 875))
            self.ctler.clickChange((960, 838), zone=(852, 804, 1065, 875))
        self.SnowHome(self)
        self.send(f"收取信源断片完成")
