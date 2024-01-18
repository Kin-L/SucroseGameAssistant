# -*- coding:gbk -*-
from ui.element.control import *
from .list import MixList
from .stack import MixStack


# 原神模组设置窗口
class Mix:
    def __init__(self, stack, icon, main):
        # 连续任务
        self.widget_mix = Widget()
        stack.addWidget(self.widget_mix)
        self.button_mix = PicButton(icon, (0, 0, 50, 50),
                                    r"assets\main_window\ui\mix-icon.png", (50, 50))
        self.list = None
        self.set = None

    def load_window(self):
        self.list = MixList(self.widget_mix, (0, 0, 215, 515))
        self.set = MixStack(self.widget_mix, (225, 0, 395, 515))
        Line(self.widget_mix, (215, 5, 3, 505), False)

    def load_single(self, single):
        # 运行列表配置加载
        self.list.combobox_mix_config0.addItems(["<未选择>"] + single)
        self.list.combobox_mix_config1.addItems(["<未选择>"] + single)
        self.list.combobox_mix_config2.addItems(["<未选择>"] + single)
        self.list.combobox_mix_config3.addItems(["<未选择>"] + single)
        self.list.combobox_mix_config4.addItems(["<未选择>"] + single)

    def add_item(self, name):
        self.list.combobox_mix_config0.addItem(name)
        self.list.combobox_mix_config1.addItem(name)
        self.list.combobox_mix_config2.addItem(name)
        self.list.combobox_mix_config3.addItem(name)
        self.list.combobox_mix_config4.addItem(name)

    def remove_item(self, name):
        self.list.combobox_mix_config0.removeItem(self.list.combobox_mix_config0.findText(name))
        self.list.combobox_mix_config1.removeItem(self.list.combobox_mix_config0.findText(name))
        self.list.combobox_mix_config2.removeItem(self.list.combobox_mix_config0.findText(name))
        self.list.combobox_mix_config3.removeItem(self.list.combobox_mix_config0.findText(name))
        self.list.combobox_mix_config4.removeItem(self.list.combobox_mix_config0.findText(name))

    def rename_item(self, old_name, new_name):
        self.list.combobox_mix_config0.rename(old_name, new_name)
        self.list.combobox_mix_config1.rename(old_name, new_name)
        self.list.combobox_mix_config2.rename(old_name, new_name)
        self.list.combobox_mix_config3.rename(old_name, new_name)
        self.list.combobox_mix_config4.rename(old_name, new_name)

    def input_config(self, _dir):
        config = {
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
            "SGA关闭": False,
        }
        config.update(_dir)
        self.list.combobox_mix_config0.setCurrentText(config["配置0"]["name"])
        self.list.combobox_mix_config1.setCurrentText(config["配置1"]["name"])
        self.list.combobox_mix_config2.setCurrentText(config["配置2"]["name"])
        self.list.combobox_mix_config3.setCurrentText(config["配置3"]["name"])
        self.list.combobox_mix_config4.setCurrentText(config["配置4"]["name"])

        self.set.independent.check_mute.setChecked(config["静音"])
        self.set.independent.combo_after.setCurrentIndex(config["完成后"])
        self.set.independent.check_kill_sga.setChecked(config["SGA关闭"])

    def output_config(self):
        config = dict()
        config["模块"] = 0
        config["配置0"] = dict()
        config["配置1"] = dict()
        config["配置2"] = dict()
        config["配置3"] = dict()
        config["配置4"] = dict()
        config["配置0"]["name"] = self.list.combobox_mix_config0.currentText()
        config["配置1"]["name"] = self.list.combobox_mix_config1.currentText()
        config["配置2"]["name"] = self.list.combobox_mix_config2.currentText()
        config["配置3"]["name"] = self.list.combobox_mix_config3.currentText()
        config["配置4"]["name"] = self.list.combobox_mix_config4.currentText()
        config["静音"] = self.set.independent.check_mute.isChecked()
        config["关闭软件"] = True
        config["完成后"] = self.set.independent.combo_after.currentIndex()
        config["SGA关闭"] = self.set.independent.check_kill_sga.isChecked()
        return config
