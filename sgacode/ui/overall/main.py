from sgacode.ui.control import (Button, TransPicButton,
                                Label, Line, Check,
                                SLineEdit, PicButton)
from sgacode.ui.overall.timer import TimerWindow
from PyQt5.QtWidgets import QWidget, QFileDialog
from sgacode.tools.sgagroup import sg


class OverallWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.lbtitle = Label(self, (0, 0, 80, 40), "全局设置", 18)
        self.timer = TimerWindow(self, (0, 60, 620, 300))
        self.lbocr = Label(self, (0, 250, 110, 40), f"指定OCR路径：")
        self.leocrpath = SLineEdit(self, (110, 255, 470, 33))
        foldpath = r"resources/main/button/fold.png"
        self.fileselect = PicButton(self, (587, 255, 33, 33), foldpath, (25, 25))
        self.lbkeyboard = Label(self, (0, 290, 110, 40), f"停止快捷键：")
        self.lekeyboard = SLineEdit(self, (110, 295, 120, 33))

        self.line = Line(self, (0, 340, 620, 3))

        self.ckautoupdate = Check(self, (0, 350, 150, 40), "自动更新")
        self.btcheckupdate = Button(self, (95, 355, 80, 30), "检查更新")
        self.btstartupdate = Button(self, (90, 355, 80, 30), "开始更新")
        self.btstartupdate.hide()
        self.btstartupdate.setEnabled(False)
        self.lbversion = Label(self, (180, 350, 120, 40), f"版本号 {sg.info.version}", 14)
        self.btupdatehistory = Button(self, (280, 355, 80, 30), "更新日志")
        self.btrunhistory = Button(self, (370, 355, 80, 30), "运行日志")
        supportpath = r"resources/main/button/support.png"
        githubpath = r"resources/main/button/github.png"
        giteepath = r"resources/main/button/gitee.png"
        bilibilipath = r"resources/main/button/bilibili.png"
        sizetp = (30, 30)
        self.btsupport = TransPicButton(self, (460, 352, 30, 30), supportpath, (25, 25))
        self.btgithub = TransPicButton(self, (500, 352, 30, 30), githubpath, sizetp)
        self.btgitee = TransPicButton(self, (540, 352, 30, 30), giteepath, sizetp)
        self.btbilibili = TransPicButton(self, (580, 352, 30, 30), bilibilipath, sizetp)

    def SelectOCRPath(self):
        path = QFileDialog.getOpenFileName(self, "选择OCR组件exe文件")
        self.leocrpath.setText(path[0])
        sg.mainconfig['OcrPath'] = path
