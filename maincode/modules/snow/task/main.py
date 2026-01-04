import json
import sys
import requests
from maincode.tools.core.baseclass import SGAStop
from maincode.tools.system.notification import GetTracebackInfo
from maincode.tools.core.logger import logger
from maincode.tools.system.window import GetWindow
from time import sleep
from maincode.config.configctrl import scc
from win32gui import FindWindow
from os import path
from .energy import snowEnergy
from .dailytask import snowDailyTask
from .receive import snowOther
from .gacharecog import snowGachaRecog
from .xxkt import snowXXKT
from ..emulator.main import emulatorstart
from .rogue import snowRogue
from .guess import snowGuess


def get_gitee_file(file_path, branch="master"):
    """
    获取Gitee仓库文件内容
    owner: 仓库所有者
    repo: 仓库名
    file_path: 文件路径
    branch: 分支名，默认为master
    """
    url = f"https://gitee.com/api/v5/repos/huixinghen/SucroseGameAssistant/contents/{file_path}?ref={branch}"

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        # 如果是文件，内容在content字段中（base64编码）
        if 'content' in data:
            import base64
            content = base64.b64decode(data['content']).decode('utf-8')
            return content
        else:
            return "未找到文件内容"

    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"
    except Exception as e:
        return f"处理失败: {e}"


def CloseSnow(self):
    for _ in range(20):
        try:
            win1 = GetWindow("尘白禁区")
            win2 = GetWindow("Snowbreak: Containment Zone")
            if win1:
                win1.close()
            elif win2:
                win2.close()
            else:
                self.send(f"尘白禁区已关闭")
                self.para["startwait"] = True
                return True
        except Exception as e:
            logger.error(f"关闭窗口时发生异常: {e}")
        sleep(0.5)
    self.send(f"尘白禁区关闭超时")
    return False


def SnowHome(self):
    num = 30
    flag = False
    while num > 0:
        sc = self.ctler.screenshot()
        task_ocr_result = self.ctler.ocr((1458, 330, 1529, 379), sc)[0]
        exit_ocr_result = self.ctler.ocr((1617, 23, 1701, 70), sc)[0]
        if "任务" in task_ocr_result:
            if flag:
                return True
            else:
                flag = True
        elif "退出" in exit_ocr_result:
            self.ctler.clickChange(target="退出", zone=(1617, 23, 1701, 70))
            self.ctler.waitTo("任务", (1458, 330, 1529, 379), (0.4, 30))
            return True
        else:
            flag = False
            num -= 1
            self.ctler.press("esc")
            self.ctler.wait(0.7)
        self.ctler.wait(0.8)
    logger.error("尘白禁区返回主页超时")
    return False


def taskstart(self):
    if self.para["OtherConfig"]["Snow"]["Server"] == 3:
        emulatorstart(self)
        return
    self.SnowHome = SnowHome
    # print(self.para)
    self.send("开始任务:尘白禁区", True)
    num = 3
    with open("resources/snow/list.json", 'r', encoding='utf-8') as g:
        local_dict = json.load(g)
    if ("-hideui" in sys.argv) and (local_dict["LIST版本"] != 0):
        try:
            content = get_gitee_file("resources/snow/list.json", "master-v3")
            repo_dict = json.loads(content)
            if repo_dict["LIST版本"] > local_dict["LIST版本"]:
                with open("resources/snow/list.json", 'w', encoding='utf-8') as g:
                    json.dump(repo_dict, g, ensure_ascii=False, indent=1)
                self.game_dict = repo_dict["限时活动"]
            else:
                self.game_dict = local_dict["限时活动"]
        except Exception as e:
            _str = GetTracebackInfo(e)
            logger.error(_str + "SNOW_LIST文件获取异常, 沿用本地文件")
            self.game_dict = local_dict["限时活动"]
    else:
        self.game_dict = local_dict["限时活动"]
    while num > 0:
        try:
            # print("startwait", self.para.get("startwait", True))
            if self.para.get("startwait", True):
                SnowLaunch(self)
                if self.para.get("rogue", False):
                    snowRogue(self)
                    self.para["rogue"] = False
                    return
                elif self.para.get("guess", False):
                    snowGuess(self)
                    self.para["guess"] = False
                    return
                elif self.para.get("XXKT", False):
                    snowXXKT(self)
                    self.para["XXKT"] = False
                    return
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
            break
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
                    self.ctler.window.foreground()
                    if SnowHome(self):
                        self.ctler.wait(2)
                    else:
                        self.send(f"进行重试,等待中...")
                        self.para["startwait"] = True
                        CloseSnow(self)
                        self.ctler.wait(4)
                        continue
            else:
                CloseSnow(self)
                self.send(f"尘白禁区:执行异常,跳过流程")
                scc.info.TaskError = True
                break
        else:
            self.send(f"任务完成:尘白禁区")
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
    h1 = FindWindow("wailsWindow", "尘白禁区启动器")
    h2 = FindWindow("Qt5159QWindowIcon", "西山居启动器-尘白禁区")
    h3 = FindWindow("Qt5159QWindowIcon", "SnowBreak")
    if h1:
        hwnd = h1
        self.launcher_mode = "snow_launcher.exe"
    elif h2:
        hwnd = h2
        self.launcher_mode = "SeasunGame.exe"
    elif h3:
        hwnd = h3
        self.launcher_mode = "steam"
    else:
        if not (isinstance(_path, str) and path.isfile(_path) and
                path.split(_path)[1] in ["snow_launcher.exe", "SeasunGame.exe"]):
            self.send("启动器路径异常")
            raise RuntimeError("启动器路径异常")
        self.launcher_mode = path.split(_path)[1]
        if _dict["Server"] == 2:
            self.launcher_mode = "steam"
        if self.launcher_mode == "snow_launcher.exe":
            item = ["wailsWindow", "尘白禁区启动器"]
        elif self.launcher_mode == "SeasunGame.exe":
            item = ["Qt5159QWindowIcon", "西山居启动器-尘白禁区"]
        elif self.launcher_mode == "steam":
            item = ["Qt5159QWindowIcon", "SnowBreak"]
        else:
            self.send("启动器路径异常")
            raise RuntimeError("启动器路径异常")
        hwnd = FindWindow(*item)
        if not hwnd:
            hwnd = self.ctler.RunProg(f"start \"\" \"{_path}\"", [item], (0.4, 10), 15)
            assert hwnd
    self.ctler.ChooseWindow(hwnd, (1280, 748))
    LauchPrepare(self)


def LauchPrepare(self):
    if self.para["PreLoad"]:
        if self.launcher_mode in ["SeasunGame.exe", "steam"]:
            _pos, _sim = self.ctler.findpic(r"resources\snow\picture\pre-load2.png",
                                            (889, 638, 971, 708))
            if _sim:
                self.ctler.clickChange(zone=(889, 638, 971, 708), pos=_pos)
                self.ctler.wait(0.5)
                self.ctler.clickChange("确定")
                self.send("开始预下载")
                self.ctler.wait(0.5)
            else:
                self.send("暂无预下载")
        elif self.launcher_mode == "snow_launcher.exe":
            _pos = self.ctler.findtext("下", (781, 585, 950, 734))
            if _pos:
                self.ctler.clickChange(zone=(559, 317, 713, 391), pos=_pos)
                self.ctler.wait(0.5)
                self.ctler.clickChange("确定")
                self.send("开始预下载")
                self.ctler.wait(0.5)
            else:
                self.send("暂无预下载")
        else:
            raise ValueError("启动器路径异常")
    if self.launcher_mode == "snow_launcher.exe":
        self.ctler.ChangeReference((1280, 748))
        error = 0
        num = 120
        hwndNum = 0
        while num > 0:
            if hwnd := FindWindow("UnrealWindow", "尘白禁区"):
                self.ctler.ChooseWindow(hwnd, (1920, 1080))
                hwnd += 1
                if self.ctler.ZoomW != self.ctler.ZoomH:
                    if hwndNum == 3:
                        self.send(f"当前窗口: {self.ctler.window.rect}")
                        self.send("游戏窗口分辨率不适配, 请将窗口模式分辨率设置为16：9")
                        self.send("尝试切换")
                        self.ctler.press('alt+enter')
                        self.ctler.wait(1)
                        self.ctler.ChooseWindow(hwnd, (1920, 1080))
                        if self.ctler.ZoomW != self.ctler.ZoomH:
                            self.send(
                                "游戏窗口分辨率不适配，可能出现运行异常。建议使用16：9分辨率如：1920*1080，1600*900，2560*1440")
                            self.send(f"当前窗口: {self.ctler.window.rect}")
                        else:
                            self.send(f"切换后成功，当前窗口: {self.ctler.window.rect}")
                    else:
                        sleep(2)
                        continue
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
                error = -5
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
                self.ctler.waitTo("开始游戏", zone=(1004, 646, 1151, 701), wait=(2, 100))
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
    elif self.launcher_mode in ["SeasunGame.exe", "steam"]:
        self.ctler.ChangeReference((1280, 748))
        error = 0
        num = 120
        hwndNum = 0
        if self.launcher_mode == "SeasunGame.exe":
            item = ["UnrealWindow", "尘白禁区"]
        elif self.launcher_mode == "steam":
            item = ["UnrealWindow", "Snowbreak: Containment Zone"]
        else:
            return
        while num > 0:
            if hwnd := FindWindow(*item):
                self.ctler.ChooseWindow(hwnd, (1920, 1080))
                hwnd += 1
                if self.ctler.ZoomW != self.ctler.ZoomH:
                    if hwndNum == 3:
                        self.send(f"当前窗口: {self.ctler.window.rect}")
                        self.send("游戏窗口分辨率不适配, 请将窗口模式分辨率设置为16：9")
                        self.send("尝试切换")
                        self.ctler.press('alt+enter')
                        self.ctler.wait(1)
                        self.ctler.ChooseWindow(hwnd, (1920, 1080))
                        if self.ctler.ZoomW != self.ctler.ZoomH:
                            self.send(
                                "游戏窗口分辨率不适配，可能出现运行异常。建议使用16：9分辨率如：1920*1080，1600*900，2560*1440")
                            self.send(f"当前窗口: {self.ctler.window.rect}")
                        else:
                            self.send(f"切换后成功，当前窗口: {self.ctler.window.rect}")
                    else:
                        sleep(2)
                        continue
                return True
            _value = self.ctler.ocr((966, 693, 1200, 750))[0]
            if "开始游戏" in _value:
                self.ctler.click((1087, 720))
                self.ctler.wait(2)
                error = -2
                continue
            elif "更新" in _value:
                if self.para["Update"]:
                    for t in range(180):
                        _v = self.ctler.ocr((966, 693, 1200, 750))[0]
                        if "更新" == _v:
                            self.ctler.click((1087, 720))
                        elif "开始游戏" in _v:
                            self.ctler.click((1087, 720))
                            self.ctler.wait(2)
                            error = -2
                            break
                        self.ctler.wait(2)
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
        _list = self.ctler.ocr(mode=1)
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
                    self.ctler.clickChange((986, 949), zone=(27, 962, 97, 1015), errsc=False)
                except TimeoutError:
                    self.ctler.click((1866, 219))
                    self.ctler.clickChange((986, 949), zone=(27, 962, 97, 1015))
                # self.ctler.clickChange("开始游戏", (883, 920, 1049, 989))
                self.send("登录游戏")
                self.ctler.wait(5)
                continue
        elif server == 1:
            if self.ctler.findpic(r"resources\snow\picture\login2.png", (853, 369, 1055, 461))[1] >= 0.6:
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
        # if self.ctler.StrFind("获得道具", _list):
        #     self.ctler.click((967, 909))
        #     self.send("签到成功")
        #     self.ctler.wait(2.5)
        #     continue
        # if self.ctler.StrFind("时间", _list):
        #     self.ctler.click((991, 123))
        #     self.ctler.wait(1.5)
        #     continue
        if self.ctler.StrFind("版本过低", _list):
            self.send("尘白禁区:版本过低")
            raise ValueError("尘白禁区:版本过低")
        if self.ctler.StrFind("服务器暂未开放", _list):
            self.send("尘白禁区:服务器暂未开放")
            raise ValueError("尘白禁区:服务器暂未开放")
        if self.ctler.StrFind("任务", _list):
            self.ctler.wait(0.3)
            if "任务" in self.ctler.ocr((1455, 324, 1533, 380))[0]:
                self.send("加载到主界面")
                return True
            else:
                self.send("状态检测存疑：加载主界面")
                continue
        # if self.ctler.StrFind("等级提升", _list):
        #     self.ctler.click((788, 1007))
        #     self.ctler.wait(8)
        self.ctler.click((979, 955))
        self.ctler.wait(1.5)
    raise ValueError("尘白禁区:登录超时")
