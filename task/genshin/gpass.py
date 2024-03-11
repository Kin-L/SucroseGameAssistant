from tools.environment import *
from .genshin import Genshin


class Pass(Genshin):
    def genshin_pass(self):
        self.home()
        if self.open_sub("纪行"):
            while 1:
                if "纪行" in ocr((134, 24, 199, 70)):
                    break
                else:
                    for i in range(4):
                        click(1889, 24)
                        wait(200)
            click(959, 50)
            wait(1500)
            if "领取" in ocr((1663, 939, 1824, 1018))[0]:
                click(1742, 977)
                wait(2500)
                click(829, 977)
                wait(2000)
                self.indicate("领取已完成的纪行任务")
            else:
                self.indicate("暂无纪行任务完成")
            click(860, 49)
            wait(1500)
            if "领取" in ocr((1663, 939, 1824, 1018))[0]:
                click(1742, 977)
                wait(3000)
                click(829, 977)
                wait(2000)
                self.indicate("领取纪行奖励")
            else:
                self.indicate("暂无纪行奖励可领取")
            self.home()
        else:
            self.indicate("纪行未开启")
