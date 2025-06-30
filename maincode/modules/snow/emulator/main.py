import subprocess

from maincode.tools.myclass import SGAStop
from maincode.tools.main import GetTracebackInfo, logger
from time import sleep
from win32gui import FindWindow
from os import path
from .energy import snowEnergy
from .dailytask import snowDailyTask
from .other import snowOther
from .gacharecog import snowGachaRecog


def CloseSnow(self):
    package_name = "com.dragonli.projectsnow.lhm"
    cmd1 = [self.ctler.adb_path, "-s", self.ctler.device_serial, "shell", "ps", "-A", "|", "grep", package_name]
    cmd2 = [self.ctler.adb_path, "-s", self.ctler.device_serial, "shell", "am", "force-stop", package_name]
    for _ in range(20):
        output = subprocess.run(cmd1, capture_output=True, text=True)
        if package_name in output.stdout:
            subprocess.run(cmd2, capture_output=True, text=True)
        else:
            return True
        self.ctler.wait(1)
    self.send(f"尘白禁区关闭超时")
    return False


def SnowHomeEmulator(self):
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
            self.ctler.tapChange(target="退出", zone=(1617, 23, 1701, 70))
            self.ctler.waitTo("任务", (1458, 330, 1529, 379), (0.4, 30))
            return True
        else:
            flag = False
            num -= 1
            self.ctler.tap("KEYCODE_BACK")
        self.ctler.wait(0.8)
    raise TimeoutError("尘白禁区返回主页超时")


def emulatorstart(self):
    self.SnowHome = SnowHomeEmulator

    self.ctler.DeviceMode("emulator", self.para["OtherConfig"]["Snow"]["Path"])
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
                self.ctler.tap((829, 585))
                self.ctler.wait(0.3)
                self.ctler.tap((829, 585))
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
                self.ctler.wait(4)
                self.SnowHome(self)
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
    package_name = "com.dragonli.projectsnow.lhm"
    cmd1 = [self.ctler.adb_path, "-s", self.ctler.device_serial, "shell", "ps", "-A", "|", "grep", package_name]
    cmd2 = [self.ctler.adb_path, "-s", self.ctler.device_serial, "shell", "monkey", "-p", package_name, "1"]
    for _ in range(20):
        output = subprocess.run(cmd1, capture_output=True, text=True)
        if package_name in output.stdout:
            subprocess.run(cmd2, capture_output=True, text=True)
            return True
        else:
            subprocess.run(cmd2, capture_output=True, text=True)
        sleep(2)
    self.send(f"尘白禁区启动超时")
    return False


def LogSnow(self, second: int):
    # 登录&进入游戏
    self.send("开始识别游戏状态")
    started = False
    for i in range(second):
        sc = self.ctler.screenshot()
        _list = self.ctler.ocr(template=sc, mode=1)
        print("_list:", _list)
        if not started:
            if self.para["AccountChoose"] and self.para["OtherConfig"]["License"]:
                if self.ctler.StrFind("欢迎", _list):
                    self.ctler.tapChange((1102, 72), zone=(984, 16, 1089, 66))
                    self.ctler.tapChange((1158, 492), zone=(738, 533, 910, 586))
                    pos = self.ctler.findtext(self.para["AccountChoose"], (731, 524, 1216, 769))
                    if pos:
                        self.ctler.tapChange(pos, zone=(738, 533, 910, 586))
                    else:
                        raise ValueError("尘白禁区:账户识别错误")
                    self.ctler.tapChange(target="登录", zone=(873, 538, 1035, 621))
                    self.ctler.tapChange((986, 949), zone=(27, 962, 97, 1015))
                    self.send("登录游戏")
                    self.ctler.wait(5)
                    started = True
                    continue
        if self.ctler.StrFind("开始游戏", _list):
            self.ctler.tapChange((986, 949), zone=(27, 962, 97, 1015))
            self.send("登录游戏")
            self.ctler.wait(5)
            started = True
            continue
        if self.ctler.StrFind("获得道具", _list):
            self.ctler.tap((967, 909))
            self.send("签到成功")
            self.ctler.wait(2.5)
            continue
        if self.ctler.StrFind("时间", _list):
            self.ctler.tap((991, 123))
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
            if "任务" in self.ctler.ocr((1331, 266, 1436, 346), sc)[0]:
                self.send("加载到主界面")
                return True
            else:
                continue
        if self.ctler.StrFind("等级提升", _list):
            self.ctler.tap((788, 1007))
            self.ctler.wait(8)
        while 1:
            _p, sim = self.ctler.findpic("resources/snow/picture/close.png", (1459, 122, 1805, 368), sc)
            if sim >= 0.6:
                self.ctler.tap(_p)
                self.ctler.wait(1.5)
                sc = self.ctler.screenshot()
            else:
                break
        while 1:
            _p, sim = self.ctler.findpic("resources/snow/picture/home.png", (1444, 0, 1921, 94), sc)
            if sim >= 0.6:
                self.ctler.tap(_p)
                self.ctler.wait(1.5)
                sc = self.ctler.screenshot()
            else:
                break
        self.ctler.wait(0.2)
    raise ValueError("尘白禁区:登录超时")
