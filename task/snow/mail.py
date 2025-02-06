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
            click(pos)
            wait(500)
            self.indicate("领取邮件完成")
            press_to_text("esc", "任务", (1458, 330, 1529, 379))
            wait(500)
        else:
            self.indicate("暂无新邮件")
        self.indicate("检查完成:邮件")
            