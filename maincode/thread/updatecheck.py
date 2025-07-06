from maincode.main.maingroup import sg
from maincode.tools.main import VersionsCompare
from time import localtime, strftime
import keyboard
from .taskctrl import SGAMain7


class SGAMain8(SGAMain7):
    def __init__(self, userui):
        super().__init__(userui)
        if self.loadui:
            self.overall.btcheckupdate.clicked.connect(self.updatecheck)
            self.mainwidget.btconfigsave.clicked.connect(self.ManualSaveConfig)
            keyboard.add_hotkey("ctrl+s", self.ManualSaveConfig)
            self.loading.hide()
            self.loading.lower()
            self.infoAdd("加载完成", False)
            self.infoEnd()
        self.timer.timeout.connect(self.timercheck)
        self.timer.start(15000)

    def timercheck(self):
        if self.loadui:
            time_str = strftime("%H:%M:%S", localtime())
            print(f"{time_str} | INFO | SGA定时检测，SGA运行中...")
        if self.sleeptime > 0:
            self.sleeptime -= 15
            return
        else:
            self.sleeptime = 0
            if not self.timerallow:
                return
        self.SaveConfig()
        y, M, d, h, m, _, w = localtime()[0:7]
        date = (y, M, d)
        if sg.mainconfig.AutoUpdate and (date != sg.info.CurrentDate):
            sg.info.CurrentDate = date
            self.updatecheck()
            return
        nowtup = ((w + 2, [h, m]), (1, [h, m]))
        tc = sg.mainconfig.TimerConfig.model_dump()
        timetup = tuple(zip(tc['Execute'], tc['Time']))
        # print(tc)
        for n, ti in enumerate(timetup):
            # print(ti, nowtup)
            if ti in nowtup:
                # print("ti:", ti)
                ck = tc['ConfigKeys'][n]
                if ck:
                    # print("ck:", ck)
                    num = sg.subconfig.FindItem(ck)[-1]
                    _config = sg.ReadSubFile(num)
                    self.TaskStart("timed", _config)
                    return

    def updatecheck(self):
        from requests import get
        from json import loads
        url = "https://gitee.com/api/v5/repos/huixinghen/SucroseGameAssistant/releases/latest"
        downloadurl = {}
        self.infoHead()
        for i in range(3):
            response = get(url, timeout=10)
            if response.status_code == 200:
                data = loads(response.text)
                newversion = data["tag_name"]
                ver = VersionsCompare(newversion, sg.info.Version)
                if ver == 1:
                    self.infoAdd(f"检测到新版本：{newversion}")
                    text: str = data["body"]
                    if "Latestv" in text:
                        lversion = text.split("Latest")[1].split("#")[0]
                        if VersionsCompare(lversion, sg.info.Version) == 1:
                            self.infoAdd(f"不符合更新条件，请手动更新到以下版本及以上：{lversion},或重新安装最新版本")
                            self.infoEnd()
                            break
                    self.infoAdd(text, False)
                    self.infoAdd(f"可通过此链接进行手动更新: \n"
                                 f"https://gitee.com/huixinghen/SucroseGameAssistant/releases", False)
                    assets = data["assets"]
                    for d in assets:
                        if "replace" in d["name"]:
                            downloadurl = d
                            break
                    else:
                        self.infoAdd("未找到更新包", False)
                        self.infoEnd()
                    break
                elif ver == 0:
                    self.infoAdd(f"当前已为最新版本")
                    self.infoEnd()
                    break
                else:
                    self.infoAdd(f"当前为提前测试版本，无需更新")
                    self.infoEnd()
                    break
        else:
            self.infoAdd(f"检查更新超时...")
            self.infoEnd()
        if downloadurl:
            self.TaskStart("update", downloadurl)
            self.infoAdd("开始更新..")
