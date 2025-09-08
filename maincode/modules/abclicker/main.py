from maincode.modules.abclicker.task.main import taskstart
from maincode.modules.abclicker.widget import ClickerPage
from maincode.modules.main import ModuleClass
from maincode.modules.template import SubConfigTemplate


class ClickerConfig(SubConfigTemplate):
    ModuleKey: int = 1  # 模块标识

    # 触发配置
    DisableKey: str = ""  # 禁用/启用键
    TriggerMode: str = "长按模式"  # 触发模式
    TriggerKey: str = ""  # 触发热键

    # 连点配置
    ClickerMode: str = "连点模式"  # 连点模式
    ClickerKey: str = ""  # 连点键
    Interval: float = 0.0  # 间隔时间(s)

    # 脚本配置
    ScriptName: list = ["", []]  # 脚本名称 脚本位置
    RunNum: int = 0  # 运行次数


class ClickerClass(ModuleClass):
    """Clicker模块主类，实现框架接口"""
    ModuleNameCH = "连点器"

    def __init__(self):
        self.ModuleKey = 1
        self.ModuleNameEN = "clicker"
        self.IconPath = 'resources/main/SGA/default.png'
        self.Config = ClickerConfig  # 配置类关联
        self.Widget = ClickerPage()  # UI界面关联
        self.Task = taskstart  # 任务入口关联
        self.LoadModule = True
        super().__init__()
