from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QWidget
from qfluentwidgets import PushButton, ToolButton, TransparentToolButton, CheckBox, ComboBox, SwitchButton, TimePicker, \
    ToggleToolButton
from typing import Tuple

int4 = Tuple[int, int, int, int]


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


class Combobox(ComboBox):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        self.setGeometry(*location)


class Swicher(SwitchButton):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        self.setGeometry(*location)


class Timepicker(TimePicker):
    def __init__(self, widget: QWidget, location: int4):
        super().__init__(widget)
        self.setGeometry(*location)
        self.getTime()


class OverallButton(ToggleToolButton):
    def __init__(self, widget: QWidget):
        super().__init__(widget)
        self.setIcon(r'resources/main/button/set.png')
        self.setGeometry(595, 0, 35, 35)
        self.setIconSize(QSize(25, 25))


class ConsoleButton(ToggleToolButton):
    def __init__(self, widget: QWidget):
        super().__init__(widget)
        self.setIcon(r'resources/main/button/command.png')
        self.setGeometry(475, 0, 35, 35)
        self.setIconSize(QSize(25, 25))


class SetButton(ToolButton):
    def __init__(self, widget: QWidget, location: int4, size=(30, 30)):
        super().__init__(widget)
        setpath = 'resources/main/button/set.png'
        self.setIcon(setpath)
        self.setGeometry(*location)
        self.setIconSize(QSize(*size))
