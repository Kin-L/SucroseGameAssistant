from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QFrame, QTextBrowser
from qfluentwidgets import StrongBodyLabel, setFont, LineEdit, ToolTipFilter, ToolTipPosition

from maincode.tools.sgaqt.widgets import int4


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
                 "1、该项目（以下称SGA）免费、开源。" \
                 "如果您付费购买了该工具，请申请退款并举报售卖方，每一次倒卖都会使开源更加困难。\n" \
                 "2、所有用于游戏的第三方工具都不保证没有封号风险。\n" \
                 "3、点击停止按钮或快捷键“ctrl+/”中止当前任务。\n" \
                 "4、SGA文件夹中有使用说明文件，" \
                 "鼠标悬停部分按钮上会有提示信息，或参考B站账号:绘星痕 的SGA介绍视频。\n" \
                 "------------------------------"
        self.append(notify)
