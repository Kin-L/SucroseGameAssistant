# -*- coding:gbk -*-
import os
import webbrowser
from .list import SnowList
from .stack import SnowStack
from ui.element.control import *
from tools.environment import env
from tools.system import check_path


# 尘白禁区模组设置窗口
class Snow:
    def __init__(self, stack, icon, main):
        self.main = main
        self.widget_snow = Widget()
        stack.addWidget(self.widget_snow)
        self.button_snow = (
            PicButton(icon, (275, 0, 50, 50),
                      r"assets\snow\picture\snow-icon.png", (50, 50)))
        self.list = None
        self.set = None

    def load_window(self):
        self.list = SnowList(self.widget_snow, (0, 0, 215, 515))
        self.set = SnowStack(self.widget_snow, (225, 0, 410, 515))
        self.list.set_snow.clicked.connect(lambda: self.set.stack.setCurrentIndex(0))
        self.list.set_fight.clicked.connect(lambda: self.set.stack.setCurrentIndex(1))
        self.list.set_daily.clicked.connect(lambda: self.set.stack.setCurrentIndex(2))
        self.list.set_mail.clicked.connect(lambda: self.set.stack.setCurrentIndex(3))
        self.list.set_roll.clicked.connect(lambda: self.set.stack.setCurrentIndex(4))

        self.set.button_wiki.clicked.connect(self.open_wiki)
        self.set.button_arrange.clicked.connect(self.roll_arrange)
        self.set.button_open_roll.clicked.connect(self.open_roll_directory)
        Line(self.widget_snow, (215, 5, 3, 505), False)

    def load_run(self, run):
        _dir = {
            "server": 0,
            "snow_path": ""
        }
        _dir.update(run)
        self.set.combo_server.setCurrentIndex(_dir["server"])
        self.set.line_start.setText(_dir["snow_path"])
        self.set.line_start.setSelection(0, 0)

    def get_run(self):
        _dir = {
            "server": self.set.combo_server.currentIndex(),
            "snow_path": check_path(self.set.line_start.text())
        }
        return _dir

    def input_config(self, _dir):
        config = {
            "模块": 5,
            "预下载": False,
            "更新": False,
            "静音": False,
            "关闭软件": False,
            "完成后": 0,
            "SGA关闭": False,
            "账号选择": "",
            "功能0": False,
            "功能1": False,
            "功能2": False,
            "功能3": False,
            "功能4": False,
            "感知互赠": False,
            "每日配给": False,
            "使用试剂": False,
            "行动选择": 0,
            "后勤选择": "底比斯小队",
            "活动后勤选择": "明夷小队",
            "个人故事": [False, False, "未选择", "未选择", "未选择", "未选择"],
            "拟境扫荡": False,
            "商店购物": [False, "新手战斗记录", "初级职级认证"],
            "武器升级": False,
            "领取日常": False,
            "领取凭证": False,
            "活动每日": False
        }
        config.update(_dir)
        self.set.check_preload.setChecked(config["预下载"])
        self.set.check_update.setChecked(config["更新"])
        self.set.independent.check_mute.setChecked(config["静音"])
        self.set.independent.check_kill_game.setChecked(config["关闭软件"])
        self.set.independent.combo_after.setCurrentIndex(config["完成后"])
        self.set.independent.check_kill_sga.setChecked(config["SGA关闭"])
        self.set.line_account.setText(config["账号选择"])
        self.set.line_account.setSelection(0, 0)

        self.list.check_fight.setChecked(config["功能0"])
        self.list.check_daily.setChecked(config["功能1"])
        self.list.check_mail.setChecked(config["功能2"])
        self.list.check_roll.setChecked(config["功能3"])

        self.set.check_share.setChecked(config["感知互赠"])
        self.set.check_supply.setChecked(config["每日配给"])
        self.set.check_reagent.setChecked(config["使用试剂"])
        self.set.mat.setCurrentIndex(config["行动选择"])
        self.set.logistics.setCurrentText(config["后勤选择"])
        self.set.logistics1.setCurrentText(config["活动后勤选择"])

        self.set.check_character.setChecked(config["个人故事"][0])
        self.set.check_supplement.setChecked(config["个人故事"][1])
        self.set.character1.setCurrentText(config["个人故事"][2])
        self.set.character2.setCurrentText(config["个人故事"][3])
        self.set.character3.setCurrentText(config["个人故事"][4])
        self.set.character4.setCurrentText(config["个人故事"][5])

        self.set.check_imitate.setChecked(config["拟境扫荡"])
        self.set.check_market.setChecked(config["商店购物"][0])
        self.set.box_market1.setCurrentText(config["商店购物"][1])
        self.set.box_market2.setCurrentText(config["商店购物"][2])
        self.set.check_weapon.setChecked(config["武器升级"])
        self.set.check_daily.setChecked(config["领取日常"])
        self.set.check_daily2.setChecked(config["领取凭证"])
        self.set.check_daily3.setChecked(config["活动每日"])

    def output_config(self):
        config = dict()
        config["模块"] = 5

        config["预下载"] = self.set.check_preload.isChecked()
        config["更新"] = self.set.check_update.isChecked()
        config["静音"] = self.set.independent.check_mute.isChecked()
        config["关闭软件"] = self.set.independent.check_kill_game.isChecked()
        config["完成后"] = self.set.independent.combo_after.currentIndex()
        config["SGA关闭"] = self.set.independent.check_kill_sga.isChecked()
        config["账号选择"] = self.set.line_account.text()

        config["功能0"] = self.list.check_fight.isChecked()
        config["功能1"] = self.list.check_daily.isChecked()
        config["功能2"] = self.list.check_mail.isChecked()
        config["功能3"] = self.list.check_roll.isChecked()

        config["感知互赠"] = self.set.check_share.isChecked()
        config["每日配给"] = self.set.check_supply.isChecked()
        config["使用试剂"] = self.set.check_reagent.isChecked()
        config["行动选择"] = self.set.mat.currentIndex()
        config["后勤选择"] = self.set.logistics.currentText()
        config["活动后勤选择"] = self.set.logistics1.currentText()
        config["个人故事"] = [
            self.set.check_character.isChecked(),
            self.set.check_supplement.isChecked(),
            self.set.character1.currentText(),
            self.set.character2.currentText(),
            self.set.character3.currentText(),
            self.set.character4.currentText()]
        config["拟境扫荡"] = self.set.check_imitate.isChecked()
        config["商店购物"] = [
            self.set.check_market.isChecked(),
            self.set.box_market1.currentText(),
            self.set.box_market2.currentText()]
        config["武器升级"] = self.set.check_weapon.isChecked()
        config["领取日常"] = self.set.check_daily.isChecked()
        config["领取凭证"] = self.set.check_daily2.isChecked()
        config["活动每日"] = self.set.check_daily3.isChecked()
        return config

    def open_roll_directory(self):
        os.startfile(env.workdir + "/personal/snow/roll")
        self.main.indicate("打开文件夹: 共鸣记录", 1)

    def open_wiki(self):
        webbrowser.open("https://wiki.biligame.com/sonw/%E9%A6%96%E9%A1%B5")
        self.main.indicate("打开网页: 尘白禁区 BWIKI", 1)

    def roll_arrange(self):
        import json
        with open("personal/snow/roll/history.json", 'r', encoding='utf-8') as m:
            _dir = json.load(m)
        from openpyxl import load_workbook
        from openpyxl.styles import Font, Alignment
        import time
        now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        import shutil
        src = r"assets\snow\default_snow_roll.xlsx"
        dst = f"personal/snow/roll/尘白禁区共鸣记录 - {now}.xlsx"
        shutil.copyfile(src, dst)
        wb = load_workbook(dst)
        fon2 = Font(name='宋体', size=12)
        fon_three = Font(name='宋体', size=12, color="3374F8")
        fon_four = Font(name='宋体', size=12, color="7E30FF", bold=True)
        fon_five = Font(name='宋体', size=12, color="FFC332", bold=True)
        al = Alignment(horizontal='center', vertical='center')
        _count = []
        for i in ["特选角色共鸣", "特选武器共鸣", "限定角色共鸣", "限定武器共鸣", "常守之誓", "中庭炉心", "新手池"]:
            _sheet = wb[i]

            _list = _dir[i]
            n_row = 1
            n_four = 0
            n_five = 0
            count = [0, 0, 0, 0, 0, [], []]
            for [r, t] in _list:
                n_row += 1
                n_four += 1
                n_five += 1
                if "日王牌" in r:
                    r = "晴-旧日王牌"
                elif "芬妮" in r:
                    if "冠" in r:
                        r = "芬妮-咎冠"
                elif "琴诺" in r:
                    if "悖" in r or "谬" in r:
                        r = "琴诺-悖谬"
                elif "不予显示" in r:
                    r = "安卡希雅-[不予显示]"
                elif "热年代" in r:
                    r = "灸热年代"
                elif "姐姐大人" in r:
                    r = "恩雅-姐姐大人"
                elif "王权连" in r:
                    r = "王权连枷"
                elif "瑞斯" in r and "刻" in r:
                    r = "瑟瑞斯-瞬刻"

                _a = _sheet[f"A{n_row}"]
                _b = _sheet[f"B{n_row}"]
                _c = _sheet[f"C{n_row}"]
                _d = _sheet[f"D{n_row}"]
                _sheet[f"A{n_row}"] = t
                _sheet[f"B{n_row}"] = r
                _sheet[f"C{n_row}"] = n_row - 1
                _sheet[f"D{n_row}"] = n_five
                _sheet[f"A{n_row}"].alignment = al
                _sheet[f"B{n_row}"].alignment = al
                _sheet[f"C{n_row}"].alignment = al
                _sheet[f"D{n_row}"].alignment = al
                if r in ["无声雷电", "泥雪", "皮斯科", "锤击",
                         "马尔贝克", "沉默的真相", "天空墙", "教训",
                         "半根火炬", "冰冷沙丘", "灰狗", "绝缘体",
                         "群鸟仇人", "有人在吗", "黑衣拿破仑", "安全线",
                         "偏头痛", "铸铁卫士", "无礼之辈", "简易扳手",
                         "冬青木", "朗姆风暴", "钢之白桦林", "湖中女神",
                         "重锤"]:
                    _fon = fon_three
                    count[0] += 1
                elif r in ["安卡希雅-[不予显示]", "肴-养生专家", "芬妮-黄金狮子", "恩雅-姐姐大人",
                           "猫汐尔-猫猫", "辰星-观测者", "琴诺-双面", "茉莉安-绷带小姐",
                           "里芙-星期三", "晴-旧日王牌", "妮塔-四手", "芙提雅-小太阳",
                           "瑟瑞斯-小金鱼",
                           "旧日叹息", "小小工具", "关键点", "彩虹打火机",
                           "烂橘子", "不协和音", "大宝贝儿", "霓虹灯管",
                           "幸运时刻", "野性装修", "小黄鸭", "腐肉便利店",
                           "是！是！船长！", "楼道怪猫", "怒不可遇", "草莓蛋糕",
                           "舒适圈", "机械警官", "龙涎香", "北极狐",
                           "军舰鸟", "次氯酸", "正在施工", "归来",
                           "青金石", "深海呼唤", "甜甜灵魂", "迷乱迪斯科",
                           "电离水母", "瓦尔基里2056", "喧哗现场", "灸热年代",
                           "湿地公园", "指示剂"]:
                    _fon = fon_four
                    count[1] += 1
                    count[5] += [f"{r}({n_four})"]
                    n_four = 0
                elif r in ["安卡希雅-辉夜", "辰星-云篆", "晴-藏锋", "猫汐尔-溯影",
                           "苔丝-魔术师", "伊切尔-豹豹", "凯茜雅-蓝闪", "琴诺-悖谬",
                           "恩雅-羽蜕", "瑟瑞斯-瞬刻",
                           "松林极光", "朱书断邪", "普赛克16", "合金真理",
                           "王牌怪诞", "海王星", "镭射风虎", "白夜别诗",
                           "渊光", "王权连枷",
                           "芬妮-咎冠", "肴-冬至", "里芙-狂猎", "茉莉安-雨燕", "芙提雅-缄默",
                           "小粮食", "星辰大海", "审判前夜", "熔岩骨骼",
                           "太阳酬金", "虎鲸号角", "太空骑手", "百战老兵",
                           "奥林匹斯", "星尘回忆"]:
                    _fon = fon_five
                    count[2] += 1
                    count[6] += [f"{r}({n_five})"]
                    n_five = 0
                else:
                    print(r, t)
                    self.main.indicate(f"稀有度异常识别异常:{r}", 3)
                    return False
                _sheet[f"A{n_row}"].font = _fon
                _sheet[f"B{n_row}"].font = _fon
                _sheet[f"C{n_row}"].font = fon2
                _sheet[f"D{n_row}"].font = fon2
                _sheet.row_dimensions[n_row].height = 18
            count[3] = n_row-1
            count[4] = n_five
            _count += [count]
        sheet0 = wb["总览"]
        sheet0["B3"] = _count[0][0]
        sheet0["C3"] = _count[0][1]
        sheet0["D3"] = _count[0][2]
        sheet0["E3"] = _count[0][3]
        sheet0["F3"] = _count[0][4]

        _list = _count[0][5]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I2"] = _str
        _list = _count[0][6]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I3"] = _str

        sheet0["B6"] = _count[1][0]
        sheet0["C6"] = _count[1][1]
        sheet0["D6"] = _count[1][2]
        sheet0["E6"] = _count[1][3]
        sheet0["F6"] = _count[1][4]
        _list = _count[1][5]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I5"] = _str

        _list = _count[1][6]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I6"] = _str

        sheet0["B9"] = _count[2][0]
        sheet0["C9"] = _count[2][1]
        sheet0["D9"] = _count[2][2]
        sheet0["E9"] = _count[2][3]
        sheet0["F9"] = _count[2][4]
        _list = _count[2][5]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I8"] = _str

        _list = _count[2][6]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I9"] = _str

        sheet0["B12"] = _count[3][0]
        sheet0["C12"] = _count[3][1]
        sheet0["D12"] = _count[3][2]
        sheet0["E12"] = _count[3][3]
        sheet0["F12"] = _count[3][4]
        _list = _count[3][5]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I11"] = _str

        _list = _count[3][6]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I12"] = _str

        sheet0["B15"] = _count[4][0]
        sheet0["C15"] = _count[4][1]
        sheet0["D15"] = _count[4][2]
        sheet0["E15"] = _count[4][3]
        sheet0["F15"] = _count[4][4]
        _list = _count[4][5]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I14"] = _str

        _list = _count[4][6]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I15"] = _str

        sheet0["B18"] = _count[5][0]
        sheet0["C18"] = _count[5][1]
        sheet0["D18"] = _count[5][2]
        sheet0["E18"] = _count[5][3]
        sheet0["F18"] = _count[5][4]
        _list = _count[5][5]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I17"] = _str

        _list = _count[5][6]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I18"] = _str

        sheet0["B21"] = _count[6][0]
        sheet0["C21"] = _count[6][1]
        sheet0["D21"] = _count[6][2]
        sheet0["E21"] = _count[6][3]
        sheet0["F21"] = _count[6][4]
        _list = _count[6][5]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I20"] = _str

        _list = _count[6][6]
        _str = ""
        for i in _list:
            _str += i + " "
        sheet0["I21"] = _str
        wb.save(dst)
        self.main.indicate("共鸣记录已导出", 3)
