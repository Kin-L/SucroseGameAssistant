from os import path, startfile
import subprocess
from time import sleep, time
from maincode.main.info import info
import re
from contextlib import contextmanager


class Zone:
    def __init__(self, *args):
        self.zone = args
        self.pos = args[:2]
        self.width = args[2] - args[0]
        self.high = args[3] - args[1]
        self.center = int(self.width / 2) + args[0], int(self.high / 2) + args[1]
        self.size = (self.width, self.high)


class LocTuple(tuple):
    def __init__(self, *args):
        pass


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

    @staticmethod
    def checkrun():
        if info.StopFlag:
            raise SGAStop

    # 代码坐标 -> 本地坐标
    def convert(self, args):
        # print(args, type(args), (self.ZoomW, self.ZoomH), (self.Ox, self.Oy))
        if type(args) is LocTuple:
            return args
        elif args is None:
            return LocTuple(self.Operate.zone)
        if len(args) == 2:
            x, y = args
            if type(args[0]) is int:
                return LocTuple((int(x * self.ZoomW) + self.Ox, int(y * self.ZoomH) + self.Oy))
            elif type(args[0]) is float:
                return LocTuple((int(x * self.Ow) + self.Ox, int(y * self.Oh) + self.Oy))
        elif len(args) == 4:
            x1, y1, x2, y2 = args
            # print(args, self.ZoomW, self.ZoomH, (self.Ox, self.Oy))
            if type(args[0]) is int:
                return LocTuple(((int(x1 * self.ZoomW) + self.Ox, int(y1 * self.ZoomH) + self.Oy,
                                  int(x2 * self.ZoomW) + self.Ox, int(y2 * self.ZoomH) + self.Oy)))
            elif type(args[0]) is float:
                return LocTuple((int(x1 * self.Ow) + self.Ox, int(y1 * self.Oh) + self.Oy,
                                 int(x2 * self.Ow) + self.Ox, int(y2 * self.Oh) + self.Oy,))
        raise ValueError

    # 本地坐标 -> 代码坐标
    def convertR(self, args):
        if len(args) == 2:
            x, y = args
            if type(args[0]) is int:
                return int(x / self.ZoomW) - self.Ox, int(y / self.ZoomH) - self.Oy
        elif len(args) == 4:
            x1, y1, x2, y2 = args
            if type(args[0]) is int:
                return (int(x1 / self.ZoomW) - self.Ox, int(y1 / self.ZoomH) - self.Oy,
                        int(x2 / self.ZoomW) - self.Ox, int(y2 / self.ZoomH) - self.Oy)
            raise ValueError

    # 代码坐标 -> 本地坐标
    def convertVector(self, args):
        if type(args) is LocTuple:
            return args
        if len(args) == 2:
            x, y = args
            if type(args[0]) is int:
                return LocTuple((int(x * self.ZoomW), int(y * self.ZoomH)))
        raise ValueError

    # 本地坐标 -> 代码坐标
    def convertVectorR(self, args):
        if len(args) == 2:
            x, y = args
            if type(x) is int:
                return int(x / self.ZoomW), int(y / self.ZoomH)
        raise ValueError

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


class ADBController:
    adb_path = None
    device_serial = None
    exe_path = None
    port = None
    adb = None

    def connect_to_emulator(self):
        emulator_ip = "127.0.0.1"
        print(self.exe_path)
        dire, name = path.split(self.exe_path)
        self.adb_path = path.join(dire, "adb.exe")
        assert path.exists(self.adb_path)
        if name == "MuMuPlayer.exe":
            port = 7555
        else:
            raise ValueError
        self.device_serial = f"{emulator_ip}:{port}"
        # """连接模拟器"""
        # # 启动ADB服务
        subprocess.run([self.adb_path, 'kill-server'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run([self.adb_path, 'start-server'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run([self.adb_path, "disconnect", self.device_serial], capture_output=True, text=True)
        if self.adbconnect():
            return True
        else:
            for _ in range(3):
                startfile(self.exe_path)
                for _ in range(20):
                    if self.adbconnect():
                        return True
            raise RuntimeError(f"无法连接到 {emulator_ip}:{self.port}")

    def adbconnect(self):
        try:
            proc = subprocess.run([self.adb_path, "connect", self.device_serial], capture_output=True, text=True)
            output = proc.stdout
            # print("output:", output)
            if "connected" in output or "already" in output:
                print(f"成功连接到模拟器: {self.device_serial}")
                self.adb = subprocess.Popen(
                    [self.adb_path, '-s', self.device_serial, 'shell'],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    bufsize=0
                )
                self._exec_shell_command('echo test')
                return True
            print(f"连接尝试失败，重试中...")
            sleep(2)
        except subprocess.CalledProcessError as e:
            print(f"连接失败: {e.stderr.decode('utf-8')}")
            sleep(2)
            return False

    def _run_adb_command(self, cmd):
        """执行ADB命令"""
        full_cmd = [self.adb_path]
        if self.device_serial:
            full_cmd.extend(["-s", self.device_serial])
        full_cmd.extend(cmd)

        return subprocess.run(
            full_cmd,
            check=True,
            capture_output=True,
            text=True
        )

    def _exec_shell_command(self, command: str):
        """
        执行ADB shell命令

        :param command: 要执行的命令
        :return: 命令输出
        """
        if not self.adb:
            raise ConnectionError("ADB连接未建立")
        self.adb.stdin.write(f"{command}\n".encode('utf-8'))
        self.adb.stdin.flush()

    @contextmanager
    def _persistent_shell(self):
        """创建持久化的ADB shell连接"""
        if not self.device_serial:
            raise Exception("未连接到任何设备")
        cmd = [self.adb_path, "-s", self.device_serial, "shell"]
        proc = subprocess.Popen(cmd,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                bufsize=1)  # 行缓冲
        try:
            yield proc
        finally:
            proc.stdin.close()
            proc.terminate()
            proc.wait()

    def getresolution(self):
        output = subprocess.run([self.adb_path, "-s", self.device_serial, "shell", "wm", "size"],
                                capture_output=True, text=True).stdout.strip()
        # 解析输出格式: "Physical size: 1080x1920" 或 "Override size: 720x1280"
        match = re.search(r"(\d+)x(\d+)", output)
        if match:
            return int(match.group(1)), int(match.group(2))


if __name__ == '__main__':
    pass
