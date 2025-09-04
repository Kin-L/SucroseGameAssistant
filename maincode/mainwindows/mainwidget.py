from maincode.tools.sgaqt.texts import Line, tips, InfoBox
from maincode.tools.sgaqt.buttons import PicButton, OverallButton, ConsoleButton
from maincode.tools.sgaqt.widgets import Widget, Stack, Support
from ctypes import windll
from maincode.tools.core.constant import spr
from time import localtime, strftime
from maincode.tools.core.logger import logger
from maincode.config.configctrl import scc

# 常量定义
UI_WIDTH = 625
UI_HEIGHT = 575
BUTTON_SIZE_TP = (25, 25)
HISTORY_BUTTON_POS = (555, 0, 35, 35)
SAVE_BUTTON_POS = (515, 0, 35, 35)
SEPARATOR_LINE = "------------------------------"


class MainWidget(Widget):
    def __init__(self):
        super().__init__()
        self.sksetting = Stack(self, (5, 0, UI_WIDTH, UI_HEIGHT))
        Line(self, (5, 38, UI_WIDTH, 3))
        # 全局/模块 设置按钮
        self.btsetting = OverallButton(self)
        self.console_window = None
        try:
            self.console_window = windll.kernel32.GetConsoleWindow()
            windll.user32.ShowWindow(self.console_window, int(scc.mc.ShowConsole))

        except Exception as e:
            logger.error(f"Failed to get console window: {e}")
        self.obstate = False
        self.support = Support()
        # 历史信息按钮
        self.bthistory = PicButton(self, HISTORY_BUTTON_POS, spr["HistoryPic"], BUTTON_SIZE_TP)
        self.btconfigsave = PicButton(self, SAVE_BUTTON_POS, spr["SavePic"], BUTTON_SIZE_TP)
        tips(self.btconfigsave, "手动保存并应用当前页面设置(快捷键：ctrl+s)")
        # 指示信息窗口
        self.infobox = InfoBox(self)
        self.btconsole = ConsoleButton(self)
        self.btconsole.setChecked(scc.mc.ShowConsole)

    def changeob(self):
        if self.obstate:
            self.sksetting.setCurrentIndex(1)
            self.obstate = False
        else:
            self.sksetting.setCurrentIndex(0)
            self.obstate = True

    def changecs(self):
        if not self.console_window:
            return
        try:
            if scc.mc.ShowConsole:
                windll.user32.ShowWindow(self.console_window, 0)
                scc.mc.ShowConsole = False
            else:
                windll.user32.ShowWindow(self.console_window, 1)
                scc.mc.ShowConsole = True
        except Exception as e:
            logger.error(f"Failed to toggle console visibility: {e}")

    def infoAdd(self, msg: str = "", addtime=True):
        timestr = ""
        if addtime:
            timestr = strftime("%H:%M:%S ", localtime())
        msg = msg.strip("\n")  # 修复原逻辑错误
        if "\n" in msg:
            prefix = "\n  " if addtime else "\n"
            msg = prefix + msg.replace("\n", "\n  ")
        full_msg = timestr + msg
        self.infobox.append(full_msg)
        self.infobox.ensureCursorVisible()
        logger.info(msg)

    def infoHead(self):
        today = strftime("%Y-%m-%d", localtime())
        if today != logger.date:
            logger.new_handler(today)
        self.infobox.append(today)

    def infoEnd(self):
        self.infobox.append(SEPARATOR_LINE)
        self.infobox.ensureCursorVisible()
        logger.info(SEPARATOR_LINE)

    def infoClear(self):
        self.infobox.clear()
