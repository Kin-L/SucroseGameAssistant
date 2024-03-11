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
            if self.task["每周补给"][0]:
                click(725, 418)
                wait(1500)
                num = int(ocr((1602, 44, 1734, 78))[0].replace(" ", "")[:-4])
                if num >= 300:
                    self.indicate(f"补给点数: {num}")
                    for i in ["因", "能源", "礼物", self.task["每周补给"][1], self.task["每周补给"][2]]:
                        if click_text(i):
                            wait(2500)
                            if "兑换" in ocr((1214, 739, 1299, 790))[0]:
                                click(1371, 564)
                                wait(800)
                                click(1284, 775)
                                wait(2000)
                                click(192, 930)
                                self.indicate(f"兑换 {i}")
                                wait(2000)
                                num = int(ocr((1602, 44, 1734, 78))[0].replace(" ", "")[:-4])
                                if num >= 300:
                                    continue
                                else:
                                    self.indicate(f"补给点数不足300: {num}")
                                    break
                else:
                    self.indicate(f"补给点数不足300: {num}")
            click(296, 75)
            wait(1000)
