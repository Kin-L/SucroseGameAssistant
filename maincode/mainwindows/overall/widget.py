from ...tools.sgaqt.texts import Label, SLineEdit, Line, tips
from ...tools.sgaqt.buttons import Button, PicButton, TransPicButton, Check, Combobox
from ..timer.main import SGATimer
from PyQt5.QtWidgets import QWidget
from maincode.config.configctrl import scc
from maincode.tools.core.constant import spr
from maincode.mainwindows.mainwindow import SGAQMainWindow


class OverallWidget(QWidget):
    def __init__(self, SQMW: SGAQMainWindow):
        super().__init__()
        self.lbtitle = Label(self, (0, 0, 80, 40), "全局设置", 18)
        self.timer = SGATimer(self, (0, 60, 620, 300), SQMW)
        self.lbocr = Label(self, (0, 250, 110, 40), f"指定OCR路径：")
        self.leocrpath = SLineEdit(self, (110, 255, 470, 33))
        tips(self.leocrpath, "请选择\"OCR-json.exe\"文件")

        self.fileselect = PicButton(self, (587, 255, 33, 33), spr["FoldPic"], (25, 25))
        self.lbkeyboard = Label(self, (0, 290, 110, 40), f"停止快捷键：")
        self.lekeyboard = SLineEdit(self, (110, 295, 120, 33))
        sizetp = (30, 30)

        self.lbmodules = Label(self, (0, 335, 80, 40), "启用模组：")
        self.boxmodules = Combobox(self, (110, 340, 170, 35))
        self.boxmodules.setMaxVisibleItems(5)
        self.btmodulesdisable = TransPicButton(self, (290, 340, 35, 35), spr["ReducePic"], (25, 25))
        tips(self.btmodulesdisable, "禁用后，重启SGA生效")
        self.btmodulesrefresh = TransPicButton(self, (330, 340, 35, 35), spr["RefreshPic"], (25, 25))

        self.line = Line(self, (0, 380, 620, 3))

        self.ckautoupdate = Check(self, (0, 390, 150, 40), "自动更新")
        self.btcheckupdate = Button(self, (95, 395, 80, 30), "检查更新")
        self.btstartupdate = Button(self, (90, 395, 80, 30), "开始更新")
        self.btstartupdate.hide()
        self.btstartupdate.setEnabled(False)
        self.lbversion = Label(self, (180, 390, 120, 40), f"版本号 {scc.info.Version}", 14)
        self.btupdatehistory = Button(self, (280, 395, 80, 30), "更新日志")
        self.btrunhistory = Button(self, (370, 395, 80, 30), "运行日志")

        self.btsupport = TransPicButton(self, (460, 392, 30, 30), spr["SupportPic"], (25, 25))
        self.btgithub = TransPicButton(self, (500, 392, 30, 30), spr["GithubPic"], sizetp)
        self.btgitee = TransPicButton(self, (540, 392, 30, 30), spr["GiteePic"], sizetp)
        self.btbilibili = TransPicButton(self, (580, 392, 30, 30), spr["BilibiliPic"], sizetp)
        self.btweb = TransPicButton(self, (0, 545, 30, 30), spr["HelpPic"], sizetp)
        tips(self.btweb, "使用引导/反馈")
        self.btrestart = TransPicButton(self, (40, 545, 30, 30), spr["RestartPic"], sizetp)
        tips(self.btrestart, "重启SGA")
