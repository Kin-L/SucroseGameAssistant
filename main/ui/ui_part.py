from PyQt5.QtWidgets import QWidget, QTextBrowser
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QPalette, QColor
from .control import Picture, Check, Combobox, Label, Widget
from qfluentwidgets import ToggleToolButton


class MainWidget(QWidget):
    # 主窗口初始化
    def __init__(self):
        super().__init__()
        self.setObjectName("main_window")
        self.resize(910, 580)
        self.setWindowTitle("砂糖代理")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        import main.ui.SGA_icon
        self.setWindowIcon(QIcon(":/SGA.ico"))
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(palette)


class TaskWidgt:
    def __init__(self, _module, _pic_path):
        self.button = Picture(_module.widget, (0, 0, 50, 50), _pic_path)
        self.button.hide()
        self.widget = Widget()
        _module.stack_module.addWidget(self.widget)
        self.list = None
        self.set = None


class OverallButton(ToggleToolButton):
    def __init__(self, widget):
        super().__init__(widget)
        self.setIcon(r"assets\main_window\button\set.png")
        self.setGeometry(QRect(635, 0, 56, 56))
        self.setIconSize(QSize(25, 25))


class InfoBox(QTextBrowser):
    def __init__(self, widget):
        super().__init__(widget)
        self.setGeometry(QRect(635, 60, 270, 515))
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


class Support(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("砂糖代理")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(":/SGA.ico"))
        self.resize(643, 419)
        Picture(self, (0, 0, 643, 419), r"assets\main_window\back\hxh.png")


class Independent:
    def __init__(self, widget=None, location=None, kill_game=True):
        self.widget = Widget(widget, location)
        self.check_mute = Check(self.widget, (0, 0, 220, 27), "静音运行")
        if kill_game:
            self.check_kill_game = Check(self.widget, (205, 0, 220, 27), "完成后关闭游戏")
        self.label_after = Label(self.widget, (0, 40, 80, 27), "完成后：")
        self.combo_after = Combobox(self.widget, (60, 40, 100, 30))
        self.combo_after.addItems(["无操作", "熄屏", "电脑睡眠"])
        self.check_kill_sga = Check(self.widget, (205, 40, 220, 27), "完成后关闭SGA")
        