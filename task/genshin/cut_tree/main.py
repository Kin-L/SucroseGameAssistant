# -*- coding:gbk -*-
from tools.environment import *
from .mondstadt import Mondstadt
from .liyue import LiYue
from .sumeru import Sumeru
from .inazuma import Inazuma
from .fontaine import Fontaine


class CutTree(Mondstadt, LiYue, Inazuma, Sumeru, Fontaine):
    def genshin_cut_tree(self):
        _freq = self.task["砍树次数"]
        if not _freq:
            self.indicate("循环次数应大于0")
            return True
        _num = 0
        for i in range(19):
            if self.task[f"砍树{i}"]:
                _num += 1
        if _num < 5:
            self.indicate("选择点位数应>=5以保障木材刷新循环")
            return True
        self.home()
        self.indicate("检查王树瑞佑。")
        self.open_sub("背包")
        wait(2000)
        self.check_overdue()
        click((1053, 48))
        wait(800)
        _p, val = find_pic(r"assets\genshin\picture\lit_tools\boon_elder_tree.png",
                               (110, 112, 1273, 805))
        if val < 0.75:
            self.indicate("没有找到道具：王树瑞佑")
            return True
        else:
            click(_p)
            wait(800)
            if find_pic(r"assets\genshin\picture\lit_tools\unload.png",
                        (1637, 972, 1765, 1068))[1] >= 0.75:
                self.indicate("王树瑞佑已装备。")
                click((1840, 47))
                wait(1500)
            else:
                self.indicate("装备王树瑞佑。")
                click((1694, 1013))
                wait(1500)
        self.indicate(f"采集木材计划开始：\n"
                      f"  点位{_num}个\n"
                      f"  循环次数：{_freq}")
        for f in range(_freq):
            if self.task["砍树0"]:
                self.birch()
            if self.task["砍树1"]:
                self.cuihua()
            if self.task["砍树2"]:
                self.pine()
            if self.task["砍树3"]:
                self.sand_bearer()
            if self.task["砍树4"]:
                self.bamboo()
            if self.task["砍树5"]:
                self.fragrant()
            if self.task["砍树6"]:
                self.fir()
            if self.task["砍树7"]:
                self.yumemiru()
            if self.task["砍树8"]:
                self.maple()
            if self.task["砍树9"]:
                self.aralia_otogi()
            if self.task["砍树10"]:
                self.otogi()
            if self.task["砍树11"]:
                self.karmaphala_bright()
            if self.task["砍树12"]:
                self.adhigama()
            if self.task["砍树13"]:
                self.mountain_date()
            if self.task["砍树14"]:
                self.mallow()
            if self.task["砍树15"]:
                self.linden()
            if self.task["砍树16"]:
                self.ash()
            if self.task["砍树17"]:
                self.cypress()
            if self.task["砍树18"]:
                self.torch()
        return False
