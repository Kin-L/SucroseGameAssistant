from sgacode.tools.configclass import ConfigTool
from typing import List, Tuple
from sgacode.ui.control import ModuleStackPage


class ModuleClass:
    Count: int = 0  # 实例化的次数，即模组数量
    SignList: List[Tuple[str, str, int, str]] = []  # 每个实例的以下四项标识信息

    ModuleNum: int = 0  # 序号
    ModuleNameCH: str = ""  # 模组中文名（用于界面显示和提示信息）
    ModuleNameEN: str = ""  # 模组英文名（用于路径，关键字，函数名等，避免特殊字符）
    ModuleKey: int = 0  # 识别ID

    IconPath: str  # 图标路径
    Config: ConfigTool
    Widget: ModuleStackPage
    PageClass: type(ModuleStackPage)

    def __init__(self):
        super().__init__()
        # 每次实例化时，增加计数并将类添加到实例列表中
        ModuleClass.Count += 1
        ModuleClass.SignList.append((self.ModuleNameCH,
                                     self.ModuleNameEN, self.ModuleKey,
                                     self.IconPath))
