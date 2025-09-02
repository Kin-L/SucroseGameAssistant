from maincode.config.info import info


class Zone:
    def __init__(self, *args):
        self.zone = args
        self.pos = args[:2]
        self.width = args[2] - args[0]
        self.high = args[3] - args[1]
        self.center = int(self.width / 2) + args[0], int(self.high / 2) + args[1]
        self.size = (self.width, self.high)


class LocTuple(tuple):
    def __new__(cls, iterable):
        return super().__new__(cls, iterable)


class CtrlBase:
    Zone = Zone
    LocTuple = LocTuple
    RefRes = (1920, 1080)  # 代码坐标的参考区域
    Rw = 1920
    Rh = 1080
    LocRes = Zone(0, 0, 1920, 1080)  # 本地桌面区域
    Lw = 1920
    Lh = 1080
    Operate = Zone(0, 0, 1920, 1080)  # 本地操作区域 左上角坐标和窗口大小
    Ox = 0
    Oy = 0
    Ow = 1920
    Oh = 1080
    ZoomW = 1  # 本地操作区域 相对于 代码坐标的参考分辨率 的缩放倍率 Zoom = OperateZone/ReferenceResolution
    ZoomH = 1
    scaling = 1  # 本地缩放

    def checkrun(self):
        ...

    # 代码坐标 -> 本地坐标
    def convert(self, args):
        # print(args, type(args), (self.ZoomW, self.ZoomH), (self.Ox, self.Oy))
        if type(args) is LocTuple:
            return args
        elif args is None:
            return LocTuple(self.Operate.zone)
        if len(args) == 2:
            x, y = args
            if isinstance(x, int):
                return LocTuple((int(x * self.ZoomW) + self.Ox, int(y * self.ZoomH) + self.Oy))
            elif isinstance(x, float):
                return LocTuple((int(x * self.Ow) + self.Ox, int(y * self.Oh) + self.Oy))
        elif len(args) == 4:
            x1, y1, x2, y2 = args
            if isinstance(x1, int):
                return LocTuple((
                    int(x1 * self.ZoomW) + self.Ox, int(y1 * self.ZoomH) + self.Oy,
                    int(x2 * self.ZoomW) + self.Ox, int(y2 * self.ZoomH) + self.Oy
                ))
            elif isinstance(x1, float):
                return LocTuple((
                    int(x1 * self.Ow) + self.Ox, int(y1 * self.Oh) + self.Oy,
                    int(x2 * self.Ow) + self.Ox, int(y2 * self.Oh) + self.Oy
                ))
        raise ValueError("Invalid coordinate format")

    # 本地坐标 -> 代码坐标
    def convertR(self, args):
        if len(args) == 2:
            x, y = args
            if isinstance(x, int):
                return int(x / self.ZoomW) - self.Ox, int(y / self.ZoomH) - self.Oy
        elif len(args) == 4:
            x1, y1, x2, y2 = args
            if isinstance(x1, int):
                return (
                    int(x1 / self.ZoomW) - self.Ox, int(y1 / self.ZoomH) - self.Oy,
                    int(x2 / self.ZoomW) - self.Ox, int(y2 / self.ZoomH) - self.Oy
                )
        raise ValueError("Invalid coordinate format")

    # 代码坐标 -> 本地坐标
    def convertVector(self, args):
        if type(args) is LocTuple:
            return args
        if len(args) == 2:
            x, y = args
            if isinstance(x, int):
                return LocTuple((int(x * self.ZoomW), int(y * self.ZoomH)))
        raise ValueError("Invalid vector format")

    # 本地坐标 -> 代码坐标
    def convertVectorR(self, args):
        if len(args) == 2:
            x, y = args
            if isinstance(x, int):
                return int(x / self.ZoomW), int(y / self.ZoomH)
        raise ValueError("Invalid vector format")

    @classmethod
    def ChangeReference(cls, zone):
        cls.RefRes = zone
        cls.Rw, cls.Rh = zone

    @classmethod
    def InitLocal(cls, zone):
        cls.LocRes = Zone(*zone)
        cls.Lw, cls.Lh = cls.LocRes.pos

    @classmethod
    def ChangeOperate(cls, zone):
        cls.Operate = Zone(*zone)
        cls.Ox, cls.Oy = cls.Operate.pos
        cls.Ow, cls.Oh = cls.Operate.size
        cls.ZoomW = cls.Ow / cls.Rw
        cls.ZoomH = cls.Oh / cls.Rh
        # print("ChangeOperate", zone, (cls.Ow, cls.Oh), (cls.Rw, cls.Rh), (cls.ZoomW, cls.ZoomH))


class SGAStop(BaseException):
    def __str__(self):
        return "SGA stop"


if __name__ == '__main__':
    pass
