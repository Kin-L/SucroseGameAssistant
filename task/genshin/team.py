from tools.environment import *
from .genshin import Genshin


class Team(Genshin):
    # 切换到标准队伍
    def genshin_team(self):
        self.home()
        self.open_sub("队伍配置")
        wait(1000)
        for i in range(30):
            res = find_pic("assets/genshin/picture/team.png", (37, 980, 115, 1058))
            if res[1] >= 0.6:
                self.indicate("进入到队伍配置界面")
                break
            elif i == 29:
                self.indicate("error:加载队伍配置界面超时\n")
                raise RuntimeError("原神:加载队伍配置界面超时")
            wait(500)
        click(77, 1016)
        wait(800)
        roll(580, 224, 55)
        wait(500)
        click(580, 224)
        wait(500)
        click(328, 1016)
        wait(800)
        click(1685, 1018)
        wait(500)
        click(1843, 47)
        self.world()
        press("1")
        wait(300)
        press("1")
        wait(300)
