from PyQt5.QtWidgets import QWidget, QTextBrowser
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QPalette, QColor
from qfluentwidgets import ToggleToolButton
from ui.element.control import Picture, Check, Combobox, Label, Widget, Button


class MWindow(QWidget):
    # 主窗口初始化
    def __init__(self):
        super().__init__()
        self.setObjectName("main_window")
        self.resize(910, 580)
        self.setWindowTitle("砂糖代理")
        self.setWindowFlags(Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setFixedSize(self.width(), self.height())
        from assets.main_window.ui import SGA_icon
        self.setWindowIcon(QIcon(":/SGA.ico"))
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor(255, 255, 255))
        self.setPalette(palette)


class OverallButton(ToggleToolButton):
    def __init__(self, widget):
        super().__init__(widget)
        self.setIcon(r"assets\main_window\ui\set.png")
        self.setGeometry(QRect(635, 0, 56, 56))
        self.setIconSize(QSize(25, 25))


class InfoBox(QTextBrowser):
    def __init__(self, widget):
        super().__init__(widget)
        self.setGeometry(QRect(635, 60, 270, 515))
        self.setStyleSheet("QTextBrowser { font-size: 14px; }")
        self.moveCursor(self.textCursor().Start)  # <font color='red'>
        notify = "使用须知：\n" \
                 "    1、该项目（以下称SGA）免费、开源。如果您付费购买了该工具，请申请退款并举报售卖方，每一次倒卖都会使开源更加困难。\n" \
                 "    2、SGA包含第三方工具模块，所有第三方工具都不保证没有封号风险，怕别用，封认罚。\n" \
                 "    3、SGA更新随缘。警告维权，问题反馈，SGA更新，合作建议，请关注B站账号：绘星痕。\n" \
                 "    4、模块运行期间，可点击界面上“停止”按钮或键盘组合键“ctrl+/”快捷中止运行。\n" \
                 "    5、关于SGA使用方法和项目详情，可查看SGA文件夹中的说明文件的详细说明，" \
                 "和SGA各子界面的帮助按钮的精简提示，或参考B站账号：绘星痕 的SGA介绍和演示视频。\n"
        self.append(notify)


class Support(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("砂糖代理")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(":/SGA.ico"))
        self.resize(643, 419)
        Picture(self, (0, 0, 643, 419), r"assets\main_window\ui\hxh.png")


class AliveTip(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("砂糖代理")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon(":/SGA.ico"))
        self.resize(240, 80)
        Label(self, (40, 0, 160, 80), "SGA已启动，不能同时\n使用一个以上的SGA。")


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
        