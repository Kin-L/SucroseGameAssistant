from tools.environment import *
from ..default_task import Task


class Reward(Task):
    def __init__(self):
        super().__init__()

    def kleins_reward(self):
        if not find_color("red", (172, 415, 238, 470))[1]:
            self.indicate("暂无任务奖励")
            wait(500)
        else:
            click(145, 430)
            wait(1500)
            if find_color("red", (753, 146, 790, 189))[1]:
                click(727, 183)
                wait(1000)
                click(1340, 1009)
                wait(2000)
                click(941, 827)
                wait(2000)
                self.indicate("领取任务奖励")
            else:
                self.indicate("暂无任务奖励")
            click(296, 75)
            wait(1000)
