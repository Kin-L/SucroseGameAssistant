
def snowOther(self):
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
    if self.para["ProofReceive"]:
        self.ctler.clickChange((311, 580), zone=(283, 560, 366, 599))
        flag = False
        for _p in [(1272, 1025), (1512, 1027), (1052, 1029)]:
            self.ctler.click(_p)
            self.ctler.wait(0.5)
            pos = self.ctler.findtext("领取", (76, 1000, 220, 1045))
            if pos:
                self.ctler.clickChange(pos, zone=(76, 1000, 220, 1045))
                self.send("领取凭证奖励")
                self.ctler.clickChange(pos, zone=(809, 40, 1113, 147))
                flag = True
        if not flag:
            self.send("凭证奖励暂无可领取")
        self.ctler.pressTo("esc", "任务", (1458, 330, 1529, 379))
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
