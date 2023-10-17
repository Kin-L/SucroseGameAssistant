# -*- coding:gbk -*-
from function import *
from PyQt5.QtCore import  QThread,pyqtSignal
import sys,json
# pyinstaller -D -w D:\Kin-project\python\venv\yuanshen\yuanshen.py
class Fly(object):
    # 捉晶蝶-阿如村上方
    def fly1(self):
        self.home()
        self.testsignal.emit("捉晶蝶-阿如村上方")
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("赤金的废墟")
        click(962, 738)
        wait(800)
        self.tp_point(0)
        keydown("D")
        wait(4700)
        keyup("D")
        wait(500)
        keydown("W")
        wait(6000)
        keyup("W")
        wait(500)
        keydown("D")
        wait(150)
        keyup("D")
        wait(500)
        keydown("W")
        wait(3900)
        press("SPACE")
        wait(400)
        press("F")
        wait(500)
        keyup("W")
    # 捉晶蝶-舍身陷坑下方
    def fly2(self):
        self.home()
        self.testsignal.emit("捉晶蝶-舍身陷坑下方")
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("赤金的废墟")
        click(1872, 34)
        wait(800)
        drag((960, 967), (0, -800))
        wait(500)
        click(832, 732)
        wait(800)
        self.tp_point(0)
        keydown("W")
        wait(1300)
        keyup("W")
        wait(500)
        keydown("A")
        for i in range(7):
            wait(300)
            press("F")
        keyup("A")
    # 捉晶蝶-活力之家下方
    def fly3(self):
        self.home()
        self.testsignal.emit("捉晶蝶-活力之家下方")
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("赤金的废墟")
        click(1872, 34)
        wait(800)
        drag((960, 967), (0, -800))
        wait(500)
        click(1152, 739)
        wait(800)
        self.tp_point(0)
        keydown("A")
        wait(2800)
        keyup("A")
        wait(500)
        keydown("S")
        wait(5400)
        keyup("S")
        wait(500)
        keydown("A")
        wait(2100)
        keyup("A")
        wait(500)
        keydown("W")
        for i in range(5):
            wait(300)
            press("F")
        wait(200)
        keyup("W")
        wait(500)
    # 捉晶蝶-化城郭左方
    def fly4(self):
        self.home()
        self.testsignal.emit("捉晶蝶-化城郭左方")
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("缘觉塔")
        click(577, 692)
        wait(800)
        self.tp_point(0)
        keydown("S")
        for i in range(4):
            wait(300)
            press("F")
        keyup("S")
        wait(500)
        keydown("D")
        for i in range(4):
            wait(300)
            press("F")
        keyup("D")
        wait(500)
        keydown("S")
        wait(5000)
        keyup("S")
        wait(500)
        keydown("A")
        wait(1600)
        press("SPACE")
        wait(1600)
        keyup("A")
        wait(500)
        keydown("W")
        wait(500)
        keyup("W")
        wait(500)
        press("2")
        wait(800)
        press("E")
        wait(200)
        keydown("W")
        for i in range(8):
            wait(300)
            press("F")
        keyup("W")
        wait(500)
        press("1")
    # 捉晶蝶-层岩巨渊地面七天神像
    def fly5(self):
        self.home()
        self.testsignal.emit("捉晶蝶-层岩巨渊地面七天神像")
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("岩中幽谷")
        click(878, 698)
        wait(800)
        self.tp_point(2)
        keydown("A")
        for i in range(8):
            wait(300)
            press("F")
        wait(200)
        keyup("A")
        wait(500)
        keydown("W")
        for i in range(7):
            wait(300)
            press("F")
        wait(100)
        keyup("W")
        wait(500)
        keydown("A")
        for i in range(10):
            wait(300)
            press("F")
        keyup("A")
        wait(500)
        keydown("W")
        for i in range(7):
            wait(300)
            press("F")
        keyup("W")
    # 捉晶蝶-稻妻平海砦
    def fly6(self):
        self.home()
        self.testsignal.emit("捉晶蝶-稻妻平海砦")
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("沉眠之庭")
        click(1139, 528)
        wait(800)
        self.tp_point(0)
        keydown("S")
        for i in range(12):
            wait(300)
            press("F")
        keyup("S")
        wait(500)
        keydown("D")
        for i in range(2):
            wait(300)
            press("F")
        keyup("D")
        wait(500)
        keydown("S")
        for i in range(5):
            wait(300)
            press("F")
        keyup("S")
        wait(500)
        keydown("A")
        for i in range(4):
            wait(300)
            press("F")
        keyup("A")
        wait(500)
        keydown("W")
        for i in range(5):
            wait(300)
            press("F")
        keyup("W")
        wait(500)
class Cut_tree(object):
    # 悬铃木
    def mallow(self):
        self.testsignal.emit("采集：悬铃木×9，椴木×3")
        self.home()
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("罪祸的终末")
        wait(800)
        click(1682, 1008)
        self.world()
        keydown("S")
        wait(10000)
        keyup("S")
        wait(300)
        keydown("D")
        wait(300)
        keyup("D")
        wait(300)
        keydown("S")
        wait(2000)
        keyup("S")
        wait(300)
        keydown("A")
        wait(1000)
        keyup("A")
        wait(500)
        press("Z")
        wait(500)
    # 炬木
    def torch(self):
        self.testsignal.emit("采集：炬木×15")
        self.home()
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("苍白的遗荣")
        click(545, 1000)
        wait(800)
        self.tp_point(1)
        keydown("A")
        wait(3300)
        keyup("A")
        wait(500)
        keydown("W")
        wait(3000)
        keyup("W")
        wait(500)
        keydown("A")
        wait(1200)
        keyup("A")
        wait(500)
        press("Z")
        wait(500)
    # 白梣木
    def ash(self):
        self.testsignal.emit("采集：白梣木×12")
        self.home()
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("苍白的遗荣")
        click(522, 808)
        wait(800)
        self.tp_point(2)
        keydown("S")
        wait(8000)
        keyup("S")
        wait(500)
        keydown("A")
        wait(7000)
        keyup("A")
        wait(500)
        keydown("W")
        wait(3400)
        keyup("W")
        wait(500)
        keydown("A")
        wait(4700)
        keyup("A")
        wait(500)
        press("Z")
        wait(500)
    # 椴木
    def linden(self):
        self.testsignal.emit("采集：椴木×9")
        self.home()
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("罪祸的终末")
        wait(800)
        click(1682, 1008)
        self.world()
        keydown("S")
        wait(2500)
        keyup("S")
        wait(500)
        keydown("A")
        wait(2500)
        keyup("A")
        wait(300)
        keydown("W")
        wait(11800)
        keyup("W")
        wait(300)
        keydown("A")
        wait(100)
        keyup("A")
        wait(300)
        press("Z")
        wait(500)
    # 香柏木
    def cypress(self):
        self.testsignal.emit("采集：香柏木×15")
        self.home()
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("罪祸的终末")
        click(1213, 201)
        wait(800)
        self.tp_point(0)
        keydown("S")
        wait(4000)
        keyup("S")
        wait(500)
        keydown("D")
        wait(6000)
        keyup("D")
        wait(500)
        keydown("W")
        wait(3000)
        keyup("W")
        wait(500)
        keydown("D")
        wait(3600)
        keyup("D")
        wait(500)
        keydown("W")
        wait(2100)
        keyup("W")
        wait(500)
        press("Z")
        wait(500)
    # 柽木
    def athel(self):
        self.testsignal.emit("采集：柽木×12")
        self.home()
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("赤金的废墟")
        click(371, 837)
        wait(800)
        self.tp_point(0)
        keydown("A")
        wait(1300)
        keyup("A")
        wait(500)
        keydown("W")
        wait(6300)
        keyup("W")
        wait(500)
        press("Z")
        wait(500)
    # 梦见木
    def yumemiru(self):
        self.testsignal.emit("采集：梦见木×12")
        self.home()
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("砂流之庭")
        click(937, 617)
        wait(800)
        self.tp_point(0)
        keydown("S")
        wait(1300)
        keyup("S")
        wait(500)
        keydown("A")
        wait(400)
        keyup("A")
        wait(300)
        press("Z")
        wait(300)
        keydown("W")
        wait(500)
        keyup("W")
        wait(500)
        keydown("D")
        wait(2200)
        keyup("D")
        wait(500)
        keydown("W")
        wait(1000)
        keyup("W")
        wait(300)
        keydown("D")
        wait(800)
        keyup("D")
        wait(300)
        keydown("W")
        wait(500)
        keyup("W")
        wait(9000)
        press("Z")
        wait(500)
    # 刺葵木
    def mountain_date(self):
        self.home()
        self.testsignal.emit("采集：却砂木×12")
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("赤金的废墟")
        click(1872, 34)
        wait(800)
        drag((960, 967), (0, -200))
        wait(500)
        click(1125,984)
        wait(800)
        self.tp_point(0)
        keydown("D")
        wait(4500)
        keyup("D")
        wait(300)
        keydown("W")
        wait(3600)
        keyup("W")
        wait(300)
        press("Z")
        wait(500)
        # 第二段
        self.home()
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("熔铁的孤塞")
        click(1009,726)
        wait(800)
        self.tp_point(0)
        keydown("D")
        wait(6000)
        keyup("D")
        wait(300)
        keydown("W")
        wait(4000)
        keyup("W")
        wait(300)
        keydown("D")
        wait(5500)
        keyup("D")
        wait(300)
        keydown("W")
        wait(7900)
        keyup("W")
        wait(300)
        press("Z")
        wait(500)
    # 证悟木
    def adhigama(self):
        self.home()
        self.testsignal.emit("采集：证悟木×9")
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("缘觉塔")
        click(694,504)
        wait(800)
        self.tp_point(0)
        press("Z")
        wait(500)
    # 业果木_辉木
    def karmaphala_bright(self):
        self.home()
        self.testsignal.emit("采集：业果木×15,辉木×12")
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("缘觉塔")
        click(243,939)
        wait(800)
        self.tp_point(0)
        keydown("W")
        wait(8500)
        keyup("W")
        wait(300)
        press("Z")
        wait(300)
        keydown("S")
        wait(500)
        keyup("S")
        wait(300)
        keydown("D")
        wait(2500)
        keyup("D")
        wait(11500)
        press("Z")
        wait(500)
    # 却砂木
    def sandbearer(self):
        self.testsignal.emit("采集：却砂木×9")
        self.home()
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("华池岩岫")
        click(1080,332)
        wait(800)
        self.tp_point(0)
        keydown("A")
        wait(1500)
        keyup("A")
        wait(300)
        keydown("W")
        wait(4600)
        keyup("W")
        wait(300)
        keydown("A")
        wait(400)
        keyup("A")
        wait(300)
        press("Z")
        wait(500)

class Thread_genshin(QThread,Fly,Cut_tree):
    testsignal = pyqtSignal(str)
    accomplish = pyqtSignal(int)
    def __init__(self,tlist):
        super(Thread_genshin, self).__init__()
        self.tlist =tlist
        with open(r"resource\genshin\genshin_index.json", 'r', encoding='utf-8') as d:
            self.indexdir = json.load(d)
    def run(self):
        print(self.tlist)
        self.yuanshen_start()
        self.testsignal.emit("游戏已启动。")
        if self.tlist[0][1]:
            self.team()
            self.testsignal.emit("队伍切换完成。")
        if self.tlist[0][2]:
            self.tpkatheryne()
            self.dispatch()
            self.testsignal.emit("探索派遣检查完成。")
        if self.tlist[0][3]:
            self.use_transformer()
            self.testsignal.emit("参量质变仪检查完成。")
        if self.tlist[0][4]:
            self.catch_crystalfly()
            self.testsignal.emit("捕捉晶蝶完成。")
        if self.tlist[0][5]:
            self.tpfontaine1()
            self.make_condensed()
            self.testsignal.emit("合成浓缩树脂完成。")
        if self.tlist[0][6]:
            self.tpfontaine1()
            self.enter_rambler()
            self.tubby()
            self.testsignal.emit("领取尘歌壶完成。")
        if self.tlist[0][7]:
            self.cut_tree()
            self.testsignal.emit("伐木完成。")
        self.testsignal.emit("执行完成。")
        if self.tlist[-1][0]:
            self.testsignal.emit("尝试关闭游戏。")
            if killgame(self.tlist[1][0], "UnityWndClass", "原神"):self.testsignal.emit("游戏已关闭。")
            else:self.testsignal.emit("error：游戏关闭超时（20s）。")
        from subprocess import run
        if self.tlist[-1][2]:
            run("start "" resource\main_window\\batscr\sleep.bat", shell=True)
        if self.tlist[-1][1]:
            run("taskkill /f /t /im  SGA.exe", shell=True)
        self.accomplish.emit(1)
    # 启动并登录游戏
    def yuanshen_start(self):
        imi = imitate("UnityWndClass", "原神",8000,self.tlist[1][0])

        if imi.error_path_flag:
            self.testsignal.emit("error:游戏启动路径不是文件。")
        if imi.start_game_flag:
            self.testsignal.emit("游戏已启动。")
        if not imi.resolution_flag:
            self.testsignal.emit("error:不适配的游戏分辨率：%s×%s。"%(imi.wide, imi.high))
            self.testsignal.emit("请手动将游戏设置为横纵比16：9的全屏或者无边框窗口,并且纵分辨率大于等于720。")
        if not imi.start_game_flag or not imi.resolution_flag:
            self.accomplish.emit(3)
            wait(500)
        for fun in dir(imitate)[26:]:
            globals()[fun] = eval("imi." + fun)
        self.testsignal.emit("开始识别游戏状态。")
        serverflag = self.tlist[1][1]
        while 1:
            scpath = shotzone()
            if serverflag ==0:
                if findpic( r"resource\genshin\picture\login1.png",(900, 995, 1030, 1043),scpath)[1] >= 0.6:
                    serverflag =2
                    click(930, 630)
                    self.testsignal.emit("开门。")
                    wait(4000)
                    os.remove(scpath)
                    scpath = shotzone()
            elif serverflag==1:
                if findpic( r"resource\genshin\picture\login2.png",(863, 370, 1059, 467),scpath)[1] >= 0.6:
                    click(953,659)
                    self.testsignal.emit("登录B服账号。")
                    wait(4000)
                    os.remove(scpath)
                    scpath = shotzone()
                if findpic( r"resource\genshin\picture\login1.png",(900, 995, 1030, 1043),scpath)[1] >= 0.6:
                    serverflag = 2
                    click(930, 630)
                    self.testsignal.emit("开门。")
                    wait(4000)
                    os.remove(scpath)
                    scpath = shotzone()
            if findpic( r"resource\genshin\picture\sighin.png",(865, 240, 1060, 470),scpath)[1] >= 0.6:
                sighinflag = False
                click(930, 850)
                wait(800)
                click(930, 850)
                wait(100)
                click(930, 850)
                wait(1000)
                click(930, 850)
                wait(800)
                self.testsignal.emit("今日月卡领取成功。")
                os.remove(scpath)
                scpath = shotzone()
            if findpic( r"resource\genshin\picture\world.png",(57, 998, 179, 1075),scpath)[1] >= 0.6:
                self.testsignal.emit("加载到世界。")
                os.remove(scpath)
                break
            if findpic( r"resource\genshin\picture\home\home.png",(0, 0, 97, 88),scpath)[1] >= 0.6:
                self.testsignal.emit("加载到主界面。")
                os.remove(scpath)
                break
            os.remove(scpath)
            wait(2000)
    # 切换到标准队伍
    def team(self):
        self.home()
        self.testsignal.emit("开始确认队伍")
        self.opensub("队伍配置")
        wait(1000)
        for i in range(15):
            wait(1000)
            res = findpic( r"resource\genshin\picture\team.png",(37,980, 115,1058))
            if res[1] >= 0.6:
                self.testsignal.emit("进入到队伍配置界面。")
                break
            elif i == 14:
                self.testsignal.emit("error:加载队伍配置界面超时。\n")
                self.accomplish.emit(3)
        click(77,1016)
        wait(800)
        roll(580,224,55)
        wait(500)
        click(580,224)
        wait(500)
        click(328,1016)
        wait(800)
        click(1685,1018)
        wait(500)
        click(1843,47)
        self.world()
        press("1")
        wait(300)
        press("1")
        wait(300)
    # 每日派遣
    def tpfontaine1(self):
        self.home()
        self.testsignal.emit("前往枫丹：枫丹廷锚点1")
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("深潮的余响")
        click(1107, 786)
        wait(800)
        self.tp_point()
        self.testsignal.emit("到达枫丹：枫丹廷锚点1")
    def tpkatheryne(self):
        self.home()
        self.testsignal.emit("前往枫丹：枫丹廷锚点1")
        self.opensub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("深潮的余响")
        click(1107,786)
        wait(800)
        self.tp_point()
        self.testsignal.emit("前往枫丹凯瑟琳")
        keydown("W")
        wait(2700)
        keyup("W")
        wait(500)
        keydown("A")
        wait(1500)
        keyup("A")
        wait(500)
        self.testsignal.emit("前往枫丹凯瑟琳完成")
    def dispatch(self):
        self.testsignal.emit("开始检查派遣")
        press("F")
        wait(1000)
        click(960, 900)
        wait(1500)
        (x,y), val = findpic( r"resource\genshin\picture\dispatch\dispatch.png",(1247,311, 1337,909 ))
        if (x,y) ==(0,0):
            self.testsignal.emit("error:派遣未知错误")
            return False
        res,(cx,cy) = findcolor("32CCFF",(x+30,y-15,x+110,y+15))
        click(x+30,y)
        wait(2000)
        if res:
            self.testsignal.emit("存在可领取派遣")
            glist = self.indexdir["派遣区域坐标"]
            for g in range(len(glist)):#领取
                num = -1
                while num ==-1:
                    click(glist[g][0], glist[g][1])
                    wait(800)
                    pos, val = findpic( r"resource\genshin\picture\dispatch\get.png",(1490, 979, 1823, 1045))
                    if val>=0.6:
                        click(1692, 1024)
                        wait(1500)
                        click(1692, 1024)
                        wait(1500)
                    else:break
                    click(glist[g-1][0], glist[g-1][1])
                    wait(800)
            self.testsignal.emit("领取派遣完成")
        valt, num = 0, 0
        scpath = shotzone((1695, 12, 1755, 76))
        for i in range(6):
            val = findpic( r'resource\genshin\picture\number\%s.png' % (i),scpath=scpath)[1]
            if val > valt: valt, num = val, i
        os.remove(scpath)
        if num != 5:
            self.testsignal.emit("当前可派遣")
            ylist = [123, 228, 332 ,440,545]
            for num in range(5):#派遣
                r = self.indexdir["派遣区域"][self.tlist[2][num]]
                self.testsignal.emit("检查派遣："+r)
                [x,y] = self.indexdir["派遣区域坐标"][self.tlist[2][num]]
                click(x,y)
                wait(800)
                [x,y] = self.indexdir[r + "派遣材料坐标"][self.tlist[3][num]]
                click(x, y)
                wait(800)
                cname = r+"-"+self.indexdir[r + "派遣材料"][self.tlist[3][num]]
                scpath = shotzone((1490,979, 1823,1050))
                if findpic(r"resource\genshin\picture\dispatch\recall.png",scpath = scpath)[1] >=0.6:
                    self.testsignal.emit("执行中："+cname)
                    os.remove(scpath)
                elif findpic( r"resource\genshin\picture\dispatch\max.png",scpath = scpath)[1] >=0.6:
                    self.testsignal.emit("已达派遣上限")
                    os.remove(scpath)
                    break
                else:
                    res1 = findpic( r"resource\genshin\picture\dispatch\choose.png",scpath = scpath)[1]
                    res2 = findpic( r"resource\genshin\picture\dispatch\get.png",scpath = scpath,deleteflag=True)[1]
                    if res2>=0.7:
                        click(1692, 1024)
                        wait(1500)
                        click(1692, 1024)
                        wait(1500)
                    if res1>=0.7 or res2>=0.7:
                        self.testsignal.emit("可以开始派遣："+cname)
                        click(1793, 683)
                        wait(500)
                        click(1692, 1024)
                        wait(1000)
                        alist,blist,clist = [],[],[]
                        for y in ylist:
                            scpath = shotzone((154,y,430,y+82))
                            if findpic(r"resource\genshin\picture\dispatch\exploring.png",scpath=scpath)[1]>=0.75:
                                os.remove(scpath)
                                pass
                            else:
                                res1 = findpic(r"resource\genshin\picture\dispatch\20h.png",scpath=scpath)[1]
                                res2 = findpic(r"resource\genshin\picture\dispatch\25percent.png",scpath=scpath)[1]
                                res3 = findpic(r"resource\genshin\picture\dispatch\no_promote.png",scpath = scpath,deleteflag=True)[1]
                                if res1 or res2 or res3:
                                    if res1>res2 and res1>res3:alist += [y]
                                    elif res2>res3:blist += [y]
                                    else:clist += [y]
                                else:self.testsignal.emit("派遣选人识别出错。")
                        if alist :cy = alist[0]
                        else:
                            if blist: cy = blist[0]
                            else:cy = clist[0]
                        click(269, cy+40)
                        self.testsignal.emit("开始派遣："+cname)
                        wait(800)
                    else:
                        self.testsignal.emit("error:派遣执行未知错误。")
                        return False
        # 关闭派遣
        click(1853, 51)
        self.testsignal.emit("派遣结束")
        wait(3500)
        self.home()
    # 使用参量质变仪
    def use_transformer(self):
        self.home()
        self.testsignal.emit("检查参量质变仪")
        self.opensub("背包")
        click(1053, 48)
        wait(800)
        (x, y), val = findpic(r"resource\genshin\picture\lit_tools\para_trans.png", (109, 113, 1275, 459))
        if val >= 0.75:
            self.testsignal.emit("参量质变仪可用")
            click(x, y)
            wait(800)
            (x, y), val = findpic(r"resource\genshin\picture\lit_tools\para_retrieve.png", (1645, 971, 1769, 1058))
            if val >= 0.6:
                click(x, y)
                wait(1500)
            else:
                click(1840, 47)
                wait(1500)
            self.opensub("冒险之证")
            click(300, 440)
            wait(800)
            click(537, 296)
            wait(800)
            self.tp_domain("堇色之庭")
            click(1669, 1009)
            self.world()
            keydown("A")
            wait(2100)
            keyup("A")
            wait(500)
            keydown("W")
            wait(2100)
            keyup("W")
            wait(500)
            self.home()
            self.opensub("背包")
            click(1053, 48)
            wait(800)
            (x, y), val = findpic(r"resource\genshin\picture\lit_tools\para_trans.png", (109, 113, 1275, 459))
            click(x, y)
            wait(800)
            click(1694, 1022)
            wait(1500)
            click(1633, 549)
            wait(1000)
            press("F")
            wait(2000)
            for str in self.tlist[4]:
                if str == "":
                    self.testsignal.emit("未设置可用材料。")
                    break
                else:
                    c = os.path.splitext(str)[0]
                    c, b = os.path.split(c)
                    a = os.path.split(c)[1]
                    self.testsignal.emit("尝试添加材料：" + b)
                (x, y), val = findpic("resource\genshin\picture\\" + a + "\\" + a + ".png", (456, 0, 1450, 94))
                click(x, y)
                wait(800)
                (x, y), val = findpic(str, (104, 107, 1282, 955))
                click(x, y)
                wait(800)
                click(497, 1021)
                wait(800)
                res, (cx, cy) = findcolor("red", (1338, 979, 1516, 1056))
                print(res)
                if res:self.testsignal.emit("参量质变仪还未装满。")
                else:
                    click(1703, 1020)
                    wait(800)
                    click(1178, 757)
                    wait(1000)
                    self.testsignal.emit("参量质变仪已装满。")
                    break
            self.testsignal.emit("参量质变仪充能中。")
            i = 0
            while i >= 0:
                i += 1
                wait(2000)
                pos, val = findpic(r"resource\genshin\picture\acquire.png", (871, 242, 1050, 339))
                if val >= 0.6:
                    i = -1
                    click(961, 804)
                    self.testsignal.emit("参量质变仪使用成功。")
                    self.home()
                elif i == 15:
                    self.testsignal.emit("等待参量质变仪使用超时。\n")
                    self.accomplish.emit(3)
        else:
            self.testsignal.emit("参量质变仪（未找到/冷却中）")
            click(1840, 47)
            wait(1500)
    # 捉晶蝶执行判断
    def catch_crystalfly(self):
            self.testsignal.emit("开始捕捉晶蝶。")
            for num in range(len(self.tlist[5])):
                if self.tlist[5][num]:
                    self.testsignal.emit("开始点位" + str(num + 1))
                    eval("self.fly" + str(num + 1))()
                    self.testsignal.emit("结束点位" + str(num + 1))
    # 合成树脂
    def make_condensed(self):
        self.testsignal.emit("前往合成浓缩树脂")
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
        press("F")
        wait(1000)
        click(960, 950)
        wait(1500)
        (x, y), val = findpic(r"resource\genshin\picture\valu_tools\nssz.png", (57, 110, 627, 800))
        if val >= 0.6:
            click(x, y)
            wait(800)
            click(1298, 400)
            wait(800)
            valt, num = 0, 0
            scpath = shotzone((976, 866, 1043, 943))
            for i in range(6):
                val = findpic(r"resource\genshin\picture\number\%s.png" % (i), scpath=scpath)[1]
                if val > valt: valt, num = val, i
            os.remove(scpath)
            click(1618, 497)
            wait(800)
            if num != None:
                for i in range(5 - num):
                    click(1562, 674)
                    wait(400)
                click(1727, 1019)
                wait(800)
                click(1173, 786)
                wait(200)
                self.testsignal.emit("合成浓缩树脂成功")
            else:
                self.testsignal.emit("error:num is" + str(type[strn]) + "\n")
                self.accomplish.emit(3)
        else:
            self.testsignal.emit("无法合成浓缩树脂：缺少树脂或晶核")
        click(1836, 48)
        wait(2200)
    # 领取尘歌壶
    def enter_rambler(self):
        self.home()
        self.testsignal.emit("前往尘歌壶：默认尘歌壶-主建筑")
        self.opensub("背包")
        click(1053, 48)
        wait(800)
        (x,y),val=findpic(r"resource\genshin\picture\lit_tools\rambler.png",(109,113,1275,459))
        click(x,y)
        wait(800)
        click(1694, 1022)
        wait(800)
        press("esc")
        wait(1000)
        press("F")
        wait(3000)
        self.world()
        self.testsignal.emit("到达尘歌壶：默认尘歌壶-主建筑")
    def tubby(self):
        self.testsignal.emit("开始领取尘歌壶")
        keydown("S")
        wait(200)
        keyup("S")
        wait(500)
        keydown("D")
        wait(400)
        keyup("D")
        press("F")
        wait(2000)
        click(1300,431)
        wait(2000)
        click(1300,431)
        wait(2000)
        click(1076, 950)
        wait(800)
        click(1815,899)
        wait(800)
        click(1805, 704)
        wait(800)
        click(1815, 899)
        wait(800)
        click(1874, 48)
        wait(4000)
        click(1362,800)
        wait(1000)
        click(1362,800)
        self.home()
    # 伐木
    def cut_tree(self):
        self.testsignal.emit("检查采集木材。")
        runlist = []
        for u in range(1, 4):
            woodlist = self.indexdir["tree_kind%s" % (u)]
            for num in range(len(woodlist)):
                if self.tlist[6][u][num]: runlist += [woodlist[num]]
        if self.tlist[6][0] == "":cirnum = 0
        else:cirnum = int(self.tlist[6][0])
        if not (cirnum and len(runlist) >= 5):self.testsignal.emit("未设置有效伐木计划。请保证循环次数大于等于1，并且至少勾选5个伐木位点。")
        else:
            self.home()
            self.testsignal.emit("检查王树瑞佑。")
            self.opensub("背包")
            click(1053, 48)
            wait(800)
            (x, y), val = findpic( r"resource\genshin\picture\lit_tools\boon_elder_tree.png",(110, 112, 1273, 805))
            if val < 0.75:
                self.testsignal.emit("没有找到道具：王树瑞佑。采集木材中止。")
                self.testsignal.emit("采集木材中止。")
            else:
                click(x, y)
                wait(800)
                if findpic( r"resource\genshin\picture\lit_tools\unload.png",(1637, 972, 1765, 1068))[1] >= 0.75:
                    self.testsignal.emit("王树瑞佑已装备。")
                    click(1840, 47)
                    wait(1500)
                else:
                    self.testsignal.emit("装备王树瑞佑。")
                    click(1694, 1013)
                    wait(1500)
                treeliste = self.indexdir["tree_kind1"]+self.indexdir["tree_kind2"]+self.indexdir["tree_kind3"]
                treelistc = self.indexdir["木材种类1"]+self.indexdir["木材种类2"]+self.indexdir["木材种类3"]
                ctstr = ""
                for wood in runlist:
                    ctstr+=treelistc[treeliste.index(wood)]+" "
                print(ctstr)
                self.testsignal.emit("采集木材计划开始：\n"+
                                     "点位%s个：%s\n"%(len(runlist),ctstr)+
                                     "循环次数：%s" % (cirnum))
                for i in range(cirnum):
                    for wood in runlist:
                        eval("self." + wood)()

    # 打开主界面
    def home(self):
        m = 0
        while m >= 0:
            m += 1
            wait(1500)
            (x, y), val = findpic(r"resource\genshin\picture\home\home.png", (0, 0, 97, 88))
            if val >= 0.6:
                m = -1
            else:
                press("esc")
            if m == 15:
                self.testsignal.emit("error:打开主界面超时。\n")
                self.accomplish.emit(3)
    def world(self):
        i=1
        while i >0 :
            i+=1
            wait(1000)
            pos,val = findpic( r"resource\genshin\picture\world.png",(57, 998, 179, 1075))
            if val >=0.6:
                i=0
                self.testsignal.emit("加载到世界。")
            elif i == 15:
                self.testsignal.emit("error:加载世界超时。\n")
                self.accomplish.emit(3)

    # 从主界面打开子界面
    def opensub(self, cho):
        dir = {"地图": (358, 697), "背包": (663, 556), "冒险之证": (659, 698), "队伍配置": (352, 416)}
        x, y = dir[cho]
        click(x, y)
        self.testsignal.emit("打开" + cho)
        wait(2000)
    # 从秘境传送
    def tp_domain(self,str):
        tdir = {"塞西莉亚苗圃":"cecilia_garden","赤金的废墟":"city_of_gold","沉眠之庭":"slumbering_court",
                "岩中幽谷":"the_lost_valley","堇色之庭":"violet_court","深潮的余响":"deep_tides","罪祸的终末":"denouement",
                "苍白的遗荣":"pale_glory","缘觉塔":"enlightenment","砂流之庭":"flow_sand","华池岩岫":"pool_cavern",
                "熔铁的孤塞":"fortress"}
        self.testsignal.emit("尝试传送到秘境："+str)
        for num in range(15):
            wait(200)
            (x, y), val = findpic( r"resource\genshin\picture\domain\\"+tdir[str]+".png",(738, 249, 1033, 886))
            if val >=0.8:
                click(1555, y)
                wait(2000)
                break
            elif num <= 13:
                roll(1116, 296, -24)
            else:
                self.testsignal.emit("error:未识别到秘境-"+str+"\n")
                self.accomplish.emit(3)
    # 选择确认传送锚点图标并开始传送，最后判断传送成功
    def tp_point(self,num=0):
        (x, y), val = findpic( "resource\genshin\picture\maps\\tp_point%s.png"%(num),(1245, 621, 1528, 1023))
        if val >= 0.75:
            click(x, y)
            wait(800)
        click(1634, 1003)
        wait(3000)
        self.world()
if __name__ == '__main__':pass