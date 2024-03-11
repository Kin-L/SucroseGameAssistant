from .main import *
from ..default_task import Task


class Genshin(Task):
    def __init__(self):
        super().__init__()

    def tp_fontaine1(self):
        self.home()
        self.indicate("前往枫丹:\n  枫丹廷凯瑟琳锚点")
        self.open_sub("冒险之证")
        click(300, 440)
        wait(800)
        click(537, 296)
        wait(800)
        self.tp_domain("深潮的余响")
        click(1107, 786)
        wait(800)
        self.tp_point()
        self.indicate("到达枫丹:\n  枫丹廷凯瑟琳锚点")
        
    # 打开主界面
    def home(self):
        m = 0
        while m >= 0:
            m += 1
            wait(1500)
            if "好友" in ocr((480, 442, 540, 481))[0]:
                m = -1
            else:
                press("esc")
            if m == 15:
                self.indicate("error:打开主界面超时\n")
                raise RuntimeError("原神:打开主界面超时")

    def world(self):
        i = 1
        while i > 0:
            i += 1
            wait(1000)
            pos, val = find_pic(r"assets\genshin\picture\world.png", (57, 998, 179, 1075))
            if val >= 0.6:
                i = 0
                self.indicate("加载到世界")
            elif i == 90:
                self.indicate("error:加载世界超时\n")
                raise RuntimeError("原神:加载世界超时")

    # 从主界面打开子界面
    def open_sub(self, cho):
        if click_text(cho, (117, 346, 742, 1052)):
            self.indicate("打开" + cho)
            wait(2500)
            return True
        else:
            return False

    # 从秘境传送
    def tp_domain(self, domain):
        self.indicate("尝试传送到秘境:\n  " + domain)
        if domain == "椛染之庭":
            _t = "染之庭"
        elif domain == "菫色之庭":
            _t = "色之庭"
        elif domain == "无妄引咎密宫":
            _t = "无妄引"
        else:
            _t = domain
        for num in range(18):
            wait(300)
            _list = ocr((764, 243, 1058, 847), mode=1)

            for i in _list:
                if _t in i[0]:
                    wait(800)
                    click(1555, int((i[1][1]+i[1][3])/2+40))
                    wait(2000)
                    return True
            if num <= 16:
                roll(1116, 296, -24)
            else:
                self.indicate("error:\n  未识别到秘境 " + domain)
                raise RuntimeError("原神:秘境识别异常")

    # 选择确认传送锚点图标并开始传送，最后判断传送成功
    def tp_point(self, num=0):
        if "传送" in ocr((1638, 983, 1749, 1035))[0]:
            pass
        else:
            (x, y), val = find_pic(r"assets\genshin\picture\maps\%s.png" % num, (1270, 649, 1327, 961))
            if val >= 0.75:
                click(x, y)
                wait(800)
            else:
                raise RuntimeError("原神:传送识别异常")
        click(1634, 1003)
        wait(3000)
        self.world()

    def check_overdue(self):
        if "物品过期" == ocr((869, 269, 1057, 333))[0]:
            self.indicate("识别到物品过期")
            click(971, 758)
            wait(2000)

    def team_ready(self):
        for i in range(15):
            sc = screenshot()
            t0 = ocr((1289, 993, 1428, 1046))[0]
            t1 = ocr((1637, 995, 1776, 1045))[0].strip(" ")
            os.remove(sc)
            if "编队" not in t0:
                return False
            elif t1 == "出战":
                click(1557, 1020)
                wait(500)
            else:
                return True
        raise RuntimeError("队伍加载超时")

    def turn_world(self):
        m = 0
        while m >= 0:
            m += 1
            wait(1500)
            pos, val = find_pic(r"assets\genshin\picture\world.png", (57, 998, 179, 1075))
            if val >= 0.6:
                m = -1
            else:
                press("esc")
            if m == 15:
                self.indicate("error:打开主界面超时\n")
                raise RuntimeError("原神:打开主界面超时")