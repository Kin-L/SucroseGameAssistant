import sys

from qfluentwidgets import (SmoothScrollArea, StrongBodyLabel,
                            PushButton, ToolButton, TransparentToolButton,
                            CheckBox, ComboBox, LineEdit,
                            setFont)
from PyQt5 import QtCore, QtWidgets, QtGui


# 窗口
class Widget(QtWidgets.QWidget):
    def __init__(self, widget=None, location=None):
        super().__init__(widget)
        if location is not None:
            (x, y, w, h) = location
            self.setGeometry(QtCore.QRect(x, y, w, h))
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtGui.QColor(255, 255, 255))
        self.setPalette(palette)


class ScrollArea(SmoothScrollArea):
    def __init__(self, widget, location):
        super().__init__(widget)
        (x, y, w, h) = location
        self.setGeometry(QtCore.QRect(x, y, w, h))
        self.setWidgetResizable(True)


class Stack(QtWidgets.QStackedWidget):
    def __init__(self, widget, location):
        super().__init__(widget)
        (x, y, w, h) = location
        self.setGeometry(QtCore.QRect(x, y, w, h))


# 标签
class Label(StrongBodyLabel):
    def __init__(self, widget, location, text, font=16):
        super().__init__(widget)
        (x, y, w, h) = location
        self.setGeometry(QtCore.QRect(x, y, w, h))
        self.setText(text)
        setFont(self, font)


class Picture(QtWidgets.QLabel):
    def __init__(self, widget, location=None, path=None):
        super().__init__(widget)
        if location is not None:
            (x, y, w, h) = location
            self.setGeometry(QtCore.QRect(x, y, w, h))
        self.setPixmap(QtGui.QPixmap(path))
        self.setScaledContents(True)


# 按钮
class Button(PushButton):
    def __init__(self, widget, location, text):
        super().__init__(widget)
        (x, y, w, h) = location
        self.setText(text)
        self.setGeometry(QtCore.QRect(x, y, w, h))


class PicButton(ToolButton):
    def __init__(self, widget, location, path, size):
        super().__init__(widget)
        (x, y, w, h) = location
        (pw, ph) = size
        self.setIcon(path)
        self.setIconSize(QtCore.QSize(pw, ph))
        self.setGeometry(QtCore.QRect(x, y, w, h))


class TransPicButton(TransparentToolButton):
    def __init__(self, widget, location, path, size):
        super().__init__(widget)
        (x, y, w, h) = location
        (pw, ph) = size
        self.setIcon(path)
        self.setIconSize(QtCore.QSize(pw, ph))
        self.setGeometry(QtCore.QRect(x, y, w, h))


class Check(CheckBox):
    def __init__(self, widget, location, text):
        super().__init__(widget)
        (x, y, w, h) = location
        self.setGeometry(QtCore.QRect(x, y, w, h))
        self.setText(text)


# 输入框
class Combobox(ComboBox):
    def __init__(self, widget, location):
        (x, y, w, h) = location
        super().__init__(widget)
        self.setGeometry(QtCore.QRect(x, y, w, h))

    def rename(self, old_name, new_name):
        old_index = self.findText(old_name)
        if old_index == -1:
            print("error:未找到该条目。")
        else:
            self.setItemText(old_index, new_name)


class Lineedit(LineEdit):
    def __init__(self, widget, location):
        (x, y, w, h) = location
        super().__init__(widget)
        self.setGeometry(QtCore.QRect(x, y, w, h))


class Line(QtWidgets.QFrame):
    def __init__(self, widget, location, hor=True):
        (x, y, w, h) = location
        super().__init__(widget)
        self.setGeometry(QtCore.QRect(x, y, w, h))
        if hor:
            self.setFrameShape(QtWidgets.QFrame.HLine)
        else:
            self.setFrameShape(QtWidgets.QFrame.VLine)
