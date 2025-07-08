from maincode.tools.controls import (Button, TransPicButton,
                                     Label, Line, Check, tips,
                                     SLineEdit, PicButton, Combobox)
from ..timer.widget import TimerWidgets
from PyQt5.QtWidgets import QWidget
from maincode.main.maingroup import sg


class OverallWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.lbtitle = Label(self, (0, 0, 80, 40), "全局设置", 18)
        self.timer = TimerWidgets(self, (0, 60, 620, 300))
        self.lbocr = Label(self, (0, 250, 110, 40), f"指定OCR路径：")
        self.leocrpath = SLineEdit(self, (110, 255, 470, 33))
        tips(self.leocrpath, "请选择\"OCR-json.exe\"文件")

        foldpath = r"resources/main/button/fold.png"
        self.fileselect = PicButton(self, (587, 255, 33, 33), foldpath, (25, 25))
        self.lbkeyboard = Label(self, (0, 290, 110, 40), f"停止快捷键：")
        self.lekeyboard = SLineEdit(self, (110, 295, 120, 33))
        tips(self.lekeyboard, "更改快捷将在重启SGA后生效")
        sizetp = (30, 30)

        self.lbmodules = Label(self, (0, 335, 80, 40), "启用模组：")
        self.boxmodules = Combobox(self, (110, 340, 170, 35))
        self.boxmodules.setMaxVisibleItems(5)
        self.btmodulesdisable = TransPicButton(self, (290, 340, 35, 35), "resources/main/button/reduce.png", (25, 25))
        self.btmodulesrefresh = TransPicButton(self, (330, 340, 35, 35), "resources/main/button/refresh.png", (25, 25))

        self.line = Line(self, (0, 380, 620, 3))

        self.ckautoupdate = Check(self, (0, 390, 150, 40), "自动更新")
        self.btcheckupdate = Button(self, (95, 395, 80, 30), "检查更新")
        self.btstartupdate = Button(self, (90, 395, 80, 30), "开始更新")
        self.btstartupdate.hide()
        self.btstartupdate.setEnabled(False)
        self.lbversion = Label(self, (180, 390, 120, 40), f"版本号 {sg.info.Version}", 14)
        self.btupdatehistory = Button(self, (280, 395, 80, 30), "更新日志")
        self.btrunhistory = Button(self, (370, 395, 80, 30), "运行日志")
        supportpath = r"resources/main/button/support.png"
        githubpath = r"resources/main/button/github.png"
        giteepath = r"resources/main/button/gitee.png"
        bilibilipath = r"resources/main/button/bilibili.png"

        self.btsupport = TransPicButton(self, (460, 392, 30, 30), supportpath, (25, 25))
        self.btgithub = TransPicButton(self, (500, 392, 30, 30), githubpath, sizetp)
        self.btgitee = TransPicButton(self, (540, 392, 30, 30), giteepath, sizetp)
        self.btbilibili = TransPicButton(self, (580, 392, 30, 30), bilibilipath, sizetp)
