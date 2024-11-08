from tools.environment import *
from .genshin import Genshin


class Team(Genshin):
    # 切换到标准队伍(1号队)
    def genshin_team(self):
        self.team_change_to(1)
        self.indicate("已切换至探索队伍")