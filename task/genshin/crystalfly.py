from .genshin import Genshin
from tools.environment import *


class CatchFly(Genshin):
    def genshin_catch_fly(self):
        _t = True
        for i in range(5):
            if self.task[f"晶蝶{i}"]:
                _t = False
        if _t:
            self.indicate("请至少选择一个晶蝶点位")
            return True
        if self.task["晶蝶0"]:
            self.indicate("开始点位:化城郭左方")
            self.fly0()
            self.indicate("完成点位:化城郭左方")
        if self.task["晶蝶1"]:
            self.indicate("开始点位:阿如村上方")
            self.fly1()
            self.indicate("完成点位:阿如村上方")
        if self.task["晶蝶2"]:
            self.indicate("开始点位:舍身陷坑下方")
            self.fly2()
            self.indicate("完成点位:舍身陷坑下方")
        if self.task["晶蝶3"]:
            self.indicate("开始点位:塔拉塔海谷")
            self.fly3()
            self.indicate("完成点位:塔拉塔海谷")
        if self.task["晶蝶4"]:
            self.indicate("开始点位:稻妻平海砦")
            self.fly4()
            self.indicate("完成点位:稻妻平海砦")
        return False

    # 捉晶蝶-化城郭左方
    def fly0(self):
        self.home()
        self.tp_domain("缘觉塔")
        click((577, 692))
        wait(800)
        self.tp_point(0)
        keydown("S")
        for i in range(4):
            wait(300)
            press("F")
        keyup("S")
        wait(500)
        keydown("D")
        for i in range(4):
            wait(300)
            press("F")
        keyup("D")
        wait(500)
        keydown("S")
        wait(5000)
        keyup("S")
        wait(500)
        keydown("A")
        wait(1600)
        press("SPACE")
        wait(1600)
        keyup("A")
        wait(500)
        keydown("W")
        wait(300)
        keyup("W")
        wait(500)
        press("2")
        wait(800)
        press("E")
        wait(200)
        keydown("W")
        for i in range(6):
            wait(300)
            press("F")
        keyup("W")
        wait(500)
        keydown("A")
        wait(500)
        keyup("A")
        wait(300)
        # 捉晶蝶-活力之家下方
        self.home()
        self.tp_domain("赤金的城墟")
        click((1872, 34))
        wait(800)
        drag((960, 967), (0, -800))
        wait(500)
        click((1152, 739))
        wait(800)
        self.tp_point(0)
        wait(500)
        press("1")
        wait(500)
        press("1")
        wait(500)
        keydown("A")
        wait(2800)
        keyup("A")
        wait(500)
        keydown("S")
        wait(5400)
        keyup("S")
        wait(500)
        keydown("A")
        wait(2100)
        keyup("A")
        wait(500)
        keydown("W")
        for i in range(5):
            wait(300)
            press("F")
        wait(200)
        keyup("W")
        wait(500)

    # 捉晶蝶-阿如村上方
    def fly1(self):
        self.home()
        self.tp_domain("赤金的城墟")
        click((962, 738))
        wait(800)
        self.tp_point(0)
        keydown("D")
        wait(4700)
        keyup("D")
        wait(500)
        keydown("W")
        wait(6000)
        keyup("W")
        wait(500)
        keydown("D")
        wait(150)
        keyup("D")
        wait(500)
        keydown("W")
        wait(3900)
        press("SPACE")
        wait(400)
        press("F")
        wait(800)
        keyup("W")

    # 捉晶蝶-舍身陷坑下方
    def fly2(self):
        self.home()
        self.tp_domain("赤金的城墟")
        click((1872, 34))
        wait(800)
        drag((960, 967), (0, -800))
        wait(500)
        click((832, 732))
        wait(800)
        self.tp_point(0)
        keydown("W")
        wait(1300)
        keyup("W")
        wait(500)
        keydown("A")
        for i in range(7):
            wait(300)
            press("F")
        keyup("A")

    # 捉晶蝶-塔拉塔海谷
    def fly3(self):
        self.home()
        self.tp_domain("深潮的余响")
        click((1256, 526))
        wait(800)
        self.tp_point(1)
        keydown("D")
        wait(4500)
        keyup("D")
        wait(500)
        keydown("ctrl")
        wait(5500)
        keyup("ctrl")
        wait(500)
        keydown("W")
        for i in range(10):
            press("F")
            wait(200)
        keyup("W")
        wait(200)
        keydown("A")
        for i in range(10):
            press("F")
            wait(150)
        keyup("A")
        wait(500)

    # 捉晶蝶-稻妻平海砦
    def fly4(self):
        self.home()
        self.tp_domain("沉眠之庭")
        click((1139, 528))
        wait(800)
        self.tp_point(0)
        keydown("S")
        for i in range(12):
            wait(300)
            press("F")
        keyup("S")
        wait(500)
        keydown("D")
        for i in range(2):
            wait(300)
            press("F")
        keyup("D")
        wait(500)
        keydown("S")
        for i in range(5):
            wait(300)
            press("F")
        keyup("S")
        wait(500)
        keydown("A")
        for i in range(4):
            wait(300)
            press("F")
        keyup("A")
        wait(500)
        keydown("W")
        for i in range(5):
            wait(300)
            press("F")
        keyup("W")
        wait(500)
