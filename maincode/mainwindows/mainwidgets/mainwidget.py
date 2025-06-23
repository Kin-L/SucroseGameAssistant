from maincode.tools.controls import (Line, Stack, Widget,
                                     PicButton, InfoBox, OverallButton,
                                     tips, Support)


class MainWidget(Widget):
    def __init__(self):
        super().__init__()
        self.sksetting = Stack(self, (5, 0, 625, 575))
        Line(self, (5, 38, 625, 3))
        # 全局/模块 设置按钮
        self.btsetting = OverallButton(self)
        self.obstate = False
        self.support = Support()
        # 历史信息按钮
        historypath = r"resources/main/button/history.png"
        savepath = r"resources/main/button/save.png"
        sizetp = (25, 25)
        self.bthistory = PicButton(self, (555, 0, 35, 35), historypath, sizetp)
        self.btconfigsave = PicButton(self, (515, 0, 35, 35), savepath, sizetp)
        tips(self.btconfigsave, "手动保存当前页面和全局设置,并应用定时(快捷键：ctrl+s)")
        # 指示信息窗口
        self.infobox = InfoBox(self)
        self.obstate = False

    def changeob(self):
        if self.obstate:
            self.sksetting.setCurrentIndex(1)
            self.obstate = False
        else:
            self.sksetting.setCurrentIndex(0)
            self.obstate = True
