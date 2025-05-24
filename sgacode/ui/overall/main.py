from sgacode.ui.control import (Button, TransPicButton,
                                Label, Line, Check,
                                SLineEdit)
from sgacode.ui.overall.timer import TimerWindow
from PyQt5.QtWidgets import QWidget
from sgacode.tools.main import env


class OverallWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.lbtitle = Label(self, (0, 0, 80, 40), "全局设置", 18)
        self.timer = TimerWindow(self, (0, 60, 620, 300))
        self.line = Line(self, (0, 300, 620, 3))
        self.ckautoupdate = Check(self, (0, 310, 150, 40), "自动更新")
        self.btcheckupdate = Button(self, (135, 315, 80, 30), "检查更新")
        self.btstartupdate = Button(self, (135, 315, 80, 30), "开始更新")
        self.btstartupdate.hide()
        self.btstartupdate.setEnabled(False)
        self.lbversion = Label(self, (225, 310, 120, 40), f"版本号 {env.version}", 14)

        self.btupdatehistory = Button(self, (325, 315, 80, 30), "更新日志")

        githubpath = r"resources/main/button/github.png"
        giteepath = r"resources/main/button/gitee.png"
        bilibilipath = r"resources/main/button/bilibili.png"
        sizetp = (30, 30)
        self.btgithub = TransPicButton(self, (500, 312, 30, 30), githubpath, sizetp)
        self.btgitee = TransPicButton(self, (540, 312, 30, 30), giteepath, sizetp)
        self.btbilibili = TransPicButton(self, (580, 312, 30, 30), bilibilipath, sizetp)
        self.lbocr = Label(self, (0, 250, 110, 40), f"指定OCR路径：")
        self.leocrpath = SLineEdit(self, (110, 255, 510, 33))
