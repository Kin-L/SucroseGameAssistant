from main.mainwindows import smw
from main.mainenvironment import sme


def check_update():
    smw.overall.button_check.setEnabled(False)
    smw.sendbox(mode=1)
    smw.sendbox("检查更新中...", mode=2)


def load_update():
    smw.overall.button_update.setEnabled(False)
    smw.sendbox(mode=1)
    smw.sendbox("开始更新中", mode=2)


def update_check_change():
    sme.update = smw.overall.auto_update.isChecked()


def open_update_history():
    from os import startfile
    startfile(sme.workdir + "/update.txt")
    smw.sendbox(mode=1)
    smw.sendbox("打开更新日志")
    smw.sendbox(mode=3)
