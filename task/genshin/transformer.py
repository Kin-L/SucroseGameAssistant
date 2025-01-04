from tools.environment import *
from .genshin import Genshin
import os , time


class Transformer(Genshin):
    def genshin_transformer(self):
        if self.task['参量质变仪1'] == 0 and self.task['参量质变仪2'] == 0 :
            self.indicate("error:\n  参量质变仪材料未设置")
            return True
        
        #检查参量质变仪时间
        self.home()
        self.indicate("检查参量质变仪")
        self.open_sub("背包")
        wait(1500)
        self.check_overdue()
        click((1053, 48))
        wait(800)
        (x, y), val = find_pic(r"assets\genshin\picture\lit_tools\para_trans.png", (109, 113, 1275, 459))
        if val <= 0.8:
            self.indicate("参量质变仪（未找到/冷却中）")
            self.home()
            return 0
        else:
            _t = ocr((x-58, y-55, x+58, y+55))[0]
            for i in ["天", "时", "分", "秒"]:
                if i in _t:
                    self.indicate("参量质变仪（未找到/冷却中）")
                    self.home()
                    return 0
            self.indicate("参量质变仪可用")

        click((x, y))
        wait(800)
        _p, val = find_pic(r"assets\genshin\picture\lit_tools\para_retrieve.png", (1645, 971, 1769, 1058))
        if val >= 0.6:
            click(_p)
            wait(1500)
        self.home()
        self.tp_fontaine1()
        self.home()
        self.open_sub("背包")
        click((1053, 48))
        wait(800)
        _p, val = find_pic(r"assets\genshin\picture\lit_tools\para_trans.png", (109, 113, 1275, 459))
        click(_p)
        wait(800)
        click((1694, 1022))
        wait(1500)
        click((1633, 549))
        wait(1000)
        
        #打开质变仪
        press("F")
        wait(2000)
        #材料目录
        meterial_pic_name = ["bugle","insignia","mask","raven_insignia","slime"]
        self.indicate("尝试添加第一种材料")
        for m in range(1,3):
            pic_dir1 = os.path.join("assets", "genshin", "picture", "develop_tools", meterial_pic_name[self.task["参量质变仪1"]] + f"{m}" + ".png")
            _p, val = find_pic(pic_dir1, (100,104,1279,815))
            if val <= 0.8:
                self.indicate(f"第一种材料品质{m}未找到")
                continue
            click(_p)
            wait(500)
            click((462,1026)) #点击最大数量
            wait(500)
            res = find_color("red", (1338, 979, 1560, 1056))[1]
            if res == 0:
                pass
            else:
                self.indicate("第一种材料当前品质数量不足，正在寻找更高品质")
        if res != 0:
            self.indicate("第一种材料不足，正在添加第二种材料")
            for n in range(1,3):
                pic_dir2 = os.path.join("assets", "genshin", "picture", "develop_tools", meterial_pic_name[self.task["参量质变仪2"]] + f"{n}" + ".png")    
                _p, val = find_pic(pic_dir2, (100,104,1279,815))
                if val <= 0.8:
                    self.indicate(f"第二种材料品质{n}未找到")
                    continue
                click(_p)
                wait(500)
                click((454, 1021))
                wait(500)
                res1 = find_color("red", (1338, 979, 1560, 1056))[1]
                if res1 == 0:
                    pass
                else:
                    self.indicate("第一种材料当前品质数量不足，正在寻找更高品质")
            if res1 == 0:
                self.indicate("材料不足，请重新设置材料")
                self.home()
                return 0
            
        self.indicate("参量质变仪已装满")
        click((1703, 1020))
        wait(800)
        click((1178, 757))
        wait(1000)
        self.indicate("参量质变仪充能中")
        press("4")
        for i in range(60):
            click((50,50))
            wait(500)
            pos, val = find_pic(r"assets\genshin\picture\acquire.png", (871, 242, 1050, 339))
            if val >= 0.6:
                break
            elif i == 60:
                self.indicate("参量质变仪充能超时\n")
                return True
        click((961, 804))
        self.indicate("参量质变仪使用成功")
        self.home()
        self.turn_world()
        press("1")
        self.home()
        return False
