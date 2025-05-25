from qfluentwidgets import (SmoothScrollArea, StrongBodyLabel,
                            PushButton, ToolButton, TransparentToolButton,
                            CheckBox, ComboBox, LineEdit, SwitchButton,
                            setFont, TimePicker, ToolTipFilter,
                            ToolTipPosition, ToggleToolButton)
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QStackedWidget, QTextBrowser
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import QSize
from typing import Union, Tuple
palette = QPalette()
palette.setColor(QPalette.Background, QColor(255, 255, 255))

int4 = Tuple[int, int, int, int]


# 窗口
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


# 标签
class Label(StrongBodyLabel):
    def __init__(self, widget: QWidget, location: int4, text: str, font: int = 16):
        super().__init__(widget)
        self.setGeometry(*location)
        self.setText(text)
        setFont(self, font)


class Picture(QLabel):
    def __init__(self, widget: QWidget, location: int4, path: str):
        super().__init__(widget)
        self.setGeometry(*location)
        self.setPixmap(QPixmap(path))
        self.setScaledContents(True)


# 按钮
class Button(PushButton):
    def __init__(self, widget: QWidget, location: int4, text: str):
        super().__init__(widget)
        self.setText(text)
        self.setGeometry(*location)


class PicButton(ToolButton):
    def __init__(self, widget: QWidget, location: int4, path: str, size: (int, int)):
        super().__init__(widget)
        self.setIcon(path)
        self.setGeometry(*location)
        self.setIconSize(QSize(*size))
        

class TransPicButton(TransparentToolButton):
    def __init__(self, widget: QWidget, location: int4, path: str, size: (int, int)):
        super().__init__(widget)
        self.setIcon(path)
        self.setGeometry(*location)
        self.setIconSize(QSize(*size))


class Check(CheckBox):
    def __init__(self, widget: QWidget, location: int4, text: str):
        super().__init__(widget)
        self.setGeometry(*location)
        self.setText(text)


# 输入框
class Combobox(ComboBox):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        self.setGeometry(*location)

    def rename(self, old_name, new_name):
        old_index = self.findText(old_name)
        if old_index == -1:
            print("error:未找到该条目。")
        else:
            self.setItemText(old_index, new_name)


class SLineEdit(LineEdit):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        self.setGeometry(*location)


class Line(QFrame):
    def __init__(self, widget: QWidget, location: int4, hor=True):
        super().__init__(widget)
        self.setGeometry(*location)
        if hor:
            self.setFrameShape(QFrame.HLine)
        else:
            self.setFrameShape(QFrame.VLine)


class Swicher(SwitchButton):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        self.setGeometry(*location)


class Timepicker(TimePicker):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        self.setGeometry(*location)


def tips(control, text: str):
    control.setToolTip(text)
    control.installEventFilter(
        ToolTipFilter(control, showDelay=200,
                      position=ToolTipPosition.TOP))


class InfoBox(QTextBrowser):
    def __init__(self, widget: QWidget):
        super().__init__(widget)
        self.setGeometry(635, 0, 270, 575)
        self.setStyleSheet("QTextBrowser { font-size: 14px; }")
        self.moveCursor(self.textCursor().Start)  # <font color='red'>
        notify = "使用须知:\n" \
                 "1、该项目（以下称SGA）免费、开源。"\
                 "如果您付费购买了该工具，请申请退款并举报售卖方，每一次倒卖都会使开源更加困难。\n" \
                 "2、所有用于游戏的第三方工具都不保证没有封号风险。\n" \
                 "3、点击停止按钮或快捷键“ctrl+/”中止当前任务。\n" \
                 "4、SGA文件夹中有使用说明文件，" \
                 "鼠标悬停部分按钮上会有提示信息，或参考B站账号:绘星痕 的SGA介绍视频。\n" \
                 "------------------------------"
        self.append(notify)


class OverallButton(ToggleToolButton):
    def __init__(self, widget: QWidget):
        super().__init__(widget)
        self.setIcon(r'resources/main/button/set.png')
        self.setGeometry(595, 0, 35, 35)
        self.setIconSize(QSize(25, 25))


class StateSigh(QWidget):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        self.setGeometry(*location)
        self.setPalette(palette)
        self.rightpic = QPixmap("resources/main/state/right.png")
        self.stoppic = QPixmap("resources/main/state/right.png")
        self.errorpic = QPixmap("resources/main/state/right.png")
        self.righttext = "正常运行"
        self.stoptext = "手动终止"
        self.errortext = "运行异常"
        self.light = Picture(self, (0, 3, 25, 25), self.rightpic)
        self.label = Label(self, (30, 0, 65, 30), self.righttext)

    def SetState(self, mode: int):
        if mode == 0:
            self.light.setPixmap(self.rightpic)
            self.setText(self.righttext)
        elif mode == 1:
            self.light.setPixmap(self.stoppic)
            self.setText(self.stoptext)
        elif mode == 2:
            self.light.setPixmap(self.errorpic)
            self.setText(self.errortext)


class SetButton(ToolButton):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        setpath = 'resources/main/button/set.png'
        self.setIcon(setpath)
        self.setGeometry(*location)
        self.setIconSize(QSize(30, 30))


class SetStackPage(QWidget):
    def __init__(self, name: str):
        super().__init__()
        self.setPalette(palette)
        self.lbname = Label(self, (0, 10, 120, 25), name)
        Line(self, (0, 45, 630, 1))


class ModuleStackPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setPalette(palette)
        self.srlist = ScrollArea(self, (0, 55, 210, 480))
        self.srlist.setFrameShape(QFrame.Shape(0))
        self.sksetting = Stack(self, (225, 0, 400, 515))
