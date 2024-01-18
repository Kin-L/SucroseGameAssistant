import os

from tools.environment import *
from ..default_task import Task


class Review(Task):
    def __init__(self):
        super().__init__()

    def kleins_review(self):
        _float = self.task["回顾"]
        if _float % 1 == 0:
            _num = int(_float)
        else:
            _num = round(_float, 1)
        click(1628, 946)
        wait(1000)
        click(258, 386)
        wait(1000)
        # 战术支援
        _list = [613, 779, 954, 1132, 1295, 1502, 1666, 798]
        for num in range(3):
            for _x in _list:
                click(_x, 795)
                wait(300)
            if num < 2:
                click(1646, 347)
                wait(500)
            if num < 1:
                wait(8500)
        self.indicate("战术支援完成")
        # 战术回顾
        click(293, 277)
        wait(500)
        _list = [(575, 820, 825, 868),
                 (1003, 821, 1252, 867),
                 (1430, 822, 1680, 867)]
        sc = screenshot()
        for n in range(3):
            _text = ocr(_list[n], sc)[0]
            if _text == "回顾完成":
                self.indicate("战术回顾%s:已完成" % n)
                click([704, 1134, 1562][n], 846)
                wait(1000)
                click(1648, 858)
                wait(1000)
                click(1060, 868)
                wait(1500)
            elif (":" in _text) or ("：" in _text):
                self.indicate("战术回顾%s:进行中" % n)
                continue
            elif _text == "进行回顾":
                self.indicate("战术回顾%s:空闲" % n)
            else:
                self.indicate("error:战术回顾%s 识别异常" % n)
                raise RuntimeError("战术回顾%s 识别异常" % n)
            self.indicate("尝试创建战术回顾")
            x, y = [(703, 846), (1130, 846), (1557, 847)][n]
            click(x, y)
            wait(1000)
            click(734, 846)
            wait(500)
            _p = str(_num) + "%"
            _f = False
            for c in range(35):
                text_list = ocr((694, 153, 761, 938), mode=1)
                for _t in text_list:
                    if _t[0] == _p:
                        x, y = center(_t[1])
                        click(x, y)
                        wait(400)
                        click(524, 1007)
                        wait(1000)
                        _f = True
                        break
                if _f:
                    break
                roll(476, 833, -19)
                wait(800)
                if c == 34:
                    click(144, 70)
                    wait(500)
                    click(700, 845)
                    wait(800)
                    click(586, 226)
                    wait(500)
            click(1652, 875)
            self.indicate("战术回顾%s开始" % n)
            wait(1500)
        os.remove(sc)
        # 结束
        click(296, 75)
        wait(1000)
