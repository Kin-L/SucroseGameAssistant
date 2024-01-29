from tools.environment import *
from .genshin import Genshin


class Team(Genshin):
    # 切换到标准队伍
    def genshin_team(self):
        def open_team():
            self.home()
            self.open_sub("队伍配置")
            wait(1000)
            for i in range(30):
                if "队伍配置" in ocr((108, 23, 235, 77))[0]:
                    self.indicate("进入到队伍配置界面")
                    break
                elif i == 29:
                    self.indicate("error:加载队伍配置界面超时\n")
                    raise RuntimeError("原神:加载队伍配置界面超时")
                wait(500)
            wait(500)
        open_team()
        if not self.team_ready():
            self.indicate("处于联机/尘歌壶模式,更换队伍前进行状态初始化")
            click(1843, 47)
            self.world()
            self.tp_fontaine1()
            open_team()
        click(77, 1016)
        wait(800)
        roll(580, 224, 55)
        wait(500)
        click(580, 224)
        wait(500)
        click(328, 1016)
        wait(800)
        if self.team_ready():
            click(1843, 47)
            self.world()
            wait(300)
            press("1")
            wait(300)
            press("1")
            wait(300)
        else:
            click(1843, 47)
            self.world()
            wait(300)
            raise RuntimeError("处于联机模式,请退出联机后再试")

