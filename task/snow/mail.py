from tools.environment import *
from ..default_task import Task


class Mail(Task):
    def __init__(self):
        super().__init__()

    def snow_mail(self):
        self.indicate("开始检查:邮件")
        if find_color("yellow", (167, 443, 175, 455))[1]:
            click_change((113, 465), (91, 451, 131, 477))
            wait(500)
            pos = find_text("领取", (308, 967, 516, 1044))
            if pos:
                click_change((402, 1004), (308, 967, 516, 1044))
                wait_text("获得道具", (809, 40, 1113, 147))
                self.indicate("领取邮件完成")
                click_change(pos, (809, 40, 1113, 147))
            else:
                self.indicate("暂无新邮件")
            click_change((1668, 49), (1646, 24, 1697, 72))
            wait(500)
        else:
            self.indicate("暂无新邮件")
        self.indicate("检查完成:邮件")
            