# -*- coding:gbk -*-
import os,traceback

from function import *
from PyQt5.QtCore import  QThread,pyqtSignal
import sys,json,shutil
# pyinstaller -D -w D:\Kin-project\python\venv\hxls\hxls.py
class Thread_hxls(QThread):
    testsignal = pyqtSignal(str)
    accomplish = pyqtSignal(int)
    def __init__(self,tlist):
        super(Thread_hxls, self).__init__()
        self.tlist =tlist
        with open(r"resource\hxls\hxls_index.json", 'r', encoding='utf-8') as d:
            self.indexdir = json.load(d)
    def run(self):
        print(self.tlist)
        self.hxls_start()
        self.testsignal.emit("(自动触发驾驶舱舍友互动)")
        click(769,590)
        wait(300)
        if self.tlist[0][1]:
            self.fight()
            self.testsignal.emit("检查完成：作战。")
        if self.tlist[0][2]:
            self.dispatch()
            self.testsignal.emit("检查完成：线下采购。")
        if self.tlist[0][3]:
            self.review()
            self.testsignal.emit("检查完成：战术回顾。")
        if self.tlist[0][4]:
            self.getmarket()
            self.testsignal.emit("检查完成：集市领取。")
        if self.tlist[0][5]:
            self.recruit()
            self.testsignal.emit("检查完成：舍友访募。")
        if self.tlist[0][6]:
            self.reward()
            self.testsignal.emit("检查完成：今日工作。")
        if self.tlist[0][7]:
            self.market_network()
            self.testsignal.emit("检查完成：卡门商网。")
        if self.tlist[0][8]:
            self.random_gift()
            self.testsignal.emit("检查完成：随机礼包。")
        self.testsignal.emit("执行完成。")
        # 结束后操作
        if self.tlist[-1][0]:
            self.testsignal.emit("尝试关闭游戏。")
            if killgame(self.tlist[1][0], "UnityWndClass", "环行旅舍"):self.testsignal.emit("游戏已关闭。")
            else:self.testsignal.emit("error：游戏关闭超时（20s）。")
        from subprocess import run
        if self.tlist[-1][2]:
            run("start "" resource\main_window\\batscr\sleep.bat", shell=True)
            # os.system("start "" resource\main_window\\batscr\sleep.bat")
        if self.tlist[-1][1]:
            run("taskkill /f /t /im  SGA.exe", shell=True)
            # os.system("taskkill /f /t /im  SGA.exe")
        self.accomplish.emit(1)

    def hxls_start(self):
        imi = imitate("UnityWndClass", "环行旅舍",path = self.tlist[1][0])
        if imi.error_path_flag:
            self.testsignal.emit("error:游戏启动路径不是文件。")
        if imi.start_game_flag:
            self.testsignal.emit("游戏已启动。")
        if not imi.resolution_flag:
            self.testsignal.emit("error:不适配的游戏分辨率：%s×%s。" % (imi.wide, imi.high))
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
            if serverflag==0:
                if findpic(r"resource\hxls\picture\startgame1.png",(871, 612, 1052, 654),scpath)[1] >= 0.6:
                    wait(300)
                    click(930, 630)
                    self.testsignal.emit("登录游戏。")
                    wait(5000)
                    os.remove(scpath)
                    scpath = shotzone()
            elif serverflag==1:
                if findpic( r"resource\hxls\picture\startgame2.png",(830, 595, 1093, 682),scpath)[1] >= 0.6:
                    wait(300)
                    click(960,633)
                    self.testsignal.emit("登录账号。")
                    wait(1500)
                    os.remove(scpath)
                    scpath = shotzone()
                if findcolor( "blue",(910, 658, 992, 704))[0]:
                    wait(300)
                    click(958,679)
                    self.testsignal.emit("登录游戏。")
                    wait(5000)
                    os.remove(scpath)
                    scpath = shotzone()
            if findpic( r"resource\hxls\picture\sighin.png",(887, 240, 1032, 280),scpath)[1] >= 0.6: # 签到奖励
                click(970, 930)
                wait(1500)
                click(1789, 120)
                self.testsignal.emit("签到成功。")
                wait(1000)
                os.remove(scpath)
                scpath = shotzone()
            (x, y), sim = findpic(r"resource\hxls\picture\close\close2.png",scpath=scpath)
            if sim >= 0.6:
                click(x, y)
                wait(1500)
                os.remove(scpath)
                scpath = shotzone()
            if findpic( r"resource\hxls\picture\home.png",(1739, 37, 1814, 98),scpath)[1] >= 0.7:# 主界面
                wait(1500)
                os.remove(scpath)
                scpath = shotzone()
                if findpic(r"resource\hxls\picture\home.png", (1739, 37, 1814, 98), scpath)[1] >= 0.7:
                    self.testsignal.emit("加载到主界面。")
                    os.remove(scpath)
                    break
            os.remove(scpath)
            wait(1500)

    def fight(self):
        self.testsignal.emit("开始检查：作战。")
        val = findpic( r"resource\hxls\picture\fight\fighting.png",(1652, 306, 1788, 393))[1]
        if val>=0.6:
            self.testsignal.emit("重游进行中，不能再次开启作战。")
        elif not findcolor( "2000FF",(1784, 382, 1825, 429))[0]:
            self.testsignal.emit("作战空闲中。")
            if self.tlist[2][0]:self.testsignal.emit("没有再次重游目标。")
        else:
            click(1739, 420)
            self.testsignal.emit("重游完成，领取重游奖励。")
            wait(1500)
            while 1:
                scpath = shotzone()
                if findpic( r"resource\hxls\picture\lvup.png",(827, 134, 1088, 262),scpath)[1] >= 0.6:
                    self.testsignal.emit("等级提升！")
                    click(1282, 690)
                    os.remove(scpath)
                    scpath = shotzone()
                if findpic( r"resource\hxls\picture\fight\retour.png",(1670, 50, 1820, 110),scpath)[1] >= 0.6:
                    wait(500)
                    if findpic( r"resource\hxls\picture\fight\retour.png",(1670, 50, 1820, 110))[1] >= 0.6:
                        os.remove(scpath)
                        if self.tlist[2][0]:
                            self.testsignal.emit("尝试重复上次作战。")
                            click(1744, 80)
                            wait(1800)
                            scpath = shotzone()
                            ((x1, y1), sim1) = findpic( r"resource\hxls\picture\fight\add.png",(1100, 335, 1900, 983),scpath =scpath)
                            ((x2, y2), sim2) = findpic(r"resource\hxls\picture\fight\start.png", (960, 540, 1920, 1080),scpath=scpath,deleteflag=True)
                            if sim1 >= 0.6 and sim2 >= 0.6:
                                click(x1 + 120, y1)
                                wait(1000)
                                click(x2, y2)
                                wait(1000)
                                if findpic( r"resource\hxls\picture\fight\lack.png",(1085, 716,1256, 846))[1]>0.75:
                                    self.testsignal.emit("能源不足。")
                                    click(761,781)
                                    wait(1000)
                                else:
                                    self.testsignal.emit("开始重复上次作战。")
                                click(288, 78)
                                wait(1500)
                            else:
                                self.testsignal.emit("(不能识别的界面)")
                                click(288, 78)
                                wait(1500)
                        else:
                            click(971, 930)
                            wait(800)
                        break
                    else:pass
                os.remove(scpath)
                wait(1000)
        if (not self.tlist[2][0]) and (val==0):
            click(1446,359)
            wait(1500)
            click(964,1029)
            wait(1500)
            num = self.tlist[2][1]
            x,y = [(519,545),(885,554),(1248,534)][num]
            click(x,y)
            wait(2000)
            click(786, 555)
            wait(1500)
            click(1077,856)
            wait(1000)
            click(1525,549)
            wait(500)
            click(1458,816)
            wait(1000)
            if findpic( r"resource\hxls\picture\fight\lack.png",(1085, 716, 1256, 846))[1] >= 0.75:
                self.testsignal.emit("能源不足。")
                click(761, 781)
                wait(1000)
            else:
                self.testsignal.emit("开始作战：获取 "+["格","风物志","节"][num])
            click(288, 78)
            wait(1500)


    def dispatch(self):#
        self.testsignal.emit("开始检查：线下采购。")
        click(146,720)
        wait(1000)
        click(1563, 141)
        wait(1000)
        dlist = []
        for n in range(6):
            y1, y2 = self.indexdir["线下采购区域"][n]
            zoom = (1068, y1, 1263, y2)
            x, y = self.indexdir["线下采购坐标"][n]
            click(x, y)
            wait(400)
            if findpic( r"resource\hxls\picture\dispatch\condition2.png",zoom)[1] >= 0.6:  # 完成派遣
                click(1708, 977)
                wait(1200)
                if self.tlist[3][6]:click(1208,845)
                else:
                    dlist += [n]
                    click(878,851)
                self.testsignal.emit("线下采购" + str(n + 1) + "：完成，已领取。")
                wait(1200)
            elif findpic( r"resource\hxls\picture\dispatch\condition1.png",(1632, 927,1796, 1013))[1]>=0.6:
                self.testsignal.emit("线下采购" + str(n + 1) + "：进行中。")
            elif findpic( r"resource\hxls\picture\dispatch\condition0.png",zoom)[1]>=0.6:#派遣
                dlist += [n]
                self.testsignal.emit("线下采购" + str(n + 1) + "：待派遣。")
        for n in dlist:
            self.testsignal.emit("线下采购" + str(n + 1) + "：尝试开始派遣。")
            y1,y2 = self.indexdir["线下采购区域"][n]
            zoom = (1068, y1, 1263, y2)
            x,y = self.indexdir["线下采购坐标"][n]
            click(x,y)
            wait(500)
            click(1562, 939)
            wait(800)
            mnum,fnum,pnum = self.tlist[3][n]
            tpath = "resource\hxls\picture\dispatch\zone"+str(mnum)+".png"
            (x,y), sim = findpic( tpath,(666, 420, 1860, 484))
            if sim ==0:
                drag((1128,451),(-200,0))
                wait(800)
                (x,y), sim = findpic( tpath,(666, 420, 1860, 484))
            click(x,y)
            wait(500)
            x, y = [(951, 667), (961, 749), (960, 838)][fnum]
            click(x, y)
            wait(500)
            click(1571, 883)
            wait(1000)
            (x, y), sim = findpic( r"resource\hxls\picture\dispatch\plan"+str(pnum)+".png",(194, 145, 454, 585))
            if sim >=0.85:
                click(x, y)
                wait(500)
                self.testsignal.emit("线下采购开始："+self.indexdir["线下采购材料"][mnum]+
                                     "-"+self.indexdir["携带资金"][fnum]+
                                     "-"+self.indexdir["采购方案"][pnum])
            else:
                self.testsignal.emit("采购方案未找到目标，已自动选择一号位。")
                self.testsignal.emit("线下采购开始：" + self.indexdir["线下采购材料"][mnum] +
                                     "-" + self.indexdir["携带资金"][fnum])
                click(143,151)
                wait(500)
            click(397, 1008)
            wait(1500)
        # 结束
        click(296, 75)
        wait(1000)

    def review(self):
        self.testsignal.emit("开始检查：战术回顾。")
        if findcolor( "red",(1631,876,1708,958))[0]:
            self.testsignal.emit("存在战术回顾已完成。")
            click(1628, 946)
            wait(1000)
            click(258, 386)
            wait(1000)
            # 战术支援
            self.testsignal.emit("开始战术支援。")
            list = [(613, 795),(779, 799),(954, 803),(1132, 795),(1295, 799),(1502, 798),(1666, 798)]
            for num in range(3):
                for (x,y) in list:
                    click(x,y)
                    wait(300)
                if num < 2:
                    click(1646, 347)
                    wait(500)
                if num < 1:wait(8500)
            self.testsignal.emit("战术支援完成。")
            # 战术回顾
            self.testsignal.emit("开始检查战术回顾。")
            click(293, 277)
            wait(500)
            list = [(575, 820, 825, 868,1),(1003, 821, 1252, 867,2),(1430, 822, 1680, 867,3)]
            for (x1,y1,x2,y2,n) in list:
                (x,y),val = findpic( r"resource\hxls\picture\review\reviewed.png",(x1,y1,x2,y2))
                if val >= 0.6:#完成回顾
                    self.testsignal.emit("战术回顾%s：已完成。"%(n))
                    click(x,y)
                    wait(1000)
                    click(1648, 858)
                    wait(1000)
                    click(1060, 868)
                    wait(1500)
                else:
                    (x,y),val = findpic( r"resource\hxls\picture\review\toreview.png",(x1,y1,x2,y2))
                    if val >= 0.6:#开始回顾
                        self.testsignal.emit("战术回顾%s：空闲。"%(n))
                    else:
                        self.testsignal.emit("战术回顾%s：进行中。" % (n))
                if val >= 0.6:
                    self.testsignal.emit("尝试创建战术回顾。")
                    click(x,y)
                    wait(1000)
                    click(734, 846)
                    wait(500)
                    if self.tlist[4] !="0%":
                        for cycle in range(35):
                            rvpath = "resource\hxls\picture\\review\su"+self.indexdir["战术回顾选择"][self.tlist[4]][:-1]+".png"
                            (x,y),val = findpic( rvpath,(698, 131, 756, 934))
                            if val >= 0.85:
                                click(x,y)
                                wait(500)
                                break
                            else:
                                roll(476, 833,-19)
                                wait(800)
                    click(524, 1007)
                    wait(1000)
                    click(1652, 875)
                    self.testsignal.emit("战术回顾开始。")
                    wait(1500)
            # 结束
            click(296, 75)
            wait(1000)
        else:
            self.testsignal.emit("暂无战术回顾完成。")
            wait(500)

    def getmarket(self):
        self.testsignal.emit("开始检查：集市领取。")
        if not findcolor( "red",(304, 254, 377, 324))[0]:
            self.testsignal.emit("集市暂无可领取。")
        else:
            click(283,331)
            wait(1000)
            if findcolor("red",(64, 308, 351, 384))[0]:
                click(198,350)
                wait(500)
                if findpic( r"resource\hxls\picture\market\daily.png",(399, 123, 768, 455))[1]>=0.6:
                    click(590,285)
                    wait(1200)
                    click(1257,723)
                    wait(1200)
                    self.testsignal.emit("领取每日配给完成。")
                    click(1054,837)
                    wait(1200)
                else:self.testsignal.emit("暂无每日配给可领取。")
            else:
                self.testsignal.emit("暂无每日配给可领取。")
            if findcolor( "red",(63, 468, 344, 546))[0]:
                click(203,508)
                wait(1000)
                click(1487,79)
                wait(2000)
                self.testsignal.emit("领取援外协议完成。")
                click(1010, 712)
                wait(2000)
            else:
                self.testsignal.emit("暂无援外协议可领取。")
            click(299, 77)
            wait(1000)

    def recruit(self):
        self.testsignal.emit("开始检查:舍友访募。")
        click(1469,697)
        wait(2000)
        tzone = [(171, 234,379, 338),(174, 346,378, 445),(172, 455,377, 556)]
        tclick = [(129,290 ),(126,395),(131,501)]
        vflag,cflag = True,self.tlist[5][0]
        for n in range(3):
            lzone = tzone[n]
            x, y = tclick[n]
            if findpic( r"resource\hxls\picture\recruit\accomplish.png",lzone)[1] >= 0.6:
                self.testsignal.emit("访募%s：完成。尝试领取。"%(n+1))
                self.receive_recruit(x, y)
            while 1:
                if findpic( r"resource\hxls\picture\recruit\new.png",lzone)[1] >= 0.6:
                    self.testsignal.emit("访募%s：空闲。尝试开始访募。"%(n+1))
                    click(x, y)
                    wait(1000)
                    if findcolor( "2F2C30",(480, 253,499, 273))[0]:
                        self.testsignal.emit("普通访募。")
                        vflag = self.create_recruit()
                        if (not cflag) or (not vflag):break
                        else:
                            self.testsignal.emit("尝试使用高速显影剂。")
                            click(743, 811)
                            wait(1000)
                            if findpic( r"resource\hxls\picture\recruit\lack.png",(903, 70, 1021, 141))[1]>=0.6:
                                self.testsignal.emit("缺少高速显影剂。")
                                cflag = False
                            else:
                                self.testsignal.emit("高速显影剂使用成功。")
                                self.receive_recruit(x, y)
                    else:
                        if findcolor( "purple",(480, 253,499, 273))[0]:
                            self.testsignal.emit("发现必出SR访募。")
                        elif findcolor( "orange+yellow",(480, 253,499, 273))[0]:
                            self.testsignal.emit("发现必出SSR访募！")
                        break
                else:
                    self.testsignal.emit("访募%s：进行中。"%(n+1))
                    break
            if not vflag: break
        click(296, 75)
        wait(1000)
    def create_recruit(self):
        for i in range(self.tlist[5][1]):
            click(990, 626)
            wait(100)
        click(871, 818)
        wait(800)
        if findpic( r"resource\hxls\picture\recruit\lack.png",(903, 70, 1021, 141))[1]>=0.6:
            self.testsignal.emit("缺少格或外显记录。")
            return False
        else:
            self.testsignal.emit("舍友访募开始。")
            return True
    def receive_recruit(self,x,y):
        try:
            click(x, y)
            wait(2500)
            scpath = shotzone()
            Nval = findpic( r"resource\hxls\picture\recruit\N.png",(252, 444, 421, 553),scpath)[1]
            Rval = findpic( r"resource\hxls\picture\recruit\R.png",(252, 444, 421, 553),scpath)[1]
            SRval = findpic( r"resource\hxls\picture\recruit\SR.png",(252, 444, 421, 553),scpath)[1]
            SRRval = findpic( r"resource\hxls\picture\recruit\SSR.png",(252, 444, 421, 553),scpath)[1]
            vallist = (Nval,Rval,SRval,SRRval)
            maxval = max(vallist)
            if maxval:
                maxindex = vallist.index(maxval)
                if maxindex==0:self.testsignal.emit("访募到N卡。")
                elif maxindex == 1:self.testsignal.emit("访募到R卡。")
                else:
                    nowtime = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
                    shutil.copyfile(scpath, r"resource\hxls\screenshot\%s.png" % (nowtime))
                    if maxindex==2:self.testsignal.emit("访募到SR卡,可在文件夹“resource\hxls\screenshot”中查看。")
                    else:self.testsignal.emit("访募到SSR卡！可在文件夹“resource\hxls\screenshot”中查看。")
            else:
                nowtime = time.strftime("%Y-%m-%d %H：%M：%S", time.localtime())
                shutil.copyfile(scpath, r"resource\hxls\screenshot\%s.png" % (nowtime))
                self.testsignal.emit("error:舍友访募未知错误。(" + nowtime + ".png)")
                self.accomplish.emit(3)
            os.remove(scpath)
            click(273, 903)
            wait(1500)
            click(273, 903)
            wait(1500)
        except (Exception, BaseException) as e:
            exstr = traceback.format_exc()
            self.testsignal.emit(exstr)
    def reward(self):
        self.testsignal.emit("开始检查：今日工作。")
        if not findcolor( "red",(172, 415,238, 470))[0]:
            self.testsignal.emit("暂无任务奖励。")
            wait(500)
        else:
            click(145,430)
            wait(1500)
            if findcolor( "red",(753,146,790,189))[0]:
                click(727, 183)
                wait(1000)
                click(1340, 1009)
                wait(2000)
                click(941, 827)
                wait(2000)
                self.testsignal.emit("领取任务奖励完成。")
            else:self.testsignal.emit("暂无任务奖励。")
            click(296, 75)
            wait(1000)
    def market_network(self):
        self.testsignal.emit("开始检查：卡门商网。")
        click(419,162)
        wait(1500)
        click(1690,220)
        wait(800)
        scpath = shotzone()
        val1 = findpic(r"resource\hxls\picture\market_network\unlock.png", (1504, 862, 1851, 979), scpath)[1]
        val2 = findpic(r"resource\hxls\picture\market_network\receive.png", (1504, 862, 1851, 979), scpath)[1]
        os.remove(scpath)
        if val2>val1 and val2>=0.7:
            click(1670,917 )
            self.testsignal.emit("已领取通讯波频。")
            wait(800)
        else:
            self.testsignal.emit("暂无可领取通讯波频。")
        click(301,81 )
        wait(1000)
    def random_gift(self):
        self.testsignal.emit("开始检查：随机包。")
        click(150,623)
        wait(2000)
        click(720,301)
        wait(800)
        gdirpath = r"resource\hxls\picture\random_gift"
        dirlist =os.listdir(gdirpath)
        uglist =[]
        for g in dirlist:
            gname = self.indexdir[os.path.splitext(g)[0]]
            gpath = gdirpath+"\\"+g
            num = 0
            self.testsignal.emit("检查随机包：" + gname)
            while 1:
                (x,y),val = findpic( gpath,(820,111, 1840,501))
                if val >= 0.75:
                    num += 1
                    click(x, y)
                    wait(1000)
                    click(956, 867)
                    self.testsignal.emit("已使用%s个。"%(num))
                    wait(1000)
                    click(956, 867)
                    wait(800)
                else:
                    self.testsignal.emit("使用完毕。")
                    break
            if num:
                uglist += ["%s:%s个。"%(gname,num)]
            else:self.testsignal.emit("暂无该随机包。")
        if uglist:
            self.testsignal.emit("使用随机包统计：")
            for i in uglist:
                self.testsignal.emit(i)
        click(296, 75)
        wait(1000)
    def getmail(self):
        self.testsignal.emit("开始检查：邮件。")
        res,(cx,cy) = findcolor("red",(472, 26, 521, 80))
        if res:
            wait(500)
            click(472, 78)
            wait(1500)
            click(577, 809)
            wait(2000)
            click(1006, 885)
            wait(2000)
            click(1791, 122)
            self.testsignal.emit("领取邮件完成。")
            wait(2000)
        else:
            self.testsignal.emit("暂无新邮件。")
            wait(500)
if __name__ == '__main__':pass






