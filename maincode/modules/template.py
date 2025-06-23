from maincode.tools.controls import palette, ScrollArea, Stack
from PyQt5.QtWidgets import QWidget, QFrame
from pydantic import BaseModel


class SubConfigTemplate(BaseModel):
    ConfigKey: str = ""
    ModuleKey: int
    ConfigName: str = "默认配置"
    Mute: bool = False
    SoftClose: bool = False
    Finished: int = 0
    SGAClose: bool = False


class ModuleStackPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setPalette(palette)
        self.srlist = ScrollArea(self, (0, 55, 210, 480))
        self.srlist.setFrameShape(QFrame.Shape(0))
        self.sksetting = Stack(self, (225, 0, 400, 515))

    def LoadWindow(self, *args):
        pass

    def SetWindow(self, config: dict, *args):
        pass

    def CollectConfig(self, *args) -> dict:
        pass
