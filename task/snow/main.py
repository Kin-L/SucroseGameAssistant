# -*- coding:gbk -*-
from tools.environment import *
from tools.software import find_hwnd
from .fight import Fight
from .daily import Daily
from .mail import Mail
from .roll import Roll
import os
import traceback


class TaskSnow(Fight, Daily, Mail, Roll):
    def __init__(self):
        super().__init__()

    def snow_start(self, task: type[dir]):
        _k = False
        self.task = task
        print(task)
        env.OCR.enable()
        self.indicate("开始任务:尘白禁区")
        self.snow_launch()
        # noinspection PyBroadException
        try:
            self.snow_log(60)
            click((829, 585))
            wait(500)
            click((829, 585))
            wait(500)
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
            logger.error("任务执行异常：尘白禁区\n%s" % traceback.format_exc())
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
        if os.path.isfile(_path):
            dire, name = os.path.split(_path)
            if name == "snow_launcher.exe":
                env.soft.set_path(_path)
                env.soft.set_hwnd_find(1, "wailsWindow", "尘白禁区启动器")
            elif name == "SeasunGame.exe":
                env.soft.set_path(_path)
                env.soft.set_hwnd_find(1, "Qt5159QWindowIcon", "西山居启动器-尘白禁区")
            else:
                self.indicate("尘白禁区，无效启动路径")
                raise ValueError("尘白禁区:无效启动路径")
        else:
            self.indicate("尘白禁区，无效启动路径")
            raise ValueError("尘白禁区:无效启动路径")
        # 启动游戏
        for u in range(2):
            if env.soft.find_hwnd():
                env.soft.foreground()
            else:
                if env.soft.run(fls=False):
                    self.indicate("启动器打开成功")
                else:
                    self.indicate("打开启动器超时")
                    raise RuntimeError("尘白禁区:打开启动器超时")
            wait(1000)

            if self.task["预下载"]:
                _p, sim = find_pic(r"assets\snow\picture\pre-load.png")
                if sim:
                    click(_p)
                    wait(1500)
                    click_text("确定")
                    wait(2000)
                else:
                    self.indicate("暂无预下载")
            if self.lauch_prepare():
                for p in range(10):  # 0, "UnrealWindow", "尘白禁区"
                    _h = find_hwnd((1, None, "尘白禁区"))
                    if _h:
                        env.soft.set_hwnd_find(0, "UnrealWindow", "尘白禁区")
                        env.soft.hwnd = _h
                        if env.mode(1):
                            env.soft.set_pid(env.soft.hwnd)
                            self.indicate("游戏已启动")
                            env.soft.foreground()
                            return True
                        else:
                            env.soft.foreground()
                            wait(3000)
                    else:
                        env.soft.foreground()
                        wait(1000)
                        click_text("开始游戏")
                        wait(2000)
            raise RuntimeError("尘白禁区:启动超时")
        raise RuntimeError("尘白禁区:启动异常")

    def lauch_prepare(self):
        for i in range(120):
            if find_hwnd((0, "UnrealWindow", "尘白禁区")):
                return True
            _list = ocr(mode=1)
            for o in _list:
                if res := text_match(o, "开始游戏"):
                    click(res)
                    return True
                elif res := text_match(o, "检查更新"):
                    click(res)
                    wait(2000)
                    break
                elif res := text_match(o, "获取更新"):
                    if self.task["更新"]:
                        click(res)
                        wait(2000)
                        click_text("确定")
                        wait(2000)
                        break
                    else:
                        self.indicate("尘白禁区:需要更新,当前未勾选自动更新,终止任务")
                        raise RuntimeError("尘白禁区:需要更新,当前未勾选自动更新,终止任务")
                elif text_match(o, "更新完成"):
                    click_text("确定")
                    wait(2000)
                    return False
                elif text_match(o, "更新中"):
                    self.indicate("更新中...")
                    for t in range(180):
                        wait(20000)
                        if not click_text("更新中"):
                            break
                        elif t == 179:
                            raise RuntimeError("尘白禁区:更新超时")
                    break
        return False

    def snow_log(self, second: int):
        # 登录&进入游戏
        self.indicate("开始识别游戏状态")
        server = self.task["启动"]["server"]
        for i in range(second):
            sc = screenshot()
            if server == 0:
                if "开始游戏" in ocr((883, 920, 1049, 989))[0]:
                    server = 2
                    wait(300)
                    if self.task["账号选择"]:
                        click((1864, 222))
                        wait(1000)
                        click((1033, 38))
                        wait(800)
                        click((1152, 522))
                        wait(800)
                        click_text(self.task["账号选择"], (703, 462, 1216, 715))
                        wait(800)
                        click((964, 607))
                        wait(800)
                    for r in range(3):
                        click((930, 630))
                        wait(800)
                    self.indicate("登录游戏")
                    wait(5000)
                    os.remove(sc)
                    sc = screenshot()
            elif server == 1:
                if find_pic(r"assets\snow\picture\login2.png", (853, 369, 1055, 461), sc)[1] >= 0.6:
                    click((964, 679))
                    self.indicate("登录B服账号")
                    wait(4000)
                    os.remove(sc)
                    sc = screenshot()
            if "获得道具" in ocr((813, 45, 1099, 138), sc)[0]:
                click((967, 909))
                self.indicate("签到成功")
                os.remove(sc)
                sc = screenshot()
                wait(2500)
            if "时间" in ocr((368, 217, 482, 249), sc)[0]:
                click((991, 123))
                os.remove(sc)
                sc = screenshot()
                wait(1500)
            if "维护" in ocr((1003, 419, 1190, 513), sc)[0]:
                os.remove(sc)
                raise RuntimeError("尘白禁区:游戏维护中")
            if "版本过低" in ocr((692, 414, 925, 513), sc)[0]:
                os.remove(sc)
                raise RuntimeError("尘白禁区:版本过低")
            if "服务器暂未开放" in ocr((784, 418, 1148, 508), sc)[0]:
                os.remove(sc)
                raise RuntimeError("尘白禁区:服务器暂未开放")
            if "任务" in ocr((1552, 364, 1618, 409), sc)[0]:
                wait(300)
                os.remove(sc)
                sc = screenshot()
                if "任务" in ocr((1552, 364, 1618, 409), sc)[0]:
                    self.indicate("加载到主界面")
                    os.remove(sc)
                    return True
            if "等级提升" in ocr((1076, 356, 1345, 448), sc)[0]:
                click((788, 1007))
                wait(8000)
            while 1:
                _p, sim = find_pic("assets/snow/picture/close.png", (1459, 122, 1805, 368), search_path=sc)
                if sim >= 0.6:
                    click(_p)
                    wait(1500)
                    os.remove(sc)
                    sc = screenshot()
                else:
                    break
            while 1:
                _p, sim = find_pic(r"assets\snow\picture\home.png", (1444, 0, 1921, 94), search_path=sc)
                if sim >= 0.6:
                    click(_p)
                    wait(1500)
                    os.remove(sc)
                    sc = screenshot()
                else:
                    break
            os.remove(sc)
            wait(1500)
        raise RuntimeError("尘白禁区:登录超时")


if __name__ == '__main__':
    pass
