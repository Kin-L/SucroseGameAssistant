from tools.environment import *
from .genshin import Genshin


class Condensed(Genshin):
    def genshin_make_condensed(self):
        for i in range(3):
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
            wait(300)
            if "合成" in ocr((1205, 502, 1315, 578))[0]:
                self.indicate("到达合成台")
                break
            elif i == 2:
                self.indicate("合成树脂未知错误,重试多次")
                return True
            else:
                self.indicate(f"error:合成树脂未知错误,开始重试第{i+1}/2次") #
        pressto("F", 1000, ("合成", (124, 18, 215, 79), 0))
        if "浓缩树脂" in ocr((1270, 103, 1417, 158))[0]:
            fly = int(ocr((1025, 917, 1134, 941))[0].split("/")[0])
            cons = int(ocr((1162, 917, 1269, 941))[0].split("/")[0])
            clickto((1339, 408), 600, ("浓缩树脂", (739, 178, 882, 227), 0))
            num = int(ocr((996, 887, 1028, 924))[0].strip(" "))
            clickto((1618, 497), 600, ("合成", (823, 740, 938, 788), 0))
            self.indicate(f"当前已有:\n"
                          f"  晶核:{fly}个\n"
                          f"  原粹树脂:{cons}/160\n"
                          f"  浓缩树脂:{num}个")
            _n = min(int(cons/40), fly, 5-num)
            if _n:
                for i in range(_n-1):
                    click((1611, 671))
                    wait(400)
                ori = cons-_n*40
                cond = num+_n
                self.task["resin"] = [ori, cond]
                self.indicate(f"本次合成浓缩树脂{_n}个\n"
                              f"  原粹树脂: {cons} -> {ori}\n"
                              f"  浓缩树脂: {num} -> {cond}")
                click((1727, 1019))
                wait(800)
                click((1180, 755))
                wait(500)
            else:
                self.indicate("浓缩树脂数量达到上限")
        else:
            self.indicate("无法合成浓缩树脂:缺少树脂或晶核")
        self.home()
        return False
