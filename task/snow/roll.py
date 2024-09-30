from os.path import exists, join
from os import makedirs, startfile
from tools.environment import *
from ..default_task import Task
from json import dump


class Roll(Task):
    def __init__(self):
        super().__init__()

    def snow_roll(self):
        self.indicate("开始获取抽卡记录")
        click_change((1655, 606), (1525, 573, 1611, 624))
        wait_pic(r"assets\snow\picture\home.png", (1504, 0, 1771, 117))
        current = {
            "特选角色共鸣": [],
            "特选武器共鸣": [],
            "限定角色共鸣": [],
            "限定武器共鸣": [],
            "常守之誓": [],
            "中庭炉心": [],
            "新手池": []
        }

        # if os.path.exists(his_path):
        #     with open(his_path, 'r', encoding='utf-8') as m:
        #         _dir = json.load(m)
        #     current.update(_dir)
        # else:
        #     open(his_path, 'a', encoding='utf-8')

        if True in self.task["共鸣记录"]:
            pass
        else:
            self.indicate("共鸣记录：请至少勾选一个卡池选项")
            return True
        roll_list = []
        if self.task["共鸣记录"][0]:
            roll_list += ["特选角色共鸣"]
        if self.task["共鸣记录"][1]:
            roll_list += ["特选武器共鸣"]
        if self.task["共鸣记录"][2]:
            roll_list += ["限定角色共鸣"]
        if self.task["共鸣记录"][3]:
            roll_list += ["限定武器共鸣"]
        if self.task["共鸣记录"][4]:
            roll_list += ["常守之誓"]
        if self.task["共鸣记录"][5]:
            roll_list += ["中庭炉心"]
        if self.task["共鸣记录"][6]:
            roll_list += ["新手池"]
        for i in roll_list:
            if i == "特选角色共鸣":
                pos = find_text("常守", (3, 67, 280, 1066))
                click_to_text(pos, "出", (377, 227, 490, 292))
                x, y = find_text("100", (3, 67, 280, 1066))
                click_change((x-90, y+35), (349, 854, 389, 897))
                click_to_text((x-90, y+120), "角色", (465, 959, 702, 1002))
            elif i == "特选武器共鸣":
                pos = find_text("常守", (3, 67, 280, 1066))
                click_to_text(pos, "出", (377, 227, 490, 292))
                x, y = find_text("100", (3, 67, 280, 1066))
                click_change((x - 90, y + 35), (349, 854, 389, 897))
                click_to_text((x - 90, y + 210), "武器", (465, 959, 702, 1002))
            elif i == "限定角色共鸣":
                pos = find_text("常守", (3, 67, 280, 1066))
                click_to_text(pos, "出", (377, 227, 490, 292))
                x, y = find_text("50", (3, 67, 280, 1066))
                click_change((x - 90, y + 35), (349, 854, 389, 897))
                click_to_text((x - 90, y + 120), "角色", (494, 994, 645, 1035))
            elif i == "限定武器共鸣":
                pos = find_text("常守", (3, 67, 280, 1066))
                click_to_text(pos, "出", (377, 227, 490, 292))
                x, y = find_text("50", (3, 67, 280, 1066))
                click_change((x - 90, y + 35), (349, 854, 389, 897))
                click_to_text((x - 90, y + 210), "武器", (494, 994, 645, 1035))
            elif i == "常守之誓":
                pos = find_text("常守", (3, 67, 280, 1066))
                click_to_text(pos, "出", (377, 227, 490, 292))
            elif i == "中庭炉心":
                pos = find_text("中庭炉心", (3, 67, 280, 1066))
                click_to_text(pos, "出", (377, 227, 490, 292))
            elif i == "新手池":
                pos = find_text("启程", (3, 67, 280, 1066))
                click_to_text(pos, "到", (324, 71, 500, 129))
            wait(500)
            click_change((1877, 141), (1858, 117, 1903, 163))
            wait(500)
            click_change((1081, 84), (379, 177, 579, 215))
            _num = 0
            _time = 0
            while 1:
                wait(100)
                if find_pic(r"assets\snow\picture\rollcheck.png")[1]:
                    _num = 0
                else:
                    _num += 1
                _time += 1
                if _time == 200:
                    self.indicate("尘白禁区: 获取共鸣记录等待超时")
                    raise RuntimeError("尘白禁区: 获取共鸣记录等待超时")
                else:
                    if _num == 4:
                        break
                    else:
                        pass

            _nl = []
            _p = 0
            page_pic = None
            while 1:
                _sc = scshot()
                if page_pic is not None:
                    u = 0
                    for u in range(3):
                        centre, sim = find_pic(page_pic, (1621, 475, 1729, 569), _sc)
                        if sim >= 0.95:
                            if u == 2:
                                break
                            else:
                                click((1666, 602))
                                wait(600)
                        else:
                            break
                    if u == 2:
                        break
                _sc = scshot()
                page_pic = _sc[488:555, 1635:1716]
                _list1 = ocr((357, 185, 685, 866), _sc, 1)
                _list2 = ocr((1357, 185, 1561, 866), _sc, 1)

                num = 0
                _p += 1
                _line = []
                _lf = 0
                for row in _list1:
                    row = row[0].strip(" ")
                    if row:
                        _tline = _list2[num][0]
                        if _tline[10] != " ":
                            _tline = _tline[:10] + " " + _tline[10:]
                        _color = "未知"
                        _zone = (342, 216+68*num, 362, 216+68*num+5)
                        if find_color("blue", _zone, _sc)[1]:
                            _color = "blue"
                        elif find_color("purple", _zone, _sc)[1]:
                            _color = "purple"
                        elif find_color("orange", _zone, _sc)[1]:
                            _color = "orange"

                        _line = [row, _tline, _color]

                        if _p != 1:
                            if _line[:2] == _nl[9][:2]:
                                _lf += 1
                        _nl = [_line] + _nl
                        _line = []
                        num += 1
                    else:
                        break
                del _sc
                if num < 10:
                    break
                else:
                    click((1666, 602))
                    wait(600)
            current[i] += _nl
            click_change((1851, 81), (1834, 64, 1872, 103))
            wait(1000)
        click_pic(r"assets\snow\picture\home.png", (1504, 0, 1771, 117))
        wait(500)
        self.indicate("获取抽卡记录完成")
        self.roll_arrange(current)

    def roll_arrange(self, _dir):
        import time
        now = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
        his_path = f"personal/snow/roll/cache/history - {now}.json"
        _path = r"personal/snow/roll/cache"
        if not exists(_path):
            makedirs("personal/snow/roll/cache")
        with open(his_path, 'a', encoding='utf-8') as x:
            dump(_dir, x, ensure_ascii=False, indent=1)
        self.indicate("抽卡记录已暂存")
        from openpyxl import load_workbook
        from openpyxl.styles import Font, Alignment
        src = r"assets\snow\default_snow_roll.xlsx"
        dst = f"personal/snow/roll/尘白禁区共鸣记录 - {now}.xlsx"
        import shutil
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
            for _line in _list:
                [r, t, col] = _line
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
                elif "九夜之" in r:
                    r = "九夜之冕"
                elif "龙舌兰" in r:
                    r = "薇蒂雅-龙舌兰"

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
                if col == "blue":
                    _fon = fon_three
                    count[0] += 1
                elif col == "purple":
                    _fon = fon_four
                    count[1] += 1
                    count[5] += [f"{r}({n_four})"]
                    n_four = 0
                elif col == "orange":
                    _fon = fon_five
                    count[2] += 1
                    count[6] += [f"{r}({n_five})"]
                    n_five = 0
                else:
                    print(r, t)
                    self.indicate(f"稀有度异常识别异常:{r}", 3)
                    return False
                _sheet[f"A{n_row}"].font = _fon
                _sheet[f"B{n_row}"].font = _fon
                _sheet[f"C{n_row}"].font = fon2
                _sheet[f"D{n_row}"].font = fon2
                _sheet.row_dimensions[n_row].height = 18
            count[3] = n_row - 1
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
        self.indicate("共鸣记录已导出", 3)
        if self.task["共鸣记录"][7]:
            startfile(join(env.workdir, dst))
