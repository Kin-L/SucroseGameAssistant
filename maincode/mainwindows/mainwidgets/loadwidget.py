from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QMovie, QPixmap
from maincode.tools.controls import palette
from maincode.tools.constant import spr


class LoadWidget(QWidget):
    def __init__(self, _widget: QMainWindow):
        super().__init__(_widget)
        self.setGeometry(0, 0, 910, 580)
        self.setPalette(palette)

        self.loadbacklab = QLabel("", self)
        self.loadbacklab.setPixmap(QPixmap(spr["LoadBackPic"]))
        self.loadbacklab.setGeometry(0, 0, 910, 580)
        self.loadbacklab.setScaledContents(True)

        self.loadgiflab = QLabel("", self)
        self.loadgifmov = QMovie(spr["LoadingGif"])
        self.loadgiflab.setMovie(self.loadgifmov)
        self.loadgiflab.setGeometry(430, 440, 50, 50)
        self.loadgiflab.setScaledContents(True)
        self.loadgifmov.start()
        self.raise_()
