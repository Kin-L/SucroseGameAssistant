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
            val = find_pic(r"assets\genshin\picture\home\home.png", (0, 0, 97, 88))[1]
            if val >= 0.6:
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
            elif i == 15:
                self.indicate("error:加载世界超时\n")
                raise RuntimeError("原神:加载世界超时")

    # 从主界面打开子界面
    def open_sub(self, cho):
        sub_dir = {"地图": (358, 697), "背包": (663, 556), "冒险之证": (659, 698), "队伍配置": (352, 416)}
        x, y = sub_dir[cho]
        click(x, y)
        self.indicate("打开" + cho)
        wait(2000)

    # 从秘境传送
    def tp_domain(self, domain):
        tdir = {
            "仲夏庭园": "midsummer", "铭记之谷": "remembrance", "孤云凌霄之处": "guyun",
            "无妄引咎密宫": "hidden", "华池岩岫": "pool_cavern", "芬德尼尔之顶": "vindagnyr",
            "山脊守望": "ridge", "椛染之庭": "momiji", "沉眠之庭": "slumbering_court",
            "岩中幽谷": "the_lost_valley", "缘觉塔": "enlightenment", "赤金的废墟": "city_of_gold",
            "熔铁的孤塞": "fortress", "罪祸的终末": "denouement", "临瀑之城": "waterfall",

            "塞西莉亚苗圃": "cecilia_garden", "震雷连山密宫": "lianshan", "砂流之庭": "flow_sand",
            "有顶塔": "abject", "深潮的余响": "deep_tides",

            "忘却之峡": "forsaken", "太山府": "taishan", "堇色之庭": "violet_court",
            "昏识塔": "ignorance", "苍白的遗荣": "pale_glory"}
        self.indicate("尝试传送到秘境:\n  " + domain)
        for num in range(15):
            wait(300)
            (x, y), val = find_pic(f"assets/genshin/picture/domain/{tdir[domain]}.png", (738, 249, 1033, 886))
            if val >= 0.8:
                click(1555, y)
                wait(2000)
                break
            elif num <= 13:
                roll(1116, 296, -24)
            else:
                self.indicate("error:\n  未识别到秘境 " + domain)
                raise RuntimeError("原神:秘境识别异常")

    # 选择确认传送锚点图标并开始传送，最后判断传送成功
    def tp_point(self, num=0):
        (x, y), val = find_pic(r"assets\genshin\picture\maps\%s.png" % num, (1245, 621, 1528, 1023))
        if val >= 0.75:
            click(x, y)
            wait(800)
        click(1634, 1003)
        wait(3000)
        self.world()

    def check_overdue(self):
        if "物品过期" == ocr((869, 269, 1057, 333))[0]:
            self.indicate("识别到物品过期")
            click(971, 758)
            wait(2000)
