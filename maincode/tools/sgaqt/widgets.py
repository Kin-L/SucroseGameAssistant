from typing import Tuple, Union
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QPixmap, QIcon, QColor
from PyQt5.QtWidgets import QWidget, QStackedWidget, QFrame
from qfluentwidgets import SmoothScrollArea

from maincode.tools.core.constant import spr
from maincode.tools.sgaqt.texts import Label, Picture, Line, TipsButton
from maincode.tools.sgaqt.buttons import Check, Combobox

palette = QPalette()
palette.setColor(QPalette.Background, QColor(255, 255, 255))
int4 = Tuple[int, int, int, int]


class Widget(QWidget):
    def __init__(self, widget: Union[QWidget, None] = None, location: Union[int4, None] = None):
        super().__init__(widget)
        if location is not None:
            self.setGeometry(*location)
        self.setPalette(palette)


class ScrollArea(SmoothScrollArea):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        self.setGeometry(*location)
        self.setWidgetResizable(True)


class Stack(QStackedWidget):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        self.setGeometry(*location)


class StateSigh(QWidget):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        self.setGeometry(*location)
        self.setPalette(palette)
        self.rightpic = QPixmap(spr.RightPic)
        self.stoppic = QPixmap(spr.StopPic)
        self.errorpic = QPixmap(spr.ErrorPic)
        self.righttext = "正常运行"
        self.stoptext = "手动终止"
        self.errortext = "运行异常"
        self.light = Picture(self, (0, 3, 25, 25), self.rightpic)
        self.label = Label(self, (30, 0, 65, 30), self.righttext)

    def SetState(self, mode: int):
        if mode == 0:
            self.light.setPixmap(self.rightpic)
            self.label.setText(self.righttext)
        elif mode == 1:
            self.light.setPixmap(self.stoppic)
            self.label.setText(self.stoptext)
        elif mode == 2:
            self.light.setPixmap(self.errorpic)
            self.label.setText(self.errortext)


class SetStackPage(QWidget):
    def __init__(self, name: str):
        super().__init__()
        self.setPalette(palette)
        self.lbname = Label(self, (0, 10, 220, 25), name)
        Line(self, (0, 45, 630, 1))


class ModuleStackPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setPalette(palette)
        self.srlist = ScrollArea(self, (0, 55, 210, 480))
        self.srlist.setFrameShape(QFrame.Shape(0))
        self.sksetting = Stack(self, (225, 0, 400, 515))

    def LoadWidget(self):
        pass

    def SetWidget(self, config: dict):
        pass

    def CollectConfig(self) -> dict:
        pass


class Support(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("砂糖代理")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(spr.SGATitlePic))
        self.resize(643, 419)
        Picture(self, (0, 0, 643, 419), spr.SGASupportPic)


class TaskPanel(QWidget):
    def __init__(self, widget: QWidget, ordinate):
        super().__init__(widget)
        self.setGeometry(0, ordinate, 360, 110)
        self.setPalette(palette)
        self.lbsettitle = Label(self, (0, 0, 120, 27), "主任务模式设置：")
        self.tips = TipsButton(self, (130, 5), "作为主任务执行时生效，作为子任务时不生效")
        self.ckmute = Check(self, (0, 40, 220, 27), "静音运行")
        self.ckkillprog = Check(self, (205, 40, 220, 27), "完成后关闭任务窗口")
        self.lbafter = Label(self, (0, 80, 80, 27), "完成后：")
        self.cbafter = Combobox(self, (60, 80, 100, 30))
        self.cbafter.addItems(["无操作", "熄屏", "电脑睡眠"])
        self.ckkillsga = Check(self, (205, 80, 220, 27), "完成后关闭SGA")
