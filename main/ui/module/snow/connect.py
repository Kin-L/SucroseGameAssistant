from main.mainwindows import main_windows as mw
from main.tools.environment import env
from subprocess import run as cmd_run
from webbrowser import open as weopen
from os import makedirs, path
_sonw = mw.module.snow


def combo_server_change():
    env.launch["snow_server"] = _sonw.set.local.combo_server.currentIndex()


def line_start_change():
    _text = _sonw.set.local.line_start.text()
    _text.strip("\"")
    if not _text:
        env.launch["snow_path"] = ""
    elif not path.exists(_text):
        mw.sendbox(f"路径不存在：{_text}")
        mw.sendbox(mode=3)
    else:
        env.launch["snow_path"] = _text


def snow_connect():
    if not path.exists("personal\\snow\\roll"):
        makedirs("personal\\snow\\roll")
    _sonw.list.set_snow.clicked.connect(lambda: _sonw.set.stack.setCurrentIndex(0))
    _sonw.list.set_fight.clicked.connect(lambda: _sonw.set.stack.setCurrentIndex(1))
    _sonw.list.set_daily.clicked.connect(lambda: _sonw.set.stack.setCurrentIndex(2))
    _sonw.list.set_mail.clicked.connect(lambda: _sonw.set.stack.setCurrentIndex(3))
    _sonw.list.set_roll.clicked.connect(lambda: _sonw.set.stack.setCurrentIndex(4))

    _sonw.set.local.button_wiki.clicked.connect(lambda: weopen("https://www.gamekee.com/snow/"))
    _sonw.set.local.combo_server.toggled.connect(combo_server_change)
    _sonw.set.local.line_start.editingFinished.connect(line_start_change)
    _sonw.set.roll.button_open_roll.clicked.connect(lambda: cmd_run(env.workdir + "\\personal\\snow\\roll", shell=True))
    _sonw.set.fight.button_snow_list1.clicked.connect(
        lambda: cmd_run(env.workdir + "\\assets\\snow\\list.json", shell=True))
    _sonw.set.daily.button_snow_list2.clicked.connect(
        lambda: cmd_run(env.workdir + "\\assets\\snow\\list.json", shell=True))

    # _sonw.list.button_start.clicked.connect(_sonw.rapid_start_game)
    # _sonw.list.button_switch.checkedChanged.connect(_sonw.switcher)
