from ..main import ModuleClass
from .widget import KleinPage
from maincode.modules.template import SubConfigTemplate


class KleinConfig(SubConfigTemplate):
    ModuleKey: int = 2  # 唯一模块标识

    # 基础配置
    PreLoad: bool = False  # 自动预下载
    Update: bool = False   # 自动更新
    AccountChoose: str = ""
    Server: int = 0        # 服务器选择（0=官服，1=其他）

    # 功能开关
    Fight: bool = False       # 作战/重游
    Dispatch: bool = False    # 线下采购
    Review: bool = False      # 战术回顾
    Market: bool = False      # 集市领取
    Recruit: bool = False     # 舍友访募
    Reward: bool = False      # 今日工作
    Network: bool = False     # 卡门商网
    Mail: bool = False        # 领取邮件
    Roll: bool = False        # 抽卡历史

    # 详细配置
    FightRetry: bool = False  # 再次重游
    FightLevel: int = 0       # 作战关卡
    DispatchRetry: bool = False  # 再次采购


class KleinClass(ModuleClass):
    def __init__(self):
        self.ModuleKey = 2
        self.ModuleNameCH = "环行旅舍"
        self.ModuleNameEN = "klein"
        self.IconPath = 'resources/klein/kleinicon.png'
        self.Config = KleinConfig
        self.Widget = KleinPage()
        self.Task = taskstart
        super().__init__()


def taskstart(self):
    self.send("香火 +1")
    self.send("功德 +1")
    self.send("扣1牢环复活")
