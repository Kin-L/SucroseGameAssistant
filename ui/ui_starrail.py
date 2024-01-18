# -*- coding:gbk -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from qfluentwidgets import CheckBox, ComboBox, CompactSpinBox, EditableComboBox, ImageLabel, LineEdit, PushButton, \
    SegmentedWidget, SmoothScrollArea, StrongBodyLabel, SubtitleLabel, TimePicker, TransparentPushButton


class Ui_starrail():
    def __init__(self):
        self.module()

    def module(self):
        self.page_starrail = QtWidgets.QWidget()
        self.page_starrail.setObjectName("page_starrail")
        self.scroll_starrail = SmoothScrollArea(self.page_starrail)
        self.scroll_starrail.setGeometry(QtCore.QRect(10, 50, 221, 391))
        self.scroll_starrail.setWidgetResizable(True)
        self.scroll_starrail.setObjectName("scroll_starrail")
        self.scrollWidget_starrail = QtWidgets.QWidget()
        self.scrollWidget_starrail.setGeometry(QtCore.QRect(0, 0, 219, 389))
        self.scrollWidget_starrail.setObjectName("scrollWidget_starrail")
        self.CheckBox_4 = CheckBox(self.scrollWidget_starrail)
        self.CheckBox_4.setGeometry(QtCore.QRect(10, 20, 92, 22))
        self.CheckBox_4.setObjectName("CheckBox_4")
        self.TransparentPushButton_4 = TransparentPushButton(self.scrollWidget_starrail)
        self.TransparentPushButton_4.setGeometry(QtCore.QRect(150, 20, 41, 30))
        self.TransparentPushButton_4.setObjectName("TransparentPushButton_4")
        self.scroll_starrail.setWidget(self.scrollWidget_starrail)
        self.label_starrail = SubtitleLabel(self.page_starrail)
        self.label_starrail.setGeometry(QtCore.QRect(50, 20, 119, 27))
        self.label_starrail.setObjectName("label_starrail")
        self.stacked_module.addWidget(self.page_starrail)

    def set_1(self):
        pass

    def set_2(self):
        pass