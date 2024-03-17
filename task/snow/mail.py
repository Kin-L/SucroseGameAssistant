# -*- coding:gbk -*-
from tools.environment import *
from ..default_task import Task


class Mail(Task):
    def __init__(self):
        super().__init__()

    def snow_mail(self):
        self.indicate("开始检查:邮件")
        if find_color("yellow", (136, 333, 143, 340))[1]:
            click((98, 365))
            wait(1500)
            click((402, 1004))
            wait(3000)
            click((955, 866))
            wait(1000)
            self.indicate("领取邮件完成")
            click((1674, 44))
            wait(2000)
        else:
            self.indicate("暂无新邮件")
            wait(500)
        self.indicate("检查完成:邮件")
            