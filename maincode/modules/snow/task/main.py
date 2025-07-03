from maincode.tools.myclass import SGAStop
from maincode.tools.main import GetWindow, GetTracebackInfo, logger
from time import sleep
from win32gui import FindWindow
from os import path
from .energy import snowEnergy
from .dailytask import snowDailyTask
from .other import snowOther
from .gacharecog import snowGachaRecog
from ..emulator.main import emulatorstart


def CloseSnow(self):
    for _ in range(20):
        win = GetWindow("尘白禁区")
        if win is None:
            self.send(f"尘白禁区已关闭")
            self.para["startwait"] = True
            return True
        else:
            win.close()
        sleep(0.5)
    self.send(f"尘白禁区关闭超时")
    return False


def SnowHome(self):
    num = 30
    flag = False
    while num > 0:
        sc = self.ctler.screenshot()
        if "任务" in self.ctler.ocr((1458, 330, 1529, 379), sc)[0]:
            if flag:
                return True
            else:
                flag = True
        elif "退出" in self.ctler.ocr((1617, 23, 1701, 70), sc)[0]:
            self.ctler.clickChange(target="退出", zone=(1617, 23, 1701, 70))
            self.ctler.waitTo("任务", (1458, 330, 1529, 379), (0.4, 30))
            return True
        else:
            flag = False
            num -= 1
            self.ctler.press("esc")
        self.ctler.wait(0.8)
    raise TimeoutError("尘白禁区返回主页超时")


def taskstart(self):
    if self.para["OtherConfig"]["Snow"]["Server"] == 3:
        emulatorstart(self)
        return
    self.SnowHome = SnowHome
    # print(self.para)
    self.send("开始任务:尘白禁区", True)
    num = 3
    while num > 0:
        try:
            # print("startwait", self.para.get("startwait", True))
            if self.para.get("startwait", True):
                SnowLaunch(self)
                LogSnow(self, 180)
                num = 3
                self.ctler.click((829, 585))
                self.ctler.wait(0.3)
                self.ctler.click((829, 585))
                self.ctler.wait(0.3)
                self.para["startwait"] = False
            if self.para["Energy"]:
                snowEnergy(self)
                num = 3
                self.para["Energy"] = False
            if self.para["DailyTask"]:
                snowDailyTask(self)
                num = 3
                self.para["DailyTask"] = False
            if self.para["Other"]:
                snowOther(self)
                num = 3
                self.para["Other"] = False
            if self.para["GachaRecog"]:
                snowGachaRecog(self)
                self.para["GachaRecog"] = False
        except SGAStop:
            raise SGAStop
        except RuntimeError as e:
            _str = GetTracebackInfo(e)
            logger.error(_str + "任务执行异常:尘白禁区")
            CloseSnow(self)
            raise RuntimeError("任务执行异常:尘白禁区")
        except Exception as e:
            num -= 1
            _str = GetTracebackInfo(e)
            self.send(f"任务执行异常:尘白禁区")
            logger.error(_str + "任务执行异常:尘白禁区")
            if num > 0:
                self.send(f"进行重试,等待中...")
                if self.para.get("startwait", True):
                    CloseSnow(self)
                    self.ctler.wait(4)
                else:
                    self.ctler.wait(2)
                    SnowHome(self)
                    self.ctler.wait(2)
            else:
                CloseSnow(self)
                self.send(f"尘白禁区:执行异常,跳过流程")
                raise RuntimeError("尘白禁区:执行异常,跳过流程")
        else:
            self.send(f"尘白禁区:执行完成")
            if self.para["SoftClose"]:
                # print("SoftClose", self.para["SoftClose"])
                self.send("尝试关闭游戏")
                CloseSnow(self)
            break


def SnowLaunch(self):
    # 路径修正
    glist = [["UnrealWindow", "尘白禁区"],
             ["UnrealWindow", "Snowbreak: Containment Zone"]]
    h1 = FindWindow("UnrealWindow", "尘白禁区")
    h2 = FindWindow("UnrealWindow", "Snowbreak: Containment Zone")
    if h1 or h2:
        hwnd = [item for item in [h1, h2] if item][0]
        self.ctler.ChooseWindow(hwnd, (1920, 1080))
        return
    _dict = self.para["OtherConfig"]["Snow"]
    _path = _dict["Path"]
    _server = _dict["Server"]
    if _server != 2:
        h1 = FindWindow("wailsWindow", "尘白禁区启动器")
        h2 = FindWindow("Qt5159QWindowIcon", "西山居启动器-尘白禁区")
        if not (h1 or h2):
            assert isinstance(_path, str)
            assert path.isfile(_path)
            assert path.split(_path)[1] in ["snow_launcher.exe", "SeasunGame.exe"]
            _list = [["wailsWindow", "尘白禁区启动器"],
                     ["Qt5159QWindowIcon", "西山居启动器-尘白禁区"]]
            # print(_path)
            hwnd = self.ctler.RunProg(f"start \"\" \"{_path}\"", _list, 2)
            assert hwnd
        else:
            hwnd = [item for item in [h1, h2] if item][0]
        self.ctler.ChooseWindow(hwnd, (1280, 748))
        LauchPrepare(self)
    else:
        _path = "start steam://rungameid/2668080"
        hwnd = self.ctler.RunProg(_path, glist, 5)
        assert hwnd
        self.ctler.ChooseWindow(hwnd, (1920, 1080))


def LauchPrepare(self):
    _path = self.para["OtherConfig"]["Snow"]["Path"]
    _name = path.split(_path)[1]
    if self.para["PreLoad"] and _name == "snow_launcher.exe":
        _pos = self.ctler.findtext("下", (781, 585, 950, 734))
        if _pos:
            self.ctler.clickChange(zone=(559, 317, 713, 391), pos=_pos)
            self.ctler.wait(0.5)
            self.ctler.clickChange("确定")
            self.send("开始预下载")
            self.ctler.wait(0.5)
        else:
            self.send("暂无预下载")
    if _name == "snow_launcher.exe":
        self.ctler.ChangeReference((1280, 748))
        error = 0
        num = 120
        while num > 0:
            if hwnd := FindWindow("UnrealWindow", "尘白禁区"):
                self.ctler.ChooseWindow(hwnd, (1920, 1080))
                return True
            if self.ctler.findtext("关闭", (398, 219, 893, 540)):
                if pos := self.ctler.findtext("确定", (398, 219, 893, 540)):
                    self.ctler.clickChange(pos, zone=(398, 219, 893, 540))
                    return False
            _value = self.ctler.ocr((1004, 646, 1151, 701))[0]
            # print("_value:", _value, self.ctler.RefRes, self.ctler.Operate.zone)
            if "开始游戏" in _value:
                self.ctler.clickChange((1073, 673), zone=(1004, 646, 1151, 701))
                self.ctler.wait(5)
                continue
            elif "获取更新" in _value:
                if self.para["Update"]:
                    self.ctler.clickChange((1073, 673), zone=(718, 476, 821, 536))
                    self.ctler.clickChange((750, 499), zone=(718, 476, 821, 536))
                    error = 0
                else:
                    self.send("尘白禁区:需要更新,当前未勾选自动更新,终止任务")
                    raise RuntimeError("尘白禁区:需要更新,当前未勾选自动更新,终止任务")
            elif "检查更新" in _value:
                num = 120
                self.ctler.wait(2)
            elif "更新中" in _value:
                self.ctler.clickTo("开始游戏", zone=(1004, 646, 1151, 701), wait=(2, 100))
                self.ctler.clickChange(target="开始游戏", zone=(1004, 646, 1151, 701))
                self.ctler.wait(5)
                return True
            else:
                error += 1
                if error >= 5:
                    raise ValueError("尘白禁区:未知错误")
                self.ctler.wait(2)
            num -= 1
        return False
    elif _name == "SeasunGame.exe":
        self.ctler.ChangeReference((1280, 748))
        error = 0
        for i in range(120):
            if hwnd := FindWindow("UnrealWindow", "尘白禁区"):
                self.ctler.ChooseWindow(hwnd, (1920, 1080))
                return True
            _value = self.ctler.ocr((966, 693, 1200, 750))[0]
            if "开始游戏" in _value:
                self.ctler.clickChange(pos=(1087, 720), zone=(966, 693, 1200, 750))
                self.ctler.wait(5)
                continue
            elif "更新" in _value:
                if self.para["Update"]:
                    self.ctler.clickChange(pos=(1087, 720), zone=(966, 693, 1200, 750))
                    for t in range(180):
                        _v = self.ctler.ocr((966, 693, 1200, 750))[0]
                        if "正在更新" in _v:
                            self.ctler.wait(2)
                        else:
                            break
                    else:
                        raise ValueError("尘白禁区:更新超时")

                else:
                    self.send("尘白禁区:需要更新,当前未勾选自动更新,终止任务")
                    raise RuntimeError("尘白禁区:需要更新,当前未勾选自动更新,终止任务")
            else:
                error += 1
                if error >= 5:
                    raise ValueError("尘白禁区:未知错误")
                self.ctler.wait(2)


def LogSnow(self, second: int):
    # 登录&进入游戏
    self.send("开始识别游戏状态")
    server = self.para["OtherConfig"]["Snow"]["Server"]
    for i in range(second):
        sc = self.ctler.screenshot()
        _list = self.ctler.ocr(template=sc, mode=1)
        if server == 0:
            if self.ctler.StrFind("开始游戏", _list):
                server = 3
                self.ctler.wait(0.3)
                if self.para["AccountChoose"] and self.para["OtherConfig"]["License"]:
                    self.ctler.clickChange((1866, 219), zone=(984, 16, 1089, 66))
                    self.ctler.clickChange(target="切换", zone=(984, 16, 1089, 66))
                    self.ctler.wait(0.5)
                    self.ctler.clickChange((1150, 517), zone=(735, 554, 849, 630))
                    pos = self.ctler.findtext(self.para["AccountChoose"], (703, 462, 1216, 715))
                    if pos:
                        self.ctler.clickChange(pos, zone=(735, 554, 849, 589))
                    else:
                        raise ValueError("尘白禁区:账户识别错误")
                    self.ctler.clickChange(target="登录", zone=(904, 577, 1018, 641))
                    self.ctler.wait(0.8)
                try:
                    self.ctler.clickChange((986, 949), zone=(27, 962, 97, 1015))
                except:
                    self.ctler.click((1866, 219))
                    self.ctler.clickChange((986, 949), zone=(27, 962, 97, 1015))
                # self.ctler.clickChange("开始游戏", (883, 920, 1049, 989))
                self.send("登录游戏")
                self.ctler.wait(5)
                continue
        elif server == 1:
            if self.ctler.findpic(r"resources\snow\picture\login2.png", (853, 369, 1055, 461), sc)[1] >= 0.6:
                self.ctler.click((964, 679))
                self.send("登录B服账号")
                self.ctler.wait(4)
                continue
        elif server == 2:
            if self.ctler.StrFind("开始游戏", _list):
                server = 3
                self.ctler.wait(0.3)
                self.ctler.clickChange(pos=(930, 630), zone=(883, 920, 1049, 989))
                self.send("登录游戏")
                self.ctler.wait(5)
                continue
        if self.ctler.StrFind("获得道具", _list):
            self.ctler.click((967, 909))
            self.send("签到成功")
            self.ctler.wait(2.5)
            continue
        if self.ctler.StrFind("时间", _list):
            self.ctler.click((991, 123))
            self.ctler.wait(1.5)
            continue
        if self.ctler.StrFind("版本过低", _list):
            self.send("尘白禁区:版本过低")
            raise RuntimeError("尘白禁区:版本过低")
        if self.ctler.StrFind("服务器暂未开放", _list):
            self.send("尘白禁区:服务器暂未开放")
            raise RuntimeError("尘白禁区:服务器暂未开放")
        if self.ctler.StrFind("任务", _list):
            self.ctler.wait(0.3)
            sc = self.ctler.screenshot()
            if "任务" in self.ctler.ocr((1455, 324, 1533, 380), sc)[0]:
                self.send("加载到主界面")
                return True
            else:
                continue
        if self.ctler.StrFind("等级提升", _list):
            self.ctler.click((788, 1007))
            self.ctler.wait(8)
        self.ctler.press("esc")
        self.ctler.wait(0.8)
    raise ValueError("尘白禁区:登录超时")
