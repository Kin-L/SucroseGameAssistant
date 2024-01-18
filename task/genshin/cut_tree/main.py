from tools.environment import *
from .mondstadt import Mondstadt
from .liyue import LiYue
from .sumeru import Sumeru
from .inazuma import Inazuma
from .fontaine import Fontaine


class CutTree(Mondstadt, LiYue, Inazuma, Sumeru, Fontaine):
    def genshin_cut_tree(self):
        _freq, _list = self.task["砍树"]
        if not _freq:
            self.indicate("循环次数应大于0")
            return True
        _num = 0
        for i in _list:
            if i:
                _num += 1
        if not _num >= 5:
            self.indicate("为保证砍树完整循环，所选砍树任务种类应>=5")
            return True
        self.home()
        self.indicate("检查王树瑞佑。")
        self.open_sub("背包")
        wait(2000)
        self.check_overdue()
        click(1053, 48)
        wait(800)
        (x, y), val = find_pic(r"assets\genshin\picture\lit_tools\boon_elder_tree.png",
                               (110, 112, 1273, 805))
        if val < 0.75:
            self.indicate("没有找到道具：王树瑞佑")
            return True
        else:
            click(x, y)
            wait(800)
            if find_pic(r"assets\genshin\picture\lit_tools\unload.png",
                        (1637, 972, 1765, 1068))[1] >= 0.75:
                self.indicate("王树瑞佑已装备。")
                click(1840, 47)
                wait(1500)
            else:
                self.indicate("装备王树瑞佑。")
                click(1694, 1013)
                wait(1500)
        self.indicate(f"采集木材计划开始：\n"
                      f"  点位{_num}个\n"
                      f"  循环次数：{_freq}")
        for f in range(_freq):
            if _list[0]:
                self.birch()
            if _list[1]:
                self.cuihua()
            if _list[2]:
                self.pine()
            if _list[3]:
                self.sand_bearer()
            if _list[4]:
                self.bamboo()
            if _list[5]:
                self.fragrant()
            if _list[6]:
                self.fir()
            if _list[7]:
                self.yumemiru()
            if _list[8]:
                self.maple()
            if _list[9]:
                self.aralia_otogi()
            if _list[10]:
                self.otogi()
            if _list[11]:
                self.karmaphala_bright()
            if _list[12]:
                self.adhigama()
            if _list[13]:
                self.mountain_date()
            if _list[14]:
                self.mallow()
            if _list[15]:
                self.linden()
            if _list[16]:
                self.ash()
            if _list[17]:
                self.cypress()
            if _list[18]:
                self.torch()
        return False
