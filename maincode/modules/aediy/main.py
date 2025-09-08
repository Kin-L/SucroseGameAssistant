from os import startfile
from maincode.modules.main import ModuleClass
from maincode.modules.template import SubConfigTemplate, ModuleStackPage
from maincode.tools.classcheck import collect_scripts
from maincode.tools.core.constant import spr
from maincode.tools.sgaqt.buttons import Combobox, TransPicButton, PicButton
from maincode.tools.sgaqt.texts import Label


class DIYConfig(SubConfigTemplate):
    ModuleKey: int = 4  # 唯一模块标识
    ScriptName: list = ["", []]


class DIYClass(ModuleClass):
    ModuleNameCH = "自定义脚本"

    def __init__(self):
        self.ModuleKey = 4
        self.ModuleNameEN = "diy"
        self.IconPath = spr.SGAdefaultPic
        self.Config = DIYConfig
        self.Widget = DIYPage()
        self.Task = taskstart
        self.LoadModule = True
        super().__init__()


def taskstart(self):
    self.ctler.wait(1)
    self.send("扣1牢环复活")
    self.ctler.wait(1)
    self.send("香火 +1")
    self.ctler.wait(1)
    self.send("功德 +1")
    self.ctler.wait(1)


class DIYPage(ModuleStackPage):
    def __init__(self):
        super().__init__()
        self.script_dict: dict = {}
        Label(self, (0, 50, 180, 27), "脚本选择：")
        self.choose_clicker_mode = Combobox(self, (90, 50, 150, 30))
        # self.choose_clicker_mode.addItems(["按下模式", "连点模式", "脚本模式"])
        self.choose_clicker_mode.addItem("未加载")
        self.btrefresh = TransPicButton(
            self, (245, 50, 33, 33),
            spr.RefreshPic, (25, 25)
        )
        # 脚本文件夹按钮
        self.btjf = PicButton(self, (285, 50, 33, 33), spr.FoldPic, (25, 25))
        self.btrefresh.clicked.connect(self._loadscript)
        self.btjf.clicked.connect(lambda: startfile(f"{spr.WorkDir}/{spr.ScriptsDir}"))
        print(f"{spr.WorkDir}/{spr.ScriptsDir}")

    def CollectConfig(self) -> dict:
        name = self.choose_clicker_mode.currentText()
        return {
            "ScriptName": [name, self.script_dict[name]],
        }

    def SetWindow(self, config: dict, *args):
        name = config["ScriptName"][0]
        if name in self.choose_clicker_mode.items:
            self.choose_clicker_mode.setCurrentText(name)

    def LoadWidget(self, *args):
        self._loadscript()

    def _loadscript(self):
        self.choose_clicker_mode.clear()
        self.script_dict = collect_scripts()
        self.choose_clicker_mode.addItems(list(self.script_dict))
