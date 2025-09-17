# 新星开拓

def snowXXKT(self):
    _list = self.ctler.ocr(mode=1)
    result = self.ctler.StrFind("难度选择", _list)
    if not result:
        self.send("请先进入新星开拓界面")
        return
    else:
        self.send("开始新星开拓")
    while 1:
        if "关卡" in self.ctler.ocr((1392, 96, 1517, 150))[0]:
            self.ctler.click((1738, 997))
            self.ctler.wait(3)
        else:
            self.ctler.click((955, 507))
            self.ctler.wait(0.5)
            self.ctler.click((961, 991))
            self.ctler.wait(0.5)
            continue
