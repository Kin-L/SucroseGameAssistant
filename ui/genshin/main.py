# -*- coding:gbk -*-
from .list import GenshinList
from .stack import GenshinStack
from ui.element.control import Line, Widget, PicButton


class Genshin:
    def __init__(self, stack, icon, main):
        self.widget_genshin = Widget()
        stack.addWidget(self.widget_genshin)
        self.button_genshin = (
            PicButton(icon, (110, 0, 50, 50),
                      r"assets\genshin\picture\genshin-icon.png", (50, 50)))
        self.list = None
        self.set = None

    def load_window(self):
        self.list = GenshinList(self.widget_genshin, (0, 0, 215, 515))
        self.set = GenshinStack(self.widget_genshin, (225, 0, 410, 515))
        self.list.set_genshin.clicked.connect(lambda: self.set.stack.setCurrentIndex(0))
        self.list.set_team.clicked.connect(lambda: self.set.stack.setCurrentIndex(1))
        self.list.set_disp.clicked.connect(lambda: self.set.stack.setCurrentIndex(2))
        self.list.set_trans.clicked.connect(lambda: self.set.stack.setCurrentIndex(3))
        self.list.set_fly.clicked.connect(lambda: self.set.stack.setCurrentIndex(4))
        self.list.set_comp.clicked.connect(lambda: self.set.stack.setCurrentIndex(5))
        self.list.set_pot.clicked.connect(lambda: self.set.stack.setCurrentIndex(6))
        self.list.set_mail.clicked.connect(lambda: self.set.stack.setCurrentIndex(7))
        self.list.set_tree.clicked.connect(lambda: self.set.stack.setCurrentIndex(8))
        self.list.set_domain.clicked.connect(lambda: self.set.stack.setCurrentIndex(9))
        Line(self.widget_genshin, (215, 5, 3, 505), False)

    def load_run(self, run):
        _dir = {
            "server": 0,
            "game": "",
            "BGI": ""
        }
        _dir.update(run)
        self.set.combo_server.setCurrentIndex(_dir["server"])
        self.set.line_start.setText(_dir["game"])
        self.set.line_start.setSelection(0, 0)
        self.set.line_bgi.setText(_dir["BGI"])

    def get_run(self):
        _dir = {
            "server": self.set.combo_server.currentIndex(),
            "game": self.set.line_start.text(),
            "BGI": self.set.line_bgi.text()
        }
        return _dir

    def input_config(self, _dir):
        config = {
            "模块": 2,
            "静音": False,
            "关闭软件": False,
            "完成后": 0,
            "SGA关闭": False,
            "功能0": False,
            "功能1": False,
            "功能2": False,
            "功能3": False,
            "功能4": False,
            "功能5": False,
            "功能6": False,
            "功能7": False,
            "功能8": False,
            "派遣0": [0, 0],
            "派遣1": [0, 0],
            "派遣2": [0, 0],
            "派遣3": [0, 0],
            "派遣4": [0, 0],
            "再次派遣": False,
            "参量质变仪0": "",
            "参量质变仪1": "",
            "参量质变仪2": "",
            "参量质变仪3": "",
            "参量质变仪4": "",
            "晶蝶0": False,
            "晶蝶1": False,
            "晶蝶2": False,
            "晶蝶3": False,
            "晶蝶4": False,
            "砍树次数": 0,
            "砍树0": False,
            "砍树1": False,
            "砍树2": False,
            "砍树3": False,
            "砍树4": False,
            "砍树5": False,
            "砍树6": False,
            "砍树7": False,
            "砍树8": False,
            "砍树9": False,
            "砍树10": False,
            "砍树11": False,
            "砍树12": False,
            "砍树13": False,
            "砍树14": False,
            "砍树15": False,
            "砍树16": False,
            "砍树17": False,
            "砍树18": False,
            "秘境": ["圣遗物", "仲夏庭院"]
        }
        config.update(_dir)
        self.set.independent.check_mute.setChecked(config["静音"])
        self.set.independent.check_kill_game.setChecked(config["关闭软件"])
        self.set.independent.combo_after.setCurrentIndex(config["完成后"])
        self.set.independent.check_kill_sga.setChecked(config["SGA关闭"])
        self.list.check_team.setChecked(config["功能0"])
        self.list.check_disp.setChecked(config["功能1"])
        self.list.check_trans.setChecked(config["功能2"])
        self.list.check_fly.setChecked(config["功能3"])
        self.list.check_comp.setChecked(config["功能4"])
        self.list.check_pot.setChecked(config["功能5"])
        self.list.check_mail.setChecked(config["功能6"])
        self.list.check_tree.setChecked(config["功能7"])
        self.list.check_domain.setChecked(config["功能8"])

        self.set.area0.setCurrentIndex(config["派遣0"][0])
        self.set.area1.setCurrentIndex(config["派遣1"][0])
        self.set.area2.setCurrentIndex(config["派遣2"][0])
        self.set.area3.setCurrentIndex(config["派遣3"][0])
        self.set.area4.setCurrentIndex(config["派遣4"][0])
        self.set.list_change(self.set.area0, self.set.mat0)
        self.set.list_change(self.set.area1, self.set.mat1)
        self.set.list_change(self.set.area2, self.set.mat2)
        self.set.list_change(self.set.area3, self.set.mat3)
        self.set.list_change(self.set.area4, self.set.mat4)
        self.set.mat0.setCurrentIndex(config["派遣0"][1])
        self.set.mat1.setCurrentIndex(config["派遣1"][1])
        self.set.mat2.setCurrentIndex(config["派遣2"][1])
        self.set.mat3.setCurrentIndex(config["派遣3"][1])
        self.set.mat4.setCurrentIndex(config["派遣4"][1])

        self.set.LineEdit0.setText(config["参量质变仪0"])
        self.set.LineEdit1.setText(config["参量质变仪1"])
        self.set.LineEdit2.setText(config["参量质变仪2"])
        self.set.LineEdit3.setText(config["参量质变仪3"])
        self.set.LineEdit4.setText(config["参量质变仪4"])
        self.set.fly0.setChecked(config["晶蝶0"])
        self.set.fly1.setChecked(config["晶蝶1"])
        self.set.fly2.setChecked(config["晶蝶2"])
        self.set.fly3.setChecked(config["晶蝶3"])
        self.set.fly4.setChecked(config["晶蝶4"])

        self.set.CompactSpinBox.setValue(config["砍树次数"])
        self.set.tree0.setChecked(config["砍树0"])
        self.set.tree1.setChecked(config["砍树1"])
        self.set.tree2.setChecked(config["砍树2"])
        self.set.tree3.setChecked(config["砍树3"])
        self.set.tree4.setChecked(config["砍树4"])
        self.set.tree5.setChecked(config["砍树5"])
        self.set.tree6.setChecked(config["砍树6"])
        self.set.tree7.setChecked(config["砍树7"])
        self.set.tree8.setChecked(config["砍树8"])
        self.set.tree9.setChecked(config["砍树9"])
        self.set.tree10.setChecked(config["砍树10"])
        self.set.tree11.setChecked(config["砍树11"])
        self.set.tree12.setChecked(config["砍树12"])
        self.set.tree13.setChecked(config["砍树13"])
        self.set.tree14.setChecked(config["砍树14"])
        self.set.tree15.setChecked(config["砍树15"])
        self.set.tree16.setChecked(config["砍树16"])
        self.set.tree17.setChecked(config["砍树17"])
        self.set.tree18.setChecked(config["砍树18"])
        self.set.domain_type.setCurrentText(config["秘境"][0])
        self.set.domain_change(self.set.domain_type, self.set.domain)
        self.set.domain.setCurrentText(config["秘境"][1])

    def output_config(self):
        config = dict()
        config["模块"] = 2

        config["静音"] = self.set.independent.check_mute.isChecked()
        config["关闭软件"] = self.set.independent.check_kill_game.isChecked()
        config["完成后"] = self.set.independent.combo_after.currentIndex()
        config["SGA关闭"] = self.set.independent.check_kill_sga.isChecked()

        config["功能0"] = self.list.check_team.isChecked()
        config["功能1"] = self.list.check_disp.isChecked()
        config["功能2"] = self.list.check_trans.isChecked()
        config["功能3"] = self.list.check_fly.isChecked()
        config["功能4"] = self.list.check_comp.isChecked()
        config["功能5"] = self.list.check_pot.isChecked()
        config["功能6"] = self.list.check_mail.isChecked()
        config["功能7"] = self.list.check_tree.isChecked()
        config["功能8"] = self.list.check_domain.isChecked()

        config["派遣0"] = [self.set.area0.currentIndex(), self.set.mat0.currentIndex()]
        config["派遣1"] = [self.set.area1.currentIndex(), self.set.mat1.currentIndex()]
        config["派遣2"] = [self.set.area2.currentIndex(), self.set.mat2.currentIndex()]
        config["派遣3"] = [self.set.area3.currentIndex(), self.set.mat3.currentIndex()]
        config["派遣4"] = [self.set.area4.currentIndex(), self.set.mat4.currentIndex()]
        config["再次派遣"] = self.set.redisp.isChecked()

        config["参量质变仪0"] = self.set.LineEdit0.text()
        config["参量质变仪1"] = self.set.LineEdit1.text()
        config["参量质变仪2"] = self.set.LineEdit2.text()
        config["参量质变仪3"] = self.set.LineEdit3.text()
        config["参量质变仪4"] = self.set.LineEdit4.text()

        config["晶蝶0"] = self.set.fly0.isChecked()
        config["晶蝶1"] = self.set.fly1.isChecked()
        config["晶蝶2"] = self.set.fly2.isChecked()
        config["晶蝶3"] = self.set.fly3.isChecked()
        config["晶蝶4"] = self.set.fly4.isChecked()

        config["砍树次数"] = self.set.CompactSpinBox.value()
        config["砍树0"] = self.set.tree0.isChecked()
        config["砍树1"] = self.set.tree1.isChecked()
        config["砍树2"] = self.set.tree2.isChecked()
        config["砍树3"] = self.set.tree3.isChecked()
        config["砍树4"] = self.set.tree4.isChecked()
        config["砍树5"] = self.set.tree5.isChecked()
        config["砍树6"] = self.set.tree6.isChecked()
        config["砍树7"] = self.set.tree7.isChecked()
        config["砍树8"] = self.set.tree8.isChecked()
        config["砍树9"] = self.set.tree9.isChecked()
        config["砍树10"] = self.set.tree10.isChecked()
        config["砍树11"] = self.set.tree11.isChecked()
        config["砍树12"] = self.set.tree12.isChecked()
        config["砍树13"] = self.set.tree13.isChecked()
        config["砍树14"] = self.set.tree14.isChecked()
        config["砍树15"] = self.set.tree15.isChecked()
        config["砍树16"] = self.set.tree16.isChecked()
        config["砍树17"] = self.set.tree17.isChecked()
        config["砍树18"] = self.set.tree18.isChecked()
        config["秘境"] = [self.set.domain_type.currentText(),
                        self.set.domain.currentText()]
        return config
