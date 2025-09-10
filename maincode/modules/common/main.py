from maincode.modules.common.task.main import taskstart
from maincode.modules.common.widget import CommonPage
from maincode.modules.main import ModuleClass
from maincode.modules.template import SubConfigTemplate


class CommonConfig(SubConfigTemplate):
    """Common模块配置类，统一管理配置项"""
    ModuleKey: int = -1  # 模块唯一标识
    StartMode: int = 0
    CMDLine: str = ""
    WaitTimeBefore: int = 2         # 开始前等待时间
    StartProcess: str = ""          # 启动判断进程名
    StartOperateMode: int = 0       # 启动操作类型
    StartOperateContent: str = ""   # 启动操作内容
    StartRecogZone: str = ""        # 启动判断指定区域
    WaitTimeAfter: int = 2          # 开始后等待时间
    EndProcess: str = ""            # 结束判断进程名
    EndRecogMode: int = 0           # 结束判断类型
    EndRecogContent: str = ""       # 结束判断内容
    EndRecogZone: str = ""        # 结束判断指定区域
    Circular: str = ""              # 判断循环


class CommonClass(ModuleClass):
    """Common模块主类，实现框架接口"""
    ModuleNameCH = "通用模块"

    def __init__(self):
        self.ModuleKey = -1
        self.ModuleNameEN = "common"
        self.IconPath = 'resources/main/SGA/default.png'
        self.Config = CommonConfig  # 配置类关联
        self.Widget = CommonPage()  # UI界面关联
        self.Task = taskstart  # 任务入口关联
        self.LoadModule = False
        super().__init__()
