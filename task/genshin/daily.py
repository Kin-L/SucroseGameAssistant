from tools.environment import *
from .genshin import Genshin
import os
from tools.software import get_pid, close
import json
from win32gui import FindWindow


class Daily(Genshin):
    def daily_activity(self):
        (ori,num)=self.check_resin()
        if self.task["浓缩树脂"]:        
            if ori >= 40 and num < 5:
                n = self.genshin_make_condensed(ori,num)
            elif num == 5:
                self.indicate("浓缩树脂已满，无法合成浓缩树脂")
                n = 0
            elif ori < 40:
                self.indicate("体力不足，无法合成浓缩树脂")
                n = 0
            else:
                self.indicate("合成浓缩树脂出错")
                return False
        if self.task["每日奖励"] and n >= 3:
            self.daily_gift()
            jiangli = 1
        else:
            jiangli = 0
        if self.task["启用秘境"]:
            self.genshin_domain()
        if jiangli == 0 :
            if self.task["每日奖励"] and ori >= 120:
                self.team_change_to(1)
                self.daily_gift
            elif jiangli == 0:
                self.indicate("消耗体力不足，无法领取每日奖励")

        return False
    
    # 检查树脂
    def check_resin(self):
        self.home()
        self.open_sub("背包")
        wait(500)
        self.check_overdue()
        click((1247, 54))
        wait(500)
        sc = scshot()
        #检查浓缩树脂
        (x, y), val = find_pic(r"assets\genshin\picture\valu_tools\nssz.png",(110, 112, 1273, 805), sc)
        if val > 0.7:
            num = int(ocr((x-15, y+65, x+15, y+92), sc)[0])
        else:
            num = 0
        #检查原粹树脂
        self.home()
        self.open_sub("冒险之证")
        click((300, 440))
        wait(500)
        ori = int((ocr((1368, 200, 1462, 236))[0].split("/")[0]).strip(" "))
        self.indicate(f"当前树脂：\n"
                      f"  原粹树脂: {ori} 个\n"
                      f"  浓缩树脂: {num} 个") 
        self.home()
        return (ori,num)

    #合成浓缩树脂
    def genshin_make_condensed(self,ori,num):
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
        #打开合成台  
        press("F")
        wait(1000)
        click((900,500))
        wait(1000)
        #识别浓缩树脂是否能做
        if "浓缩树脂" in ocr((1256,103, 1428,152))[0]:
            fly = int(ocr((1025, 917, 1134, 941))[0].split("/")[0])
            _n = min(int(ori/40), fly, 5-num)
            if _n:
                ori2 = ori - _n*40
                cond = num + _n
                self.indicate(f"本次合成浓缩树脂{_n}个\n"
                            f"  原粹树脂: {ori} -> {ori2}\n"
                            f"  浓缩树脂: {num} -> {cond}")
                click((1727, 1019))
                wait(800)
                click((1173, 786))
                wait(200)
                self.home()
                return _n
        else:
            wait(600)
            self.indicate("无法合成浓缩树脂:缺少晶核")
        self.home()    

    #领取每日奖励
    def daily_gift(self):
        self.home()
        self.open_sub("冒险之证")
        click((291,343)) #点击每日任务页面
        wait(1200)
        click((1552,753)) #完成每日任务
        wait(800)
        click((1552,753))
        wait(800)
        if "今日奖励已领取" in ocr((447,812,677,890))[0]:
            self.indicate("今日奖励已领取")
            self.home()
            return False
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
            for i in range (5):
                click((x, y))
                wait(800)
            self.indicate("每日任务完成，每日奖励已领取")
        self.home()

    #打秘境
    def genshin_domain(self):
        # 确认BGI路径
        pid = get_pid("BetterGI.exe")
        if pid is not None:
            self.indicate("BGI已启动,准备重启")
            close(pid)
        _path = self.task["启动"]["BGI"]
        if os.path.isfile(_path):
            dire, name = os.path.split(_path)
            if name == "BetterGI.exe":
                pass
            else:
                self.indicate("BGI,无效启动路径")
                return True
        else:
            self.indicate("BGI,无效启动路径")
            return True
        # 传送至秘境
        _domain = self.task["秘境"]
        self.tp_domain(_domain[1])
        click((1690, 1008))
        wait(800)
        self.world()
        self.indicate(f"到达秘境:{_domain[0]} {_domain[1]}")
        # 切换战斗队伍(2号队)
        self.team_change_to(2)
        self.indicate("已切换至战斗队伍")
        if _domain[1] == "太山府":
            pass
        elif _domain[1] == "无妄引咎密宫":
            keydown("W")
            wait(500)
            keyup("W")
            wait(500)
            keydown("A")
            wait(1000)
            keyup("A")
        elif _domain[1] == "芬德尼尔之顶":
            pass
        else:
            keydown("W")
            wait(4000)
            keyup("W")
        # 读取快捷键
        _c = os.path.split(_path)[0] + "/User/config.json"
        with open(_c, 'r', encoding='utf-8') as c:
            _dir = json.load(c)
        # 启动BGI
        def run_bgi():
            cmd = f"start \"\" \"{_path}\""
            for n in range(2):
                run(cmd, shell=True)
                for sec in range(10):
                    wait(1000)
                    hwnd = FindWindow(None, "更好的原神")
                    if hwnd:
                        self.indicate("BGI启动成功")
                        return True
            self.indicate("BGI启动异常")
            return True
        run_bgi()
        wait(3000)
        _s = _dir["hotKeyConfig"]["bgiEnabledHotkey"]
        _d = _dir["hotKeyConfig"]["autoDomainHotkey"]
        from pyautogui import hotkey
        def dopress(key):
            if "+" in key:
                _l = key.split("+")
                for i in range(4-len(_l)):
                    _l += [""]
                _k1, _k2, _k3, _k4 = _l
                hotkey(_k1.strip(" "), _k2.strip(" "), _k3.strip(" "), _k4.strip(" "))
            else:
                press(key)
        dopress(_s)
        wait(1500)
        env.soft.foreground()
        wait(2000)
        dopress(_d)
        wait(1000)
        self.indicate("BGI自动秘境运行中...")
        _dire = os.path.split(_path)[0] + "/log/"
        _name = os.listdir(_dire)[-1]
        path = _dire + _name
        while 1:
            wait(5000)
            f = open(path, encoding='utf-8')
            lines = f.readlines()
            if len(lines) >= 2 and ("→ \"自动秘境结束\"" in lines[-2] or "→ \"任务结束\"" in lines[-2]):
                break
        # env.soft.kill()
        # 关闭BGI
        pid = get_pid("BetterGI.exe")
        if pid is not None:
            close(pid)
        self.indicate("BGI自动秘境运行完成")
        self.home()
        #分解圣遗物
        if self.task["圣遗物分解"] and self.task["秘境"][0] == "圣遗物":
            self.home()
            self.open_sub("背包")
            wait(200)
            click((637,47))
            wait(200)
            click_text("分解",(602,972,758,1059))
            wait(1000)
            click_text("快速选择",(185,981,431,1051))
            wait(500)
            for i in range(4):
                click((270,153+70*i))
                wait(200)
            click_text("确认选择",(270,987,439,1049))
            wait(500)
            click((1733,1013))
            wait(800)
            click_text("进行分解",(1101,734,1292,800))
            wait(1000)
            click((1642,620))
            wait(200)
            click((1642,620))
            wait(200)   
            self.home()
            self.indicate("圣遗物分解完成")
        return False