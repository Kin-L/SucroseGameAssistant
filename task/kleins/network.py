from tools.environment import *
from ..default_task import Task


class Network(Task):
    def __init__(self):
        super().__init__()

    def kleins_market_network(self):
        if ocr((1596, 888, 1774, 945))[0]:
            click((419, 162))
            wait(1500)
            click((1690, 220))
            wait(800)
            if "一键领取" in ocr((1596, 888, 1774, 945))[0]:
                click((1670, 917))
                self.indicate("已领取通讯波频")
                wait(800)
            else:
                self.indicate("暂无可领取通讯波频")
            click((1414, 225))
            wait(500)
            if "一键领取" in ocr((1596, 888, 1774, 945))[0]:
                click((1670, 917))
                self.indicate("已领取通讯补助")
                wait(1200)
                click((918, 70))
                wait(1200)
            else:
                self.indicate("暂无可领取通讯补助")
            click((301, 81))
            wait(1000)
        else:
            self.indicate("卡门商网未开启")
