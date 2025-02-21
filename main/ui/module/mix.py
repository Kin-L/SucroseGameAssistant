from main.ui.control import (Widget, Combobox, ScrollArea,
                             QtWidgets, Label, Line)
from main.ui.ui_part import Independent
from main.mainwindows import main_windows as mw


class MixList:
    def __init__(self, _widget):
        # 功能列表窗口
        self.scroll = ScrollArea(_widget, (0, 0, 215, 515))
        self.scroll.setFrameShape(QtWidgets.QFrame.Shape(0))
        # 运行列表窗口
        self.combobox_mix_config0 = Combobox(self.scroll, (0, 50, 210, 30))
        self.combobox_mix_config1 = Combobox(self.scroll, (0, 90, 210, 30))
        self.combobox_mix_config2 = Combobox(self.scroll, (0, 130, 210, 30))
        self.combobox_mix_config3 = Combobox(self.scroll, (0, 170, 210, 30))
        self.combobox_mix_config4 = Combobox(self.scroll, (0, 210, 210, 30))

        
class MixStack:
    def __init__(self, _widget):
        self.widget = Widget(_widget, (225, 0, 395, 515))
        # 功能堆叠窗口
        self.label_local = Label(self.widget, (0, 12, 220, 18), "设置页面：连续任务 运行方式")
        self.line0 = Line(self.widget, (0, 41, 395, 3))
        self.independent = Independent(self.widget, (0, 50, 350, 70), False)


_mix_dir = {
        "模块": 0,
        "配置0": {
            "name": "<未选择>"
        },
        "配置1": {
            "name": "<未选择>"
        },
        "配置2": {
            "name": "<未选择>"
        },
        "配置3": {
            "name": "<未选择>"
        },
        "配置4": {
            "name": "<未选择>"
        },
        "静音": False,
        "关闭软件": True,
        "完成后": 0,
        "SGA关闭": False
    }


def mix_input_config(_dir=None):
    if not _dir:
        _dir = _mix_dir
    _mix = mw.module.mix
    _mix.list.combobox_mix_config0.setCurrentText(_dir["配置0"]["name"])
    _mix.list.combobox_mix_config1.setCurrentText(_dir["配置1"]["name"])
    _mix.list.combobox_mix_config2.setCurrentText(_dir["配置2"]["name"])
    _mix.list.combobox_mix_config3.setCurrentText(_dir["配置3"]["name"])
    _mix.list.combobox_mix_config4.setCurrentText(_dir["配置4"]["name"])

    _mix.set.independent.check_mute.setChecked(_dir["静音"])
    _mix.set.independent.combo_after.setCurrentIndex(_dir["完成后"])
    _mix.set.independent.check_kill_sga.setChecked(_dir["SGA关闭"])


def mix_collect_config():
    _mix = mw.module.mix
    config = dict()
    config["模块"] = 0
    config["配置0"] = dict()
    config["配置1"] = dict()
    config["配置2"] = dict()
    config["配置3"] = dict()
    config["配置4"] = dict()
    config["配置0"]["name"] = _mix.list.combobox_mix_config0.currentText()
    config["配置1"]["name"] = _mix.list.combobox_mix_config1.currentText()
    config["配置2"]["name"] = _mix.list.combobox_mix_config2.currentText()
    config["配置3"]["name"] = _mix.list.combobox_mix_config3.currentText()
    config["配置4"]["name"] = _mix.list.combobox_mix_config4.currentText()
    config["静音"] = _mix.set.independent.check_mute.isChecked()
    config["关闭软件"] = True
    config["完成后"] = _mix.set.independent.combo_after.currentIndex()
    config["SGA关闭"] = _mix.set.independent.check_kill_sga.isChecked()
    return config


def mix_box_refresh(filelist):
    _filelist = ["<未选择>"] + filelist
    _mix = mw.module.mix.list
    _mix.combobox_mix_config0.clear()
    _mix.combobox_mix_config1.clear()
    _mix.combobox_mix_config2.clear()
    _mix.combobox_mix_config3.clear()
    _mix.combobox_mix_config4.clear()
    _mix.combobox_mix_config0.addItems(_filelist)
    _mix.combobox_mix_config1.addItems(_filelist)
    _mix.combobox_mix_config2.addItems(_filelist)
    _mix.combobox_mix_config3.addItems(_filelist)
    _mix.combobox_mix_config4.addItems(_filelist)
