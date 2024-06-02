# -*- coding:gbk -*-
import os.path
from tools.environment import *
from ..default_task import Task
import json


class Roll(Task):
    def __init__(self):
        super().__init__()

    def snow_roll(self):
        self.indicate("开始获取抽卡记录")
        click((1731, 678))
        for i in range(10):
            wait(1000)
            if "共鸣" in ocr((1686, 940, 1843, 1006))[0]:
                break
            elif i < 9:
                wait(1000)
            else:
                self.indicate("尘白禁区: 获取共鸣记录等待超时")
                raise RuntimeError("尘白禁区: 获取共鸣记录等待超时")
        wait(1200)
        current = {
            "特选角色共鸣": [],
            "特选武器共鸣": [],
            "限定角色共鸣": [],
            "限定武器共鸣": [],
            "常守之誓": [],
            "中庭炉心": [],
            "新手池": []
        }
        his_path = "personal/snow/roll/history.json"
        if os.path.exists(his_path):
            with open(his_path, 'r', encoding='utf-8') as m:
                _dir = json.load(m)
            current.update(_dir)
        else:
            open(his_path, 'a', encoding='utf-8')

        for i in ["特选角色共鸣", "特选武器共鸣", "限定角色共鸣", "限定武器共鸣", "常守之誓", "中庭炉心", "新手池"]:
            if i == "特选角色共鸣":
                click_text("常守", (3, 67, 280, 1066))
                wait(500)
                x, y = find_text("100", (3, 67, 280, 1066))
                click((x, y))
                wait(1000)
                click((x-90, y+117))
            elif i == "特选武器共鸣":
                click_text("常守", (3, 67, 280, 1066))
                wait(500)
                x, y = find_text("100", (3, 67, 280, 1066))
                click((x, y))
                wait(1000)
                click((x-90, y + 180))
            elif i == "限定角色共鸣":
                click_text("常守", (3, 67, 280, 1066))
                wait(500)
                x, y = find_text("50", (3, 67, 280, 1066))
                click((x, y))
                wait(1000)
                click((x-90, y+117))
            elif i == "限定武器共鸣":
                click_text("常守", (3, 67, 280, 1066))
                wait(500)
                x, y = find_text("50", (3, 67, 280, 1066))
                click((x, y))
                wait(1000)
                click((x-90, y + 180))
            elif i == "常守之誓":
                if click_text("常守", (3, 67, 280, 1066)):
                    pass
                else:
                    continue
            elif i == "中庭炉心":
                if click_text("中庭炉心", (3, 67, 280, 1066)):
                    pass
                else:
                    continue
            elif i == "新手池":
                if click_text("启程", (3, 67, 280, 1066)):
                    pass
                else:
                    continue
            wait(800)
            click((1877, 141))
            wait(2000)
            click((1081, 84))
            wait(1000)
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

            _l = current[i]
            _nl = []
            _p = 0
            while 1:
                _list1 = ocr((357, 185, 685, 866), mode=1)
                _list2 = ocr((1357, 185, 1561, 866), mode=1)
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
                        _line = [row, _tline]

                        if _p != 1:
                            if _line == _nl[9]:
                                _lf += 1
                        if _line not in _l:
                            _nl = [_line] + _nl
                            _line = []
                        else:
                            break
                        num += 1
                    else:
                        break
                if num < 10:
                    break
                elif _lf == 10:
                    _nl = _nl[10:]
                    break
                else:
                    click((1666, 602))
                    wait(500)
            current[i] += _nl
            click((1851, 81))
            wait(2000)
        with open("personal/snow/roll/history.json", 'w', encoding='utf-8') as x:
            json.dump(current, x, ensure_ascii=False, indent=1)
        click((1674, 46))
        wait(2000)
        self.indicate("获取抽卡记录完成")
