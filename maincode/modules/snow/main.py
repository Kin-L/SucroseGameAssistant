from ..main import ModuleClass
from .widget import SnowPage
from .task.main import taskstart
from maincode.modules.template import SubConfigTemplate


class SnowConfig(SubConfigTemplate):
    ModuleKey: int = 3

    PreLoad: bool = False  # 自动预下载
    Update: bool = False  # 自动更新
    AccountChoose: str = ""

    Energy: bool = False  # 感知获取与消耗
    DailyTask: bool = False  # 日常任务
    Other: bool = False  # 其他任务
    GachaRecog: bool = False  # 共鸣记录识别

    Email: bool = False  # 领取邮件
    EnergyExchange: bool = False  # 感知互赠
    DailyEnergyPack: bool = False  # 每日配给
    EnergyDrug: bool = False  # 使用巴德尔试剂
    LevelsChoose: int = -1
    CommonLogistics: str = "底比斯小队"
    ActivityLogistics: str = "明夷小队"

    StoryEnable: bool = False  # 启用个人故事
    StoryUsePackage: bool = False  # 启用补嵌包
    StoryList: tuple[str, str, str, str] = ("未选择", "未选择", "未选择", "未选择")
    ShopEnable: bool = False  # 启用商店购物
    ShopList: tuple[str, str] = ("新手战斗记录", "初级职级认证")
    WeaponUp: bool = False  # 武器升级
    DailyTaskReceive: bool = False  # 领取日常
    ProofReceive: bool = False  # 领取凭证

    Simulation: bool = False  # 精神拟境
    ActivityDaily: bool = False  # 领取活动每日
    InfoFragment: bool = False  # 信源断片

    GachaList: tuple[bool, bool, bool, bool, bool, bool, bool] = (False, False, False, False, False, False, False)
    GachaOpenSheet: bool = False


class SnowClass(ModuleClass):
    def __init__(self):
        self.ModuleKey = 3
        self.ModuleNameCH = "尘白禁区"
        self.ModuleNameEN = "snow"
        self.IconPath = 'resources/snow/snowicon.png'
        self.Config = SnowConfig
        self.Widget = SnowPage()
        self.Task = taskstart
        super().__init__()
