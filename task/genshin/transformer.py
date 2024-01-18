from tools.environment import *
from .genshin import Genshin
import os


class Transformer(Genshin):
    def genshin_transformer(self):
        if not os.path.isfile(self.task['参量质变仪0']):
            self.indicate("error:\n  参量质变仪材料设置不正确")
            return True
        self.home()
        self.indicate("检查参量质变仪")
        self.open_sub("背包")
        wait(1500)
        self.check_overdue()
        click(1053, 48)
        wait(800)
        (x, y), val = find_pic(r"assets\genshin\picture\lit_tools\para_trans.png", (109, 113, 1275, 459))
        if val <= 0.8:
            self.indicate("参量质变仪（未找到/冷却中）")
            click(1840, 47)
            wait(1500)
        else:
            _t = ocr((x-58, y-55, x+58, y+55))[0]
            for i in ["天", "时", "分", "秒"]:
                if i in _t:
                    self.indicate("参量质变仪（未找到/冷却中）")
                    click(1840, 47)
                    wait(1500)
                    return 0
            self.indicate("参量质变仪可用")
            click(x, y)
            wait(800)
            (x, y), val = find_pic(r"assets\genshin\picture\lit_tools\para_retrieve.png", (1645, 971, 1769, 1058))
            if val >= 0.6:
                click(x, y)
                wait(1500)
            else:
                click(1840, 47)
                wait(1500)
            self.open_sub("冒险之证")
            click(300, 440)
            wait(800)
            click(537, 296)
            wait(800)
            self.tp_domain("堇色之庭")
            click(1669, 1009)
            wait(500)
            self.world()
            keydown("A")
            wait(2100)
            keyup("A")
            wait(500)
            keydown("W")
            wait(2100)
            keyup("W")
            wait(500)
            self.home()
            self.open_sub("背包")
            click(1053, 48)
            wait(800)
            (x, y), val = find_pic(r"assets\genshin\picture\lit_tools\para_trans.png", (109, 113, 1275, 459))
            click(x, y)
            wait(800)
            click(1694, 1022)
            wait(1500)
            click(1633, 549)
            wait(1000)
            press("F")
            wait(2000)
            for i in range(5):
                mat = self.task[f'参量质变仪{i}']
                if os.path.isfile(mat):
                    c = os.path.splitext(mat)[0]
                    c, b = os.path.split(c)
                    a = os.path.split(c)[1]
                    self.indicate("尝试添加材料:\n  " + b)
                    (x, y), val = find_pic(f"assets/genshin/picture/{a}/{a}.png", (456, 0, 1450, 94))
                    click(x, y)
                    wait(800)
                    (x, y), val = find_pic(mat, (104, 107, 1282, 955))
                    click(x, y)
                    wait(800)
                    click(454, 1021)
                    wait(800)
                    res = find_color("red", (1338, 979, 1560, 1056))[1]
                    if res:
                        self.indicate("参量质变仪还未装满")
                    else:
                        click(1703, 1020)
                        wait(800)
                        click(1178, 757)
                        wait(1000)
                        self.indicate("参量质变仪已装满")
                        break
                else:
                    self.indicate("参量质变仪未装满")
                    click(1840, 47)
                    wait(1500)
                    return True
            self.indicate("参量质变仪充能中")
            for i in range(15):
                wait(2000)
                pos, val = find_pic(r"assets\genshin\picture\acquire.png", (871, 242, 1050, 339))
                if val >= 0.6:
                    break
                elif i == 14:
                    self.indicate("等待参量质变仪使用超时(30s)\n")
                    return True
            click(961, 804)
            self.indicate("参量质变仪使用成功")
            self.home()
        return False
