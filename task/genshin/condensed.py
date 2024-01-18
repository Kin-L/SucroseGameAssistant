from tools.environment import *
from .genshin import Genshin


class Condensed(Genshin):
    def genshin_make_condensed(self):
        self.tp_fontaine1()
        keydown("W")
        wait(4300)
        keyup("W")
        wait(300)
        keydown("D")
        wait(500)
        keyup("D")
        wait(300)
        keydown("W")
        wait(1000)
        keyup("W")
        self.indicate("到达合成台")
        wait(300)
        press("F")
        wait(1000)
        click(960, 950)
        wait(1500)
        click(107, 188)
        wait(500)
        click(1339, 408)
        wait(600)
        if ocr((739, 178, 882, 227))[0] == "浓缩树脂":
            num = int(ocr((995, 886, 1029, 924))[0][-1])
            click(1618, 497)
            wait(600)
            fly = int(ocr((1025, 917, 1134, 941))[0].split("/")[0])
            cons = int(ocr((1162, 917, 1269, 941))[0].split("/")[0])
            self.indicate(f"当前已有:\n"
                          f"  晶核:{fly}个\n"
                          f"  原粹树脂:{cons}/160\n"
                          f"  浓缩树脂:{num}个")
            _n = min(int(cons/40), fly, 5-num)
            if _n:
                for i in range(_n):
                    click(1611, 671)
                    wait(400)
                ori = cons-_n*40
                cond = num+_n
                self.task["resin"] = [ori, cond]
                self.indicate(f"本次合成浓缩树脂{_n}个\n"
                              f"  原粹树脂: {cons} -> {ori}\n"
                              f"  浓缩树脂: {num} -> {cond}")
                click(1727, 1019)
                wait(800)
                click(1173, 786)
                wait(200)
            else:
                self.indicate("浓缩树脂数量达到上限")
        else:
            click(1618, 497)
            wait(600)
            self.indicate("无法合成浓缩树脂:缺少树脂或晶核")
        click(1836, 48)
        wait(2200)
