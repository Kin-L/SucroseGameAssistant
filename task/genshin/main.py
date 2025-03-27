from tools.environment import *
from tools.software import find_hwnd, get_pid, close
from win32gui import FindWindow
from .team import Team
from .dispatch import Dispatch
from .transformer import Transformer
from .crystalfly import CatchFly
from .daily import Daily
from .rambler import Rambler
from .cut_tree.main import CutTree
from .mail import Mail
from .gpass import Pass
from subprocess import run as cmd_run

class TaskGenshin(Team, Dispatch, Transformer,CatchFly, Daily, Rambler,Mail, CutTree, Pass):
    def __init__(self):
        super().__init__()

    def genshin_start(self, task: type[dir]): #总执行流程
        _k = False
        if task["运行方式"] == "SGA":
            _k = self.SGA_run(task)
        elif task["运行方式"] == "BGI一条龙":
            _k = self.BGI_run(task)
        return _k
        
    def BGI_run(self, task):
        self.task = task
        self.indicate("开始任务:原神")
        try:
            # 确认BGI路径
            pid = get_pid("BetterGI.exe")
            if pid :
                self.indicate("BGI已启动,准备重启")
                close(pid)
            _path = self.task["启动"]["BGI"]
            if os.path.isfile(_path):
                dire, name = os.path.split(_path)
                if name == "BetterGI.exe":
                    pass
                else:
                    self.indicate("BGI,无效启动路径")
                    return True
            else:
                self.indicate("BGI,无效启动路径")
                return True
            # 启动BGI
            cmd = f"start \"\" \"{_path}\""
            for n in range(2):
                cmd_run(cmd, shell=True)
                for sec in range(10):
                    wait(1000)
                    hwnd = FindWindow(None, "更好的原神")
                    if hwnd:
                        self.indicate("BGI启动成功")
                        wait(500)
                        break
                    elif sec == 9:
                        self.indicate("BGI启动异常")
                        return True
            # 打开一条龙
            env.OCR.enable()
            click_text("一条龙", (511,222,1411,822))
            wait(200)
            # 修改BGI设置
            _p = find_text("每日秘境刷取配置", (511,222,1411,822))
            roll(_p, -80)      
            _p = find_text("关闭游戏和软件", (1177,730,1411,822))
            if not _p:
                (x, y) = find_text("任务完成后执行的操作", (511,222,1411,822))
                click((x+120, y+15))
                wait(200)
                click_text("关闭游戏和软件", (511,222,1411,942), once = True)
            # 执行一条龙
            wait(400)
            (x, y) = find_text("任务列表", (511,222,1411,822))
            click((x+120, y))
            env.OCR.disable()
            # 检测关闭
            wait(30000)
            while 1:
                wait(10000)
                if not find_hwnd((1, "UnityWndClass", "原神")):
                    break
        except Exception:
            self.indicate("任务执行异常:原神", log=False)
            logger.error("任务执行异常:原神\n%s" % format_exc())
            sc = scshot()
            _path = errorsc_save(sc)
            logger.error(f"截图导出: {_path}")
            return True
        self.indicate("完成任务:原神")
        return False

    def SGA_run(self, task):
        _k = False
        self.task = task
        env.OCR.enable()
        self.indicate("开始任务:原神")
        self.task["resin"] = None
        self.genshin_launch()
        # noinspection PyBroadException
        try:
            self.genshin_log(60)
            if self.task["功能0"]:
                self.indicate("开始:队伍切换")
                self.genshin_team()
                self.indicate("完成:队伍切换")
            if self.task["功能1"]:
                self.indicate("开始:探索派遣")
                if self.genshin_dispatch():
                    _k = True
                self.indicate("完成:探索派遣")
            if self.task["功能2"]:
                self.indicate("开始:参量质变仪")
                if self.genshin_transformer():
                    _k = True
                self.indicate("完成:参量质变仪")
            if self.task["功能3"]:
                self.indicate("开始:自动晶蝶")
                if self.genshin_catch_fly():
                    _k = True
                self.indicate("完成:自动晶蝶")
            if self.task["功能5"]:
                self.indicate("开始:尘歌壶")
                self.genshin_rambler()
                self.indicate("完成:尘歌壶")
            if self.task["功能6"]:
                self.indicate("开始:领取邮件")
                self.genshin_mail()
                self.indicate("完成:领取邮件")
            if self.task["功能7"]:
                self.indicate("开始:自动伐木")
                if self.genshin_cut_tree():
                    _k = True
                self.indicate("完成:自动伐木")
            if self.task["功能8"]:
                self.indicate("开始:体力日常")
                if self.daily_activity():
                    _k = True
                self.indicate("完成:自动秘境")
            if self.task["功能9"]:
                self.indicate("开始:领取纪行")
                self.genshin_pass()
                self.indicate("完成:领取纪行")
        except Exception:
            self.indicate("任务执行异常:原神", log=False)
            logger.error("任务执行异常:原神\n%s" % format_exc())
            sc = scshot()
            _path = errorsc_save(sc)
            logger.error(f"截图导出: {_path}")
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
        self.indicate("完成任务:原神")
        return _k

    def genshin_launch(self):
        # 路径修正
        env.set_soft(None, (0, "UnityWndClass", "原神"))
        _path = self.task["启动"]["game"]
        # print(_path)
        if isfile(_path):
            dire, name = split(_path)
            if name == "YuanShen.exe":
                env.soft.set_path(_path)
            elif name == "launcher.exe":
                path = dire + "/Genshin Impact Game/YuanShen.exe"
                if isfile(path):
                    env.soft.set_path(path)
                else:
                    self.indicate("原神,无效启动路径")
                    raise ValueError("原神:无效启动路径")
            else:
                self.indicate("原神,无效启动路径")
                raise ValueError("原神:无效启动路径")
        else:
            self.indicate("原神,无效启动路径")
            raise ValueError("原神:无效启动路径")
        # 启动游戏
        env.soft.hwnd = find_hwnd(env.soft.mode_cls_tit)
        cond = env.soft.run()
        if cond == 1:
            self.indicate("游戏早已启动")
            wait(1000)
        elif cond == 2:
            self.indicate("游戏启动成功")
            self.indicate("等待加载,10秒后开始识别游戏状态")
            wait(10000)
        elif cond == 0:
            self.indicate("游戏启动超时")
            raise RuntimeError("原神:游戏启动超时")
        for i in range(10):
            env.soft.foreground()
            wait(1000)
            if env.mode(1):
                break
            else:
                env.soft.foreground()
                wait(2000)
        
    def genshin_log(self, second: int):
        # 登录&进入游戏
        self.indicate("开始识别游戏状态")
        server = self.task["启动"]["server"]
        for i in range(second):
            sc = scshot()
            if server == 0:
                if "点击进入" in ocr((897, 989, 1027, 1048))[0].replace(" ", ""):
                    server = 2
                    click((930, 630))
                    self.indicate("开门")
                    wait(4000)
                    sc = scshot()
            elif server == 1:
                if find_pic(r"assets\genshin\picture\login2.png", (863, 370, 1059, 467), sc)[1] >= 0.6:
                    click((953, 659))
                    self.indicate("登录B服账号")
                    wait(4000)
                    sc = scshot()
                if "点击进入" in ocr((897, 989, 1027, 1048))[0].replace(" ", ""):
                    server = 2
                    click((930, 630))
                    self.indicate("开门")
                    wait(4000)
                    sc = scshot()
            if find_pic(r"assets\genshin\picture\sighin.png", (865, 240, 1060, 470), sc)[1] >= 0.6:
                click((930, 850))
                wait(800)
                click((930, 850))
                wait(100)
                click((930, 850))
                wait(1000)
                click((930, 850))
                wait(800)
                self.indicate("今日月卡领取成功")
                sc = scshot()
            if find_pic(r"assets\genshin\picture\world.png", (57, 998, 179, 1075), sc)[1] >= 0.6:
                self.indicate("加载到世界")
                del sc
                click((509, 313))
                wait(300)
                click((509, 313))
                wait(300)
                break
            if "好友" in ocr((480, 442, 540, 481))[0]:
                self.indicate("加载到主界面")
                del sc
                click((509, 313))
                wait(300)
                click((509, 313))
                wait(300)
                break
            _p, val0 = find_pic(r"assets\genshin\picture\close0.png", (1683, 0, 1919, 236), sc)
            if val0 >= 0.6:
                click(_p)
                wait(2500)
            _p, val1 = find_pic(r"assets\genshin\picture\close1.png", (1609, 178, 1737, 293), sc)
            if val1 >= 0.6:
                click(_p)
                wait(2500)
            del sc
            if i == second - 1:
                self.indicate(f"登录超时（{second * 2}s）")
                raise RuntimeError("原神:识别游戏状态超时")
            wait(2000)
            

if __name__ == '__main__':
    logger.enable_console()
    logger.hr("欢迎使用 砂糖代理v1.1\n"
              "https://github.com/Kin-L/SGA-Sucrose_Game_Assistant\n"
              "此程序为免费开源项目 如果你付了钱请立刻退款", 0)
    pass
