from tools.environment import *
from ..default_task import Task


class Market(Task):
    def __init__(self):
        super().__init__()

    def kleins_get_market(self):
        if not find_color("red", (304, 254, 377, 324))[1]:
            self.indicate("集市暂无可领取")
        else:
            click(283, 331)
            wait(1000)
            if find_color("red", (64, 308, 351, 384))[1]:
                click(198, 350)
                wait(500)
                if find_pic("assets/kleins/picture/market/daily.png", (399, 123, 768, 455))[1] >= 0.6:
                    click(590, 285)
                    wait(1200)
                    click(1257, 723)
                    wait(1200)
                    self.indicate("领取每日配给完成")
                    click(1054, 837)
                    wait(1200)
                else:
                    self.indicate("暂无每日配给可领取")
            else:
                self.indicate("暂无每日配给可领取")
            if find_color("red", (63, 468, 344, 546))[1]:
                click(203, 508)
                wait(1000)
                click(1487, 79)
                wait(2000)
                self.indicate("领取援外协议完成")
                click(1487, 79)
                wait(2000)
                if self.task["援外兑换"][0]:
                    if int(ocr((1663, 55, 1792, 95))[0].replace(" ", "")[:-4]) >= 200:
                        if click_text("外显记录"):
                            click(1128, 459)
                            wait(800)
                            click(1190, 657)
                            wait(2000)
                            click(205, 913)
                            self.indicate("兑换外显记录")
                            wait(2000)
                    if int(ocr((1663, 55, 1792, 95))[0].replace(" ", "")[:-4]) >= 200:
                        _t = self.task["援外兑换"][1]
                        _t0 = _t
                        if _t in ["遮阳伞", "小哑铃", "爱之歌", "手握式小风扇",
                                  "演唱会门票", "相机", "灯塔胶囊"]:
                            roll(1128, 459, 55)
                            wait(800)
                        elif _t == "须臾":
                            _t0 = "须"
                        click_text(_t)
                        wait(1500)
                        click(1128, 459)
                        wait(800)
                        click(1190, 657)
                        wait(2000)
                        self.indicate(f"兑换 {_t}")
                        click(205, 913)
                        wait(2000)
            else:
                self.indicate("暂无援外协议可领取")


            click(299, 77)
            wait(1000)
            