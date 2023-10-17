# -*- coding:gbk -*-
import os.path

from PyQt5 import QtCore, QtGui, QtWidgets
import json
class Maa_ui_group(object):
    def maa_game_tool(self):
        self.maa_page = QtWidgets.QWidget()
        self.maa_page.setObjectName("maa_page")
        self.game_pages.addWidget(self.maa_page)
        with open("resource\maa\maa_index.json", 'r', encoding='utf-8') as d:
            self.maa_index = json.load(d)
        # 标签
        self.maa_choose_Label = QtWidgets.QLabel(self.maa_page)
        self.maa_choose_Label.setGeometry(self.ui_zoom(20, 0, 81, 25))
        self.maa_choose_Label.setObjectName("maa_choose_Label")
        self.maa_choose_Label.setText(self._translate("main_window", "选 项"))
        self.maa_set_Label = QtWidgets.QLabel(self.maa_page)
        self.maa_set_Label.setGeometry(self.ui_zoom(110, 0, 81, 25))
        self.maa_set_Label.setObjectName("maa_set_Label")
        self.maa_set_Label.setText(self._translate("main_window", "切换页面"))
        # 滚动页面
        self.maa_filler = QtWidgets.QWidget(self.maa_page)
        self.trans_list = self.maa_index["功能"]
        self.maa_filler.setMinimumSize(168, len(self.trans_list) * 30)  #######设置滚动条的尺寸
        self.maa_scroll = QtWidgets.QScrollArea(self.maa_page)
        self.maa_scroll.setWidget(self.maa_filler)
        x, y, w, h = self.num_zoom([2, 28, 168, 280])
        self.maa_scroll.move(x, y)
        self.maa_scroll.resize(w, h)
        self.maa_scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        for num in range(len(self.trans_list)):
            tname = self.trans_list[num]
            fnamep = self.maa_index[tname]
            strc, strs, strp = "self.maa_choose_%s" % (fnamep), "self.maa_set_%s" % (fnamep), "self.maa_%s_page" % (fnamep)
            exec(strc + "= QtWidgets.QCheckBox(self.maa_filler)")
            exec(strs + "= QtWidgets.QPushButton(self.maa_filler)")
            exec(strp + "= QtWidgets.QWidget()")
            fc, fs, fp = eval(strc), eval(strs), eval(strp)
            fc.setGeometry(self.ui_zoom(5, 5 + 30 * num, 110, 16))
            fc.setObjectName(strc)
            fc.setText(self._translate("main_window", tname))
            fs.setGeometry(self.ui_zoom(125, 3 + (30 * num), 20, 20))
            fs.setObjectName(strs)
            fs.setIcon(QtGui.QIcon(r"resource\main_window\ui\set.png"))
            fs.setFlat(True)
            fp.setObjectName(strp)
            self.set_pages.addWidget(fp)
        self.maa_choose_create.setEnabled(False)
        self.maa_choose_create.setChecked(True)
        self.maa_choose_kill_game.setEnabled(False)
        self.maa_choose_kill_game.setChecked(True)
        self.maa_set_create.clicked.connect(lambda: self.change_set_page(20))
        self.maa_set_kill_game.clicked.connect(lambda: self.change_set_page(21))

        self.maa_start_program()
        self.maa_kill_game_program()
        # 帮助按钮
        self.maa_help1.clicked.connect(lambda: self.send_maa_help("模块介绍"))
        self.maa_help2.clicked.connect(lambda: self.send_maa_help("结束操作"))

    def send_maa_help(self, helpstr):
        with open("resource\maa\maa_help.json", 'r', encoding='utf-8') as h:
            self.maa_help = json.load(h)
        help_list = self.maa_help[helpstr]
        self.output_string.moveCursor(self.output_string.textCursor().End)
        self.output_string.append("")
        for i in help_list:
            self.output_string.append(i)
            self.output_string.ensureCursorVisible()
    # 启动页面
    def maa_start_program(self):
        self.maa_game_path_Label = QtWidgets.QLabel(self.maa_create_page)
        self.maa_game_path_Label.setGeometry(self.ui_zoom(5, 5, 81, 25))
        self.maa_game_path_Label.setObjectName("maa_game_path_Label")
        self.maa_game_path_Label.setText(self._translate("main_window", "启动路径"))
        self.maa_game_path = QtWidgets.QLineEdit(self.maa_create_page)
        self.maa_game_path.setGeometry(self.ui_zoom(5, 40, 260, 20))
        self.maa_game_path.setObjectName("maa_game_path")
        self.maa_game_path.home(False)
        self.maa_set_Label = QtWidgets.QLabel(self.maa_create_page)
        self.maa_set_Label.setGeometry(self.ui_zoom(5, 65, 81, 25))
        self.maa_set_Label.setObjectName("maa_set_Label")
        self.maa_set_Label.setText(self._translate("main_window", "运行配置"))
        self.maa_set_box = QtWidgets.QComboBox(self.maa_create_page)
        self.maa_set_box.setGeometry(self.ui_zoom(5, 95, 140, 25))
        self.maa_set_box.setObjectName("maa_set_box")
        self.comboboxstyle(self.maa_set_box)
        self.maa_set_box.addItem("未识别")
        self.maa_set_refresh_button = QtWidgets.QPushButton(self.maa_create_page)
        self.maa_set_refresh_button.setGeometry(self.ui_zoom(60, 65, 25, 25))
        self.maa_set_refresh_button.setObjectName("maa_set_refresh")
        self.maa_set_refresh_button.setIcon(QtGui.QIcon(r"resource\main_window\ui\refresh.png"))
        self.maa_set_refresh_button.setFlat(True)
        self.maa_set_refresh_button.clicked.connect(self.maa_set_refresh)
        self.maa_help1 = QtWidgets.QPushButton(self.maa_create_page)
        self.maa_help1.setGeometry(self.ui_zoom(225, 5, 40, 25))
        self.maa_help1.setObjectName("maa_help1")
        self.maa_help1.setText(self._translate("main_window", "帮助"))
    # 结束页面
    def maa_kill_game_program(self):
        self.maa_choose_kill_game = QtWidgets.QCheckBox(self.maa_kill_game_page)
        self.maa_choose_kill_game.setGeometry(self.ui_zoom(5, 5, 140, 25))
        self.maa_choose_kill_game.setObjectName("maa_choose_kill_game")
        self.maa_choose_kill_game.setText(self._translate("main_window", "关闭模拟器"))
        self.maa_choose_kill_SGA = QtWidgets.QCheckBox(self.maa_kill_game_page)
        self.maa_choose_kill_SGA.setGeometry(self.ui_zoom(5, 35, 140, 25))
        self.maa_choose_kill_SGA.setObjectName("maa_choose_kill_SGA")
        self.maa_choose_kill_SGA.setText(self._translate("main_window", "关闭SGA"))

        self.maa_choose_sleep = QtWidgets.QCheckBox(self.maa_kill_game_page)
        self.maa_choose_sleep.setGeometry(self.ui_zoom(5, 65, 140, 25))
        self.maa_choose_sleep.setObjectName("maa_choose_sleep")
        self.maa_choose_sleep.setText(self._translate("main_window", "电脑睡眠"))
        self.maa_choose_sleep.clicked.connect(self.maa_sleep_click)
        self.maa_continue_Label = QtWidgets.QLabel(self.maa_kill_game_page)
        self.maa_continue_Label.setGeometry(self.ui_zoom(5, 90, 160, 25))
        self.maa_continue_Label.setObjectName("maa_continue_Label")
        self.maa_continue_Label.setText(self._translate("main_window", "继续执行"))
        self.maa_refresh_button = QtWidgets.QPushButton(self.maa_kill_game_page)
        self.maa_refresh_button.setGeometry(self.ui_zoom(60, 90, 25, 25))
        self.maa_refresh_button.setObjectName("maa_refresh")
        self.maa_refresh_button.setIcon(QtGui.QIcon(r"resource\main_window\ui\refresh.png"))
        self.maa_refresh_button.setFlat(True)
        self.maa_refresh_button.clicked.connect(self.maa_refresh)
        self.maa_continue_box = QtWidgets.QComboBox(self.maa_kill_game_page)
        self.maa_continue_box.setGeometry(self.ui_zoom(5, 120, 135, 25))
        self.maa_continue_box.setObjectName("maa_continue_box")
        self.comboboxstyle(self.maa_continue_box)
        self.maa_continue_box.addItems(["不执行"]+self.filelist)
        self.maa_continue_box.currentIndexChanged.connect(self.maa_continue_change)
        self.maa_help2 = QtWidgets.QPushButton(self.maa_kill_game_page)
        self.maa_help2.setGeometry(self.ui_zoom(225, 5, 40, 25))
        self.maa_help2.setObjectName("maa_help2")
        self.maa_help2.setText(self._translate("main_window", "帮助"))
    # 结束页面-关联按钮
    def maa_sleep_click(self):
        if self.maa_choose_sleep.isChecked():
            self.maa_choose_kill_game.setChecked(True)
            self.maa_continue_box.setCurrentIndex(0)
    def maa_continue_change(self):
        if self.maa_continue_box.currentIndex() != 0:
            self.maa_choose_kill_SGA.setChecked(False)
            self.maa_choose_sleep.setChecked(False)
    def maa_set_refresh(self):
        maa_path =self.maa_game_path.text().strip("\"")
        if os.path.isfile(maa_path):
            gui_path = os.path.split(maa_path)[0]+"\config\gui.json"
            with open(gui_path, 'r', encoding='utf-8') as g:
                self.maa_config = json.load(g)
            self.maa_set_box.clear()
            config_list = list(self.maa_config["Configurations"].keys())
            try:config_list.remove("SGA-cache")
            except:pass
            self.maa_set_box.addItems(config_list)
        else:
            self.showtext("maa路径设置错误，请检查。（请使用MAA.exe绝对路径）")
    def maa_refresh(self):
        filedir = "resource\main_window\config"
        self.filelist = []
        for file in os.listdir(filedir):
            name, suffix = os.path.splitext(file)
            if suffix == ".json": self.filelist += [name]
        self.maa_continue_box.clear()
        self.maa_continue_box.addItems(["不执行"] + self.filelist)
    # 以maa工具格式加载设置
    def load_maa(self):
        # 加载功能设置
        self.maa_choose_create.setChecked(True)
        self.maa_choose_kill_game.setChecked(True)
        # 启动设置
        self.maa_game_path.setText(self.configdir["启动路径"])
        self.maa_set_box.clear()
        self.maa_set_box.addItems(self.configdir["运行配置"])
        self.maa_set_box.setCurrentText(self.configdir["默认运行配置"])
        self.maa_choose_kill_game.setChecked(self.configdir["关闭模拟器"])
        self.maa_choose_kill_SGA.setChecked(self.configdir["关闭SGA"])
        self.maa_choose_sleep.setChecked(self.configdir["电脑睡眠"])
        self.maa_continue_box.setCurrentText(self.configdir["继续执行"])
    # 以maa工具格式保存设置
    def save_maa(self):
        self.configdir = {"游戏名称": "MAA"}
        self.configdir["启动路径"] = self.maa_game_path.text().strip("\"")
        config_list = []
        for num in range(self.maa_set_box.count()):
            config_list += [self.maa_set_box.itemText(num)]
        self.configdir["运行配置"] = config_list
        self.configdir["默认运行配置"] = self.maa_set_box.currentText()
        self.configdir["关闭模拟器"] = self.maa_choose_kill_game.isChecked()
        self.configdir["关闭SGA"] = self.maa_choose_kill_SGA.isChecked()
        self.configdir["电脑睡眠"] = self.maa_choose_sleep.isChecked()
        self.configdir["继续执行"] = self.maa_continue_box.currentText()
    # 以maa工具格式-设置文件，整理运行列表
    def create_maa_config_runlist(self):
        start_list = [self.rundir["启动路径"],self.rundir["默认运行配置"]]
        finish_list = [self.rundir["关闭模拟器"],self.rundir["关闭SGA"],self.rundir["电脑睡眠"]]
        return [start_list, finish_list]
    # 以maa工具格式-当前页面，整理运行列表
    def create_maa_main_runlist(self):
        start_list = [self.maa_game_path.text(),self.maa_set_box.currentText()]
        finish_list = [self.maa_choose_kill_game.isChecked(),
                       self.maa_choose_kill_SGA.isChecked(),
                       self.maa_choose_sleep.isChecked()]
        self.continue_config = self.maa_continue_box.currentText()
        return [start_list, finish_list]