from maincode.tools.core.constant import spr

HomePic = spr.snow.HomePic


def snowOther(self):
    if self.para["DailyTaskReceive"]:
        self.ctler.clickChange(target="任务", zone=(1440, 311, 1555, 403))
        self.ctler.wait(0.5)
        pos = self.ctler.findtext("领取", (55, 973, 197, 1023))
        if pos:
            self.ctler.clickChange(pos, zone=(18, 952, 242, 1040))
            self.ctler.clickTo(pos, HomePic, (1504, 0, 1771, 117))
            self.send("完成:领取日常奖励")
            self.ctler.wait(0.5)
        self.ctler.click((101, 257))
        self.ctler.wait(0.8)
        pos = self.ctler.findtext("领取", (55, 973, 197, 1023))
        if pos:
            self.ctler.clickChange(pos, zone=(18, 952, 242, 1040))
            self.ctler.clickTo(pos, HomePic, (1504, 0, 1771, 117))
            self.send("完成:领取周常奖励")
        self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
    if self.para["ProofReceive"]:
        self.ctler.clickChange((311, 580), zone=(283, 560, 366, 599))
        flag = False
        for _p in [(1272, 1025), (1512, 1027), (1052, 1029)]:
            self.ctler.click(_p)
            self.ctler.wait(0.5)
            pos = self.ctler.findtext("领取", (76, 1000, 220, 1045))
            if pos:
                self.ctler.clickChange(pos, zone=(76, 1000, 220, 1045))
                self.ctler.clickChange(pos, zone=(809, 40, 1113, 147))
                flag = True
        if flag:
            self.send("完成:领取凭证奖励")
        else:
            self.send("凭证奖励暂无可领取")
        self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
    if self.para["ActivityDaily"]:
        try:
            self.ctler.clickChange((1462, 481), zone=(1402, 463, 1499, 505))
            self.ctler.waitTo(HomePic, (1633, 6, 1718, 91))
        except TimeoutError:
            self.send(f"活动未开启")
            self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
        else:
            self.ctler.wait(0.3)
            pos = self.ctler.findtext("任务")
            cpos = (655, 1007)  #
            vername = "灿海假日"
            if pos:
                self.send("识别到：任务")
                x, y = self.ctler.convertR(pos)
                self.ctler.clickChange(pos, zone=(x - 10, y - 10, x + 10, y + 10))
                pos = self.ctler.findtext("领取", (0, 605, 578, 1080))

            else:
                self.send(f"未识别到：任务，尝试备用点位：{vername}")
                self.ctler.click(cpos)
                self.ctler.wait(1)
                pos = self.ctler.findtext("领取", (0, 605, 578, 1080))
            if pos:
                self.ctler.clickChange(pos, zone=(76, 1000, 220, 1045))
                self.send("完成:领取活动奖励")
            else:
                self.send("未识别到可领取的活动奖励")
            self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
            self.ctler.wait(0.5)
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
        if not self.SnowHome(self):
            raise TimeoutError
        self.send(f"完成:收取信源断片")
