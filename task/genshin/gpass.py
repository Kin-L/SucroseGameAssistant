from tools.environment import *
from .genshin import Genshin


class Pass(Genshin):
    def genshin_pass(self):
        self.home()
        #打开纪行
        if click_pic(r"assets\genshin\picture\gpass.png",(117, 346, 742, 1052)):
            for i in range(10):
                if "纪行" in ocr((134, 24, 199, 70)) :
                    break
                else:
                    click((1781, 52))
                    wait(300)
                    click((1781, 52))
                    wait(300)

            #进入纪行任务界面
            for i in range(3):
                click((959, 50))
                wait(100)
                
            #领领取已完成的纪行任务
            if "领取" in ocr((1663, 939, 1824, 1018))[0]:
                click_text("领取" ,(1663, 939, 1824, 1018))
                wait(1500)
                self.indicate("领取已完成的纪行任务")
            else:
                self.indicate("暂无纪行任务完成")

            #领取纪行奖励
            click((860, 49))
            wait(1000)
            if "领取" in ocr((1663, 939, 1824, 1018))[0]:
                click_text("领取" ,(1663, 939, 1824, 1018))
                wait(1500)
                click((974,964))
                wait(1000)
                self.indicate("领取纪行奖励")
            else:
                self.indicate("暂无纪行奖励可领取")

            self.home()
        else:
            self.indicate("纪行未开启")
