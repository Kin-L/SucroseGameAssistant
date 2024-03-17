from tools.environment import *
from .genshin import Genshin


class Team(Genshin):
    # 切换到标准队伍
    def genshin_team(self):
        def open_team():
            self.home()
            pos = find_text("队伍配置", (117, 346, 742, 1052))
            clickto(pos, 3000, ("队伍配置", (108, 23, 235, 77), 0))
            self.indicate("进入到队伍配置界面")
        open_team()
        if not self.isonline():
            self.indicate("处于联机/尘歌壶模式,更换队伍前进行状态初始化")
            self.tp_fontaine1()
            open_team()
            if self.isonline():
                raise RuntimeError("处于联机模式,请退出联机后再试")
        clickto((77, 1016), 800, ("管理队伍", (27, 17, 170, 75), 0))
        roll((580, 224), 55)
        wait(500)
        if "出战" in ocr((559, 192, 657, 256))[0]:
            self.home()
            return True
        click((580, 224))
        wait(500)
        click((328, 1016))
        wait(800)
        clickto((1557, 1020), 200, ("启用", (862, 514, 1057, 565), 0))
        self.turn_world()
        press("1")
        wait(300)
        press("1")
        wait(300)

