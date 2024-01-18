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
                click(1010, 712)
                wait(2000)
            else:
                self.indicate("暂无援外协议可领取")
            click(299, 77)
            wait(1000)
            