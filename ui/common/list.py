from ui.element.control import *


class CommonList:
    def __init__(self, widget, location):
        # 功能列表窗口
        scroll = ScrollArea(widget, location)
        scroll.setFrameShape(QtWidgets.QFrame.Shape(0))
        # 设置控件
        self.label_klein = Label(scroll, (75, 10, 80, 20), "通用执行", 18)
        setpath = "assets/main_window/ui/set.png"
        self.set_common = PicButton(scroll, (180, 10, 22, 22), setpath, (22, 22))

        self.check_start = Label(scroll, (15, 50, 140, 22), "启动设置")
        self.check_exit = Label(scroll, (15, 95, 140, 22), "结束设置")

        self.set_start = PicButton(scroll, (180, 50, 22, 22), setpath, (22, 22))
        self.set_exit = PicButton(scroll, (180, 95, 22, 22), setpath, (22, 22))
