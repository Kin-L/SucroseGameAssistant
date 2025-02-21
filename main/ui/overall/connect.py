from main.mainwindows import main_windows as mw
from main.tools.environment import env


def check_update():
    mw.overall.button_check.setEnabled(False)
    mw.sendbox(mode=1)
    mw.sendbox("检查更新中...", mode=2)


def load_update():
    mw.overall.button_update.setEnabled(False)
    mw.sendbox(mode=1)
    mw.sendbox("开始更新中", mode=2)


def update_check_change():
    env.update = mw.overall.auto_update.isChecked()


def open_update_history():
    from os import startfile
    startfile(env.workdir + "/update.txt")
    mw.sendbox(mode=1)
    mw.sendbox("打开更新日志")
    mw.sendbox(mode=3)
