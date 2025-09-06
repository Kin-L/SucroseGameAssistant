from .task.main import taskstart
from .widget import ClickerPage
from ..main import ModuleClass
from ..template import SubConfigTemplate


class ClickerConfig(SubConfigTemplate):
    ModuleKey: int = 4  # 模块标识

    # 触发配置
    DisableKey: str = ""  # 禁用/启用键
    TriggerMode: str = "长按模式"  # 触发模式
    TriggerKey: str = ""  # 触发热键

    # 连点配置
    ClickerMode: str = "连点模式"  # 连点模式
    ClickerKey: str = ""  # 连点键
    Interval: int = 0  # 间隔时间(ms)

    # 脚本配置
    ScriptName: str = ""  # 脚本名称
    RunNum: int = 0  # 运行次数


class ClickerClass(ModuleClass):
    """Clicker模块主类，实现框架接口"""
    def __init__(self):
        self.ModuleKey = 4
        self.ModuleNameCH = "连点器模块"
        self.ModuleNameEN = "clicker"
        self.IconPath = 'resources/main/SGA/default.png'
        self.Config = ClickerConfig  # 配置类关联
        self.Widget = ClickerPage()  # UI界面关联
        self.Task = taskstart  # 任务入口关联
        super().__init__()
