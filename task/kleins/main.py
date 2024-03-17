# -*- coding:gbk -*-
from tools.environment import *
from .fight import Fight
from .dispatch import Dispatch
from .review import Review
from .market import Market
from .recruit import Recruit
from .reward import Reward
from .network import Network
from .mail import Mail
from .roll import Roll
import os
import traceback


class TaskKleins(Fight, Dispatch, Review, Market, Recruit, Reward, Network, Mail, Roll):
    def __init__(self):
        super().__init__()

    def kleins_start(self, task: type[dir]):
        _k = False
        self.task = task
        env.OCR.enable()
        self.indicate("开始任务:环行旅舍")
        self.kleins_launch()
        # noinspection PyBroadException
        try:
            self.kleins_log(60)
            # 触发舍友互动
            click((969, 374))
            wait(500)
            click((969, 374))
            wait(500)
            if self.task["功能0"]:
                self.indicate("开始:作战")
                if self.kleins_fight():
                    _k = True
                self.indicate("完成:作战")
            if self.task["功能1"]:
                self.indicate("开始:线下采购")
                self.kleins_dispatch()
                self.indicate("完成:线下采购")
            if self.task["功能2"]:
                self.indicate("开始:战术回顾")
                self.kleins_review()
                self.indicate("完成:战术回顾")
            if self.task["功能3"]:
                self.indicate("开始:集市领取")
                self.kleins_get_market()
                self.indicate("完成:集市领取")
            if self.task["功能4"]:
                self.indicate("开始:舍友访募")
                self.kleins_recruit()
                self.indicate("完成:舍友访募")
            if self.task["功能5"]:
                self.indicate("开始:今日工作")
                self.kleins_reward()
                self.indicate("完成:今日工作")
            if self.task["功能6"]:
                self.indicate("开始:卡门商网")
                self.kleins_market_network()
                self.indicate("完成:卡门商网")
            if self.task["功能7"]:
                self.indicate("开始:领取邮件")
                self.kleins_get_mail()
                self.indicate("完成:领取邮件")
            if self.task["功能8"]:
                self.indicate("开始:抽卡历史")
                self.kleins_get_roll()
                self.indicate("完成:抽卡历史")
        except Exception:
            self.indicate("任务执行异常:环行旅舍", log=False)
            logger.error("任务执行异常:环行旅舍\n%s" % traceback.format_exc())
            _k = True
        env.OCR.disable()
        if self.task["关闭软件"]:
            self.indicate("尝试关闭游戏")
            s, n = 15, 2
            if env.soft.kill(s, n):
                self.indicate("游戏已关闭")
            else:
                self.indicate(f"error:游戏关闭超时（{s * n}s）")
                raise RuntimeError("kleins exit error")
        self.indicate("完成任务:环行旅舍")
        return _k

    def kleins_launch(self):
        # 路径修正
        env.set_soft(None, (1, "UnityWndClass", "环行旅舍"))
        _path = self.task["启动"]["game"]
        if os.path.isfile(_path):
            dire, name = os.path.split(_path)
            if name == "环行旅舍.exe":
                env.soft.set_path(_path)
            elif name == "kleins.exe":
                path = dire + "/Games/环行旅舍.exe"
                if os.path.isfile(path):
                    env.soft.set_path(path)
                else:
                    self.indicate("环行旅舍，无效启动路径")
                    return 3
            else:
                self.indicate("环行旅舍，无效启动路径")
                return 3
        else:
            self.indicate("环行旅舍，无效启动路径")
            return 3
        # 启动游戏
        cond = env.soft.run()
        if cond == 2:
            self.indicate("游戏启动成功")
            self.indicate("等待加载,10秒后开始识别游戏状态")
            wait(1000)
            env.soft.foreground()
            wait(9000)
        elif cond == 1:
            self.indicate("游戏早已启动")
            env.soft.foreground()
            wait(1000)
        elif cond == 0:
            self.indicate("游戏启动超时")
            return 3
        env.mode(1)

    def kleins_log(self, second: int):
        # 登录&进入游戏
        self.indicate("开始识别游戏状态")
        server = self.task["启动"]["server"]
        net = 1
        for i in range(second):
            sc = screenshot()
            if server == 0:
                if "开始游戏" in ocr((870, 611, 1050, 655), sc)[0].replace(" ", ""):
                    wait(300)
                    click((930, 630))
                    self.indicate("登录游戏")
                    wait(5000)
                    os.remove(sc)
                    sc = screenshot()
            elif server == 1:
                if "登录账号" in ocr((870, 611, 1050, 655), sc)[0].replace(" ", ""):
                    wait(300)
                    click((960, 633))
                    self.indicate("登录账号")
                    wait(1500)
                    os.remove(sc)
                    sc = screenshot()
                if find_pic(r"assets\kleins\picture\login2.png", (853, 369, 1055, 461), sc)[1] >= 0.6:
                    click((958, 679))
                    self.indicate("登录游戏")
                    wait(5000)
                    os.remove(sc)
                    sc = screenshot()
            if "签到奖励" in ocr((832, 211, 1090, 313), sc)[0].replace(" ", ""):  # 签到奖励
                click((1469, 551))
                wait(1500)
                click((1789, 120))
                self.indicate("签到成功")
                wait(1000)
                os.remove(sc)
                sc = screenshot()
            _p, sim = find_pic("assets/kleins/picture/close/close2.png", search_path=sc)
            if sim >= 0.6:
                click(_p)
                wait(1500)
                os.remove(sc)
                sc = screenshot()
            if find_pic("assets/kleins/picture/home.png", (1739, 37, 1814, 98), sc)[1] >= 0.7:
                wait(1500)
                os.remove(sc)
                sc = screenshot()
                if find_pic("assets/kleins/picture/home.png", (1739, 37, 1814, 98), sc)[1] >= 0.7:
                    self.indicate("加载到主界面")
                    os.remove(sc)
                    return 0
            if find_pic("assets/kleins/picture/rehome.png", (238, 27, 355, 105), sc)[1] >= 0.7:
                click((295, 69))
                wait(1500)
                os.remove(sc)
                self.indicate("加载到主界面")
                return 0
            if "网络连接超时" in ocr((748, 448, 1183, 524), sc)[0].replace(" ", ""):
                self.indicate(f"error: 网络连接超时({net}次)")
                if net < 4:
                    net += 1
                    click((1063, 710))
                    wait(10000)
                else:
                    os.remove(sc)
                    raise RuntimeError("环行旅舍:网络连接超时多次")
            os.remove(sc)
            wait(1500)
        raise RuntimeError("环行旅舍:识别游戏状态超时")


if __name__ == '__main__':
    pass
