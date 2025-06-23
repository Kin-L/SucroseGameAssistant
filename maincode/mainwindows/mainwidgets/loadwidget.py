from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel
from PyQt5.QtGui import QMovie, QPixmap
from maincode.tools.controls import palette


class LoadWidget(QWidget):
    def __init__(self, _widget: QMainWindow):
        super().__init__(_widget)
        self.setGeometry(0, 0, 910, 580)
        self.setPalette(palette)

        backpath = r'resources/main/SGA/loadback.png'
        self.loadbacklab = QLabel("", self)
        self.loadbacklab.setPixmap(QPixmap(backpath))
        self.loadbacklab.setGeometry(0, 0, 910, 580)
        self.loadbacklab.setScaledContents(True)

        loadgifpath = r'resources/main/SGA/loading.gif'
        self.loadgiflab = QLabel("", self)
        self.loadgifmov = QMovie(loadgifpath)
        self.loadgiflab.setMovie(self.loadgifmov)
        self.loadgiflab.setGeometry(430, 440, 50, 50)
        self.loadgiflab.setScaledContents(True)
        self.loadgifmov.start()
        self.raise_()
