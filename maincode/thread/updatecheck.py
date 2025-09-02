from requests import get, exceptions
from maincode.config.maingroup import sg
from maincode.tools.main import VersionsCompare, logger, GetTracebackInfo
from time import localtime, strftime
from maincode.tools.constant import spr


def timercheck(self) -> None:
    try:
        # 检查休眠时间
        if self.sleeptime > 0:
            self.sleeptime -= 15
            return
        elif self.sleeptime < 0:
            logger.warning("sleeptime 小于 0，可能存在初始化错误")
            self.sleeptime = 0

        if not self.timerallow:
            return

        # 打印定时检测日志
        if spr["LoadUI"]:
            time_str = strftime("%H:%M:%S", localtime())
            print(f"{time_str} | INFO | SGA定时检测，SGA运行中...")

        self.SaveConfig()

        # 获取当前时间
        current_time = localtime()
        y, M, d, h, m, _, w = current_time[:7]
        date = (y, M, d)

        # 自动更新检查
        if sg.mainconfig.AutoUpdate and (date != sg.info.CurrentDate):
            if self.updatecheck():
                sg.info.CurrentDate = date
                return

        # 构造当前时间和配置时间元组
        nowtup = (
            (w + 2, [h, m]),
            (1, [h, m])
        )
        tc = sg.mainconfig.TimerConfig.model_dump()
        timetup = tuple(zip(tc['Execute'], tc['Time']))

        # 遍历定时任务
        for n, ti in enumerate(timetup):
            if ti in nowtup:
                ck = tc['ConfigKeys'][n]
                if ck:
                    num = sg.subconfig.FindItem(ck)[-1]
                    _config = sg.ReadSubFile(num)
                    self.TaskStart("timed", _config)
                    return
    except Exception as e:
        _str = GetTracebackInfo(e) + "定时检测异常"
        logger.error(_str)
        self.infoAdd(f"定时检测异常")


def updatecheck(self) -> bool:
    try:
        from json import loads
        url = "https://gitee.com/api/v5/repos/huixinghen/SucroseGameAssistant/releases/latest"
        downloadurl = {}
        self.infoHead()

        for i in range(3):
            try:
                response = get(url, timeout=10)
                if response.status_code == 200:
                    data = loads(response.text)
                    newversion = data["tag_name"]
                    ver = VersionsCompare(newversion, sg.info.Version)
                    if ver == 1:
                        self.infoAdd(f"检测到新版本：{newversion}")
                        text: str = data["body"]
                        try:
                            if "Latestv" in text:
                                lversion = text.split("Latest")[1].split("#")[0]
                                if VersionsCompare(lversion, sg.info.Version) == 1:
                                    self.infoAdd(f"不符合更新条件，请手动更新到以下版本及以上：{lversion},或重新安装最新版本")
                                    self.infoEnd()
                                    break
                        except IndexError:
                            logger.warning("无法解析最低支持版本号")
                        self.infoAdd(text, False)
                        self.infoAdd(
                            f"可通过此链接进行手动更新: \n"
                            f"https://gitee.com/huixinghen/SucroseGameAssistant/releases",
                            False
                        )
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
            except exceptions.RequestException as e:
                logger.warning(f"第 {i + 1} 次请求失败: {e}")
                continue
        else:
            self.infoAdd(f"检查更新超时...")
            self.infoEnd()

        if downloadurl:
            self.TaskStart("update", downloadurl)
            self.infoAdd("开始更新..")
        return True
    except exceptions.ConnectionError as e:
        _str = GetTracebackInfo(e) + "DNS解析失败, 检查更新异常"
        logger.error(_str)
        self.infoAdd(f"DNS解析失败")
        self.infoAdd(f"检查更新异常")
        return False
    except Exception as e:
        _str = GetTracebackInfo(e) + "检查更新异常"
        logger.error(_str)
        self.infoAdd(f"检查更新异常")
        return False
