from tools.environment import *
from tools.software import find_hwnd
from .fight import Fight
from .daily import Daily
from .mail import Mail
from .roll import Roll
from traceback import format_exc
from os.path import isfile, split, exists


class TaskSnow(Fight, Daily, Mail, Roll):
    def __init__(self):
        super().__init__()

    def snow_start(self, task: type[dir]):
        _k = False
        self.task = task
        env.OCR.enable()
        self.indicate("开始任务:尘白禁区")
        self.snow_launch()
        # noinspection PyBroadException
        try:
            self.snow_log(60)
            click((829, 585))
            wait(300)
            click((829, 585))
            wait(300)
            if self.task["功能0"]:
                self.snow_fight()
            if self.task["功能1"]:
                self.snow_daily()
            if self.task["功能2"]:
                self.snow_mail()
            if self.task["功能3"]:
                self.snow_roll()
            self.indicate("执行完成")
            env.OCR.disable()
        except Exception:
            self.indicate("任务执行异常:尘白禁区", log=False)
            logger.error("任务执行异常：尘白禁区\n%s" % format_exc())
            _k = True
        env.OCR.disable()
        if self.task["关闭软件"]:
            self.indicate("尝试关闭游戏")
            s, n = 15, 2
            if env.soft.kill(s, n):
                self.indicate("游戏已关闭")
            else:
                self.indicate(f"error:游戏关闭超时({s * n}s)")
                raise RuntimeError("genshin exit error")
        self.indicate("完成任务:尘白禁区")
        return _k

    def snow_launch(self):
        # 路径修正
        env.set_soft(None, (0, "UnrealWindow", "尘白禁区"))
        _path = self.task["启动"]["snow_path"]
        if isfile(_path):
            dire, name = split(_path)
            if name == "snow_launcher.exe":
                env.soft.set_path(_path)
                env.soft.set_hwnd_find(1, "wailsWindow", "尘白禁区启动器")
                _value = env.soft.run(fls=False)
                _laucher = 1
                env.soft.compile_resolution = (1280, 748)
            elif name == "SeasunGame.exe":
                env.soft.set_path(_path)
                env.soft.set_hwnd_find(1, "Qt5159QWindowIcon", "西山居启动器-尘白禁区")
                _value = env.soft.run(fls=False)
                _laucher = 2
                env.soft.compile_resolution = (1280, 768)
            else:
                self.indicate("尘白禁区，无效启动路径")
                raise ValueError("尘白禁区:无效启动路径")
        else:
            self.indicate("尘白禁区，无效启动路径")
            raise ValueError("尘白禁区:无效启动路径")
        # 启动游戏
        for u in range(2):
            # env.soft.get_window_information(False)
            env.mode(3)
            if _value == 1:
                self.indicate("启动器已打开")
            elif _value == 2:
                self.indicate("启动器打开成功")
            else:
                if env.soft.run(fls=False):
                    self.indicate("启动器打开成功")
                else:
                    self.indicate("打开启动器超时")
                    raise RuntimeError("尘白禁区:打开启动器超时")
            env.soft.foreground()
            wait(1000)

            if self.task["预下载"] and _laucher == 1:
                _value = ocr((781, 585, 950, 734))
                if "下" in _value:
                    click_change((879, 668), (559, 317, 713, 391))
                    wait(500)
                    click_text("确定")
                    self.indicate("开始预下载")
                    wait(500)
                else:
                    self.indicate("暂无预下载")
            if self.lauch_prepare(_laucher):
                for p in range(10):  # 0, "UnrealWindow", "尘白禁区"
                    _h = find_hwnd((0, "UnrealWindow", "尘白禁区"))
                    if _h:
                        env.soft.set_hwnd_find(0, "UnrealWindow", "尘白禁区")
                        env.soft.hwnd = _h
                        env.soft.run()
                        env.soft.compile_resolution = (1920, 1080)
                        if env.mode(1):
                            env.soft.set_pid(env.soft.hwnd)
                            self.indicate("游戏已启动")
                            env.soft.foreground()
                            return True
                        else:
                            env.soft.foreground()
                            wait(3000)
                    else:
                        wait(1000)
                        # env.soft.foreground()
                        # wait(500)
                        # click_text("开始游戏", (1004, 646, 1151, 701))
                        # wait(500)
            env.soft.kill()
            env.soft.run(fls=False)
            # raise RuntimeError("尘白禁区:启动超时")
        raise RuntimeError("尘白禁区:启动异常")

    def lauch_prepare(self, _laucher):
        if _laucher == 1:
            error = 0
            for i in range(120):
                if find_hwnd((0, "UnrealWindow", "尘白禁区")):
                    return True
                _value = ocr((1004, 646, 1151, 701))[0]
                if "开始游戏" in _value:
                    click_change((1073, 673), (1004, 646, 1151, 701))
                    wait(5000)
                    return True
                elif "获取更新" in _value:
                    if self.task["更新"]:
                        click_change((1073, 673), (718, 476, 821, 536))
                        click_change((750, 499), (718, 476, 821, 536))
                        error = 0
                    else:
                        self.indicate("尘白禁区:需要更新,当前未勾选自动更新,终止任务")
                        raise RuntimeError("尘白禁区:需要更新,当前未勾选自动更新,终止任务")
                elif "检查更新" in _value:
                    for t in range(180):
                        _v = ocr((1004, 646, 1151, 701))
                        if "检查更新" in _v:
                            wait(2000)
                        else:
                            break
                        # _value1 = ocr((578, 465, 749, 549), sc)
                        # _value2 = ocr((1004, 646, 1151, 701), sc)
                        # del sc
                        # if "确定" in _value1:
                        #     click_change((639, 499), (578, 465, 749, 549))
                    else:
                        raise RuntimeError("尘白禁区:更新超时")
                elif "更新中" in _value:
                    pos = wait_text("开始游戏", (1004, 646, 1151, 701), (2000, 100))
                    click_change(pos, (1004, 646, 1151, 701))
                    wait(5000)
                    return True
                else:
                    error += 1
                    if error >= 5:
                        print(_value)
                        print(env.soft.frame, env.soft.zoom)
                        print(screenshot((1004, 646, 1151, 701)))
                        raise RuntimeError("尘白禁区:未知错误")
                    wait(2000)
            return False
        elif _laucher == 2:
            error = 0
            for i in range(120):
                if find_hwnd((0, "UnrealWindow", "尘白禁区")):
                    return True
                _value = ocr((966, 693, 1200, 750))[0]
                if "开始游戏" in _value:
                    click_change((1087, 720), (966, 693, 1200, 750))
                    wait(5000)
                    return True
                elif "更新" in _value:
                    if self.task["更新"]:
                        click_change((1087, 720), (966, 693, 1200, 750))
                        for t in range(180):
                            _v = ocr((966, 693, 1200, 750))
                            if "正在更新" in _v:
                                wait(2000)
                            else:
                                break
                            # _value1 = ocr((578, 465, 749, 549), sc)
                            # _value2 = ocr((1004, 646, 1151, 701), sc)
                            # del sc
                            # if "确定" in _value1:
                            #     click_change((639, 499), (578, 465, 749, 549))
                        else:
                            raise RuntimeError("尘白禁区:更新超时")

                    else:
                        self.indicate("尘白禁区:需要更新,当前未勾选自动更新,终止任务")
                        raise RuntimeError("尘白禁区:需要更新,当前未勾选自动更新,终止任务")
                else:
                    error += 1
                    if error >= 5:
                        print(env.soft.frame, env.soft.zoom)
                        print(screenshot((1004, 646, 1151, 701)))
                        raise RuntimeError("尘白禁区:未知错误")
                    wait(2000)

    def snow_log(self, second: int):
        # 登录&进入游戏
        self.indicate("开始识别游戏状态")
        server = self.task["启动"]["server"]
        started = False
        for i in range(second):
            sc = scshot()
            _list = ocr(template=sc, mode=1)
            if not started:
                if server == 0:
                    if str_find("开始游戏", _list):
                        server = 2
                        wait(300)
                        if self.task["账号选择"] and exists("license.txt"):
                            click_change((1866, 219), (984, 16, 1089, 66))
                            click_text("切换", (984, 16, 1089, 66))
                            click_change((1150, 513),  (735, 554, 849, 589))
                            pos = find_text(self.task["账号选择"], (703, 462, 1216, 715))
                            if pos:
                                click_change(pos, (735, 554, 849, 589))
                            else:
                                raise RuntimeError("尘白禁区:账户识别错误")
                            click_text("登录", (904, 577, 1018, 641))
                        click_change((930, 630), (883, 920, 1049, 989))
                        self.indicate("登录游戏")
                        wait(5000)
                        started = True
                        continue
                elif server == 1:
                    if find_pic(r"assets\snow\picture\login2.png", (853, 369, 1055, 461), sc)[1] >= 0.6:
                        click((964, 679))
                        self.indicate("登录B服账号")
                        wait(4000)
                        started = True
                        continue
            if str_find("获得道具", _list):
                click((967, 909))
                self.indicate("签到成功")
                wait(2500)
                continue
            if str_find("时间", _list):
                click((991, 123))
                wait(1500)
                continue
            # if str_find("维护", _list):
            #     raise RuntimeError("尘白禁区:游戏维护中")
            if str_find("版本过低", _list):
                raise RuntimeError("尘白禁区:版本过低")
            if str_find("服务器暂未开放", _list):
                raise RuntimeError("尘白禁区:服务器暂未开放")
            if str_find("任务", _list):
                wait(300)
                sc = scshot()
                if "任务" in ocr((1455, 324, 1533, 380), sc)[0]:
                    self.indicate("加载到主界面")
                    return True
                else:
                    continue
            if str_find("等级提升", _list):
                click((788, 1007))
                wait(8000)
            while 1:
                _p, sim = find_pic("assets/snow/picture/close.png", (1459, 122, 1805, 368), sc)
                if sim >= 0.6:
                    click(_p)
                    wait(1500)
                    
                    sc = scshot()
                else:
                    break
            while 1:
                _p, sim = find_pic(r"assets\snow\picture\home.png", (1444, 0, 1921, 94), sc)
                if sim >= 0.6:
                    click(_p)
                    wait(1500)
                    
                    sc = scshot()
                else:
                    break
            
            wait(1500)
        raise RuntimeError("尘白禁区:登录超时")


if __name__ == '__main__':
    pass
