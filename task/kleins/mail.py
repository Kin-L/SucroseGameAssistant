from tools.environment import *
from ..default_task import Task


class Mail(Task):
    def __init__(self):
        super().__init__()

    def kleins_get_mail(self):
        if find_color("red", (472, 26, 521, 80))[1]:
            wait(500)
            click(472, 78)
            wait(1500)
            click(577, 809)
            wait(2000)
            click(1006, 885)
            wait(2000)
            click(1791, 122)
            self.indicate("领取邮件完成")
            wait(2000)
        else:
            self.indicate("暂无新邮件")
            wait(500)
            