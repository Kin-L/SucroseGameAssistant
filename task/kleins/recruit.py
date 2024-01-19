from tools.environment import *
from ..default_task import Task
import os
import time
import shutil


class Recruit(Task):
    def __init__(self):
        super().__init__()

    def kleins_recruit(self):
        click(1469, 697)
        wait(2000)
        _cf = self.task["使用加速"]
        _z1 = [(197, 281, 351, 323), (197, 392, 351, 431), (197, 499, 351, 540)]
        _z2 = [(171, 234, 379, 338), (174, 346, 378, 445), (172, 455, 377, 556)]
        for n in range(3):
            x, y = [(129, 290), (126, 395), (131, 501)][n]
            if ocr(_z1[n])[0] == "访募完成":
                self.indicate("访募%s:完成尝试领取" % (n+1))
                self.receive_recruit(x, y)
            while 1:
                if find_pic("assets/kleins/picture/recruit/new.png", _z2[n])[1] >= 0.6:
                    self.indicate("访募%s:空闲,尝试开始访募" % (n+1))
                    click(x, y)
                    wait(1000)
                    _t = ocr((687, 512, 1025, 574))[0]
                    if "SSR" in _t:
                        self.indicate("发现必出SSR访募!")
                        break
                    elif "SR" in _t:
                        self.indicate("发现必出SR访募")
                        break
                    else:
                        self.indicate("普通访募")
                        for i in range(3):
                            sc = screenshot()
                            try:
                                _fund = int(ocr((1272, 56, 1406, 90), sc)[0].strip(" "))
                                _token = int(ocr((1507, 57, 1616, 90), sc)[0].strip(" "))
                                _expedite = int(ocr((1746, 54, 1846, 90), sc, 0, 0)[0].strip(" "))
                                _f = False
                                break
                            except:
                                os.remove(sc)
                                if i < 2:
                                    self.indicate("识别错误,更换区域")
                                    click(954, 261)
                                    wait(500)
                                else:
                                    self.indicate("识别错误,跳过该招募")
                                    _f = True
                        if _f:
                            break
                        if _token == 0:
                            self.indicate("招募终止:缺少外显记录,")
                            click(296, 75)
                            wait(1000)
                            return 0
                        if _fund < self.task["访募金额"] * 100:
                            self.indicate("招募终止:缺少格")
                            click(296, 75)
                            wait(1000)
                            return 0
                        for i in range(self.task["访募金额"]):
                            click(990, 626)
                            wait(100)
                        click(871, 818)
                        wait(800)
                        self.indicate("舍友访募开始")
                        if not _cf:
                            break
                        else:
                            if _expedite == 0:
                                self.indicate("缺少高速显影剂")
                                _cf = False
                            else:
                                click(743, 811)
                                wait(1000)
                                self.indicate("使用高速显影剂")
                                self.receive_recruit(x, y)
                else:
                    self.indicate("访募%s:进行中" % (n+1))
                    break
        click(296, 75)
        wait(1000)
        
    def receive_recruit(self, x, y):
        click(x, y)
        wait(2500)
        sc = screenshot()
        nv = find_pic("assets/kleins/picture/recruit/N.png", (252, 444, 421, 553), sc)[1]
        rv = find_pic("assets/kleins/picture/recruit/R.png", (252, 444, 421, 553), sc)[1]
        srv = find_pic("assets/kleins/picture/recruit/SR.png", (252, 444, 421, 553), sc)[1]
        rrv = find_pic("assets/kleins/picture/recruit/SSR.png", (252, 444, 468, 553), sc)[1]
        _name = ocr((268, 513, 651, 600), sc)[0].rstrip(" ")
        _list = (nv, rv, srv, rrv)
        max_val = max(_list)
        if max_val:
            now_time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
            max_index = _list.index(max_val)
            if max_index == 0:
                self.indicate(f"访募到N卡 {_name}")
            elif max_index == 1:
                self.indicate(f"访募到R卡 {_name}")
            else:
                shutil.copyfile(sc, f"personal/kleins/recruit/{now_time}.png")
                if max_index == 2:
                    self.indicate(f"访募到SR卡 {_name}\n  可在文件夹“personal/kleins/recruit”中查看")
                else:
                    self.indicate(f"访募到SSR卡! {_name}\n  可在文件夹“personal/kleins/recruit”中查看")
            f = open("personal/kleins/recruit/history.txt", 'a+', encoding='utf-8')
            r = ["N", "R", "SR", "SSR"][max_index]
            f.write(f"{now_time}  {r}  {_name}\n")
            f.close()
        else:
            now_time = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
            shutil.copyfile(sc, f"personal/kleins/recruit/{now_time}.png")
            self.indicate(f"error:舍友访募未知错误 ({now_time}.png)")
            raise RuntimeError("舍友访募未知错误")
        os.remove(sc)
        click(273, 903)
        wait(1500)
        click(273, 903)
        wait(1500)
