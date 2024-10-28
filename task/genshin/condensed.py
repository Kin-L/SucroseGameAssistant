from tools.environment import *
from .genshin import Genshin


class Condensed(Genshin):
    def genshin_make_condensed(self):
        for i in range(3):
            self.tp_fontaine1()
            #走到合成台
            keydown("W")
            wait(4300)
            keyup("W")
            wait(300)
            keydown("D")
            wait(500)
            keyup("D")
            wait(300)
            keydown("W")
            wait(1000)
            keyup("W")
            wait(300)

            if "合成" in ocr((1205, 502, 1315, 578))[0]:
                self.indicate("到达合成台")
                break
            elif i == 2:
                self.indicate("合成树脂未知错误,重试多次")
                return True
            else:
                self.indicate(f"error:合成树脂未知错误,开始重试第{i+1}/2次")
        press("F")
        wait(1000)
        click((960,950))
        wait(1500)
        click((107, 188))
        wait(500)
        click((1339, 408))
        wait(600)
        if "浓缩树脂" in ocr((739, 178, 882, 227))[0]:
            num = int(ocr((996, 887, 1028, 924))[0].strip(" "))
            click((1618, 497))
            wait(600)
            fly = int(ocr((1025, 917, 1134, 941))[0].split("/")[0])
            cons = int(ocr((1162, 917, 1269, 941))[0].split("/")[0])
            self.indicate(f"当前已有:\n"
                          f"  晶核:{fly}个\n"
                          f"  原粹树脂:{cons}/160\n"
                          f"  浓缩树脂:{num}个")
            _n = min(int(cons/40), fly, 5-num)
            if _n:
                """新版本自动选择能做的最大数量浓缩树脂，故注释掉
                for i in range(_n-1):
                    click((1611, 671))
                    wait(400)
                    """
                ori = cons-_n*40
                cond = num+_n
                self.task["resin"] = [ori, cond]
                self.indicate(f"本次合成浓缩树脂{_n}个\n"
                              f"  原粹树脂: {cons} -> {ori}\n"
                              f"  浓缩树脂: {num} -> {cond}")
                click((1727, 1019))
                wait(800)
                click((1173, 786))
                wait(200)
            else:
                self.indicate("浓缩树脂数量达到上限")
        else:
            click((1618, 497))
            wait(600)
            self.indicate("无法合成浓缩树脂:缺少树脂或晶核")
        self.turn_world()
        if self.task["每日奖励"]:
            if _n >= 3:
                self.indicate(f"合成浓缩树脂足够，尝试领取每日奖励")
                self.daily_gift()
            else:
                self.indicate(f"合成浓缩树脂不足，无法领取每日奖励")
        return False

    def daily_gift(self):
        self.home()
        self.open_sub("冒险之证")
        click((291,343)) #点击每日任务页面
        wait(800)
        click((1552,753)) #完成每日任务
        wait(1000)
        click((1552,753))
        wait(1000)
        click((593,851)) #点击领取奖励跳转到地图
        wait(1500)
        self.indicate("前往凯瑟琳")
        click((1634, 1003)) #点击传送
        wait(3000)
        self.turn_world()  #判断传送是否成功
        keydown("W") #跑到凯瑟琳位置
        wait(2700)
        keyup("W")
        wait(500)
        keydown("A")
        wait(1500)
        keyup("A")
        wait(500)
        press("F") #跟凯瑟琳对话
        wait(1000)
        click((960, 900))
        wait(1500)
        x, y = find_pic(r"assets\genshin\picture\condensed\get_daily_gift.png",(1300, 398, 1400, 532))[0]
        if (x, y) == (0, 0):
            self.indicate("未识别到每日任务完成")
            click((1345,800))
        else:
            self.indicate("开始领取每日任务奖励")
            click((x, y))
            wait(2000)
            click((x, y))
            wait(1000)
            click((x , y))
            wait(1000)
            self.indicate("每日任务完成，每日奖励已领取")