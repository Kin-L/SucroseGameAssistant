
def snowGuess(self):
    if "教学" not in self.ctler.ocr((1800, 207, 1874, 255))[0]:
        self.send("请先进入猜心对局界面，选择好模式并邀请少女完成")
        return
    else:
        self.send("开始猜心对局")
    # self.ctler.click((1129, 592))
    # self.ctler.wait(0.5)
    self.ctler.clickChange((1761, 989), zone=(1702, 965, 1829, 1036))
    self.ctler.wait(2)
    self.ctler.clickTo((1855, 853), "3", (1578, 1003, 1672, 1054))
    self.ctler.clickChange((1752, 62), zone=(1721, 37, 1779, 85))
    self.ctler.clickChange((1752, 62), zone=(1721, 37, 1779, 85))
    self.ctler.wait(1)
    _flag = 0
    while 1:
        txt = self.ctler.ocr((1656, 973, 1820, 1019))[0]
        if "看" in txt:
            self.ctler.wait(2)
        elif "出" in txt:
            if _flag:
                self.ctler.click((823, 767))
                self.ctler.wait(0.4)
                self.ctler.click((1104, 769))
                self.ctler.wait(0.4)
            self.ctler.click((958, 744))
            self.ctler.wait(0.4)
            self.ctler.click((1767, 952))
            self.ctler.wait(2)
            _flag = 1
            continue
        elif "再来" in txt:
            self.ctler.clickChange((1767, 997), zone=(1656, 973, 1820, 1019))
            self.ctler.wait(1)
        elif "确认" in txt:
            self.ctler.click((1427, 1006))
            self.ctler.wait(2)
        else:
            self.ctler.press("q")
            self.ctler.wait(0.3)
            self.ctler.press("w")
            self.ctler.wait(0.3)
            self.ctler.press("e")
            self.ctler.wait(0.3)
            self.ctler.click((1855, 853))
            self.ctler.wait(0.2)
        _flag = 0
