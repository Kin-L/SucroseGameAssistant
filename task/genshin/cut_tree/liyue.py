from tools.environment import *
from task.genshin.genshin import Genshin


class LiYue(Genshin):
    # 却砂木
    def sand_bearer(self):
        self.indicate("采集：却砂木×9")
        self.home()
        self.tp_domain("华池岩岫")
        click((1080, 332))
        wait(800)
        self.tp_point(0)
        keydown("A")
        wait(1500)
        keyup("A")
        wait(300)
        keydown("W")
        wait(4600)
        keyup("W")
        wait(300)
        keydown("A")
        wait(400)
        keyup("A")
        wait(300)
        press("Z")
        wait(500)

    # 竹节
    def bamboo(self):
        self.indicate("采集：竹节×30")
        self.home()
        self.tp_domain("无妄引咎密宫")
        click((609, 663))
        wait(800)
        self.tp_point(0)
        keydown("D")
        wait(7400)
        keyup("D")
        wait(300)
        keydown("W")
        wait(500)
        keyup("W")
        wait(300)
        press("Z")
        wait(300)