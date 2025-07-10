from time import localtime
from cpufeature import CPUFeature
from os import getcwd, path, makedirs
from shutil import copyfile
import json
from maincode.tools.main import GetWindow


class SGAInfo:
    def __init__(self):
        self.Version: str = "v3.0.1"
        # SGA窗口句柄
        self.Window = GetWindow("砂糖代理")
        self.Monitors: list = []  # 电脑显示器信息
        self.Platform: str = ""  # 系统平台信息
        self.StartTime = localtime()  # 记录SGA本次启动时间
        self.CurrentDate = None
        self.Workdir = getcwd()  # 记录并检查SGA本次工作目录
        self.CpuFeature = CPUFeature["AVX2"]
        self.OcrPath = ""
        self.TaskError = None
        self.StopFlag = None
        self.getmonitors()
        self.getplatform()
        self.OtherConfig = {}

    def getmonitors(self) -> None:
        from screeninfo import get_monitors
        for i, monitor in enumerate(get_monitors(), start=1):
            self.Monitors += [[i, (monitor.width, monitor.height), (monitor.x, monitor.y)]]

    def getplatform(self) -> None:
        import platform
        system = platform.system()
        release = platform.release()
        version = platform.version()
        if system == "Windows":
            if release == "10":
                build_number = int(version.split('.')[2])  # 获取构建版本号
                self.Platform = "Windows 11" if build_number >= 22000 else "Windows 10"
            elif release == "7":
                self.Platform = "Windows 7"
            else:
                self.Platform = f"Windows-未知版本:{release}-Version: {version}）"
        else:
            self.Platform = system

    def GetEnvironmentInfoStr(self):
        _str = (f"\n运行环境:\n"
                f"  工作目录:{self.Workdir}\n"
                f"  CPUFeature:{self.CpuFeature}\n"
                f"  系统:{self.Platform}\n"
                f"显示器:")
        for i, (w, h), (x, y) in self.Monitors:
            _str += f"\n  编号:{i} 分辨率:{w}×{h} 位置:{x},{y}"
        return _str

    def BasisFileInit(self):
        cachedir = "cache"
        scdir = "personal/script"
        rstpath = "resources/main/schtasks.json"
        pstpath = "personal/schtasks.json"
        rrspath = "resources/main/script/start-SGA.bat"
        prspath = "personal/script/start-SGA.bat"
        if not path.exists(cachedir):
            makedirs(cachedir)
        if not path.exists(scdir):
            makedirs(scdir)
        with open(rstpath, 'r', encoding='utf-8') as m:
            xml_dir = json.load(m)
        xml_list = xml_dir["part2"]
        xml_list[32] = f"      <Command>{self.Workdir}\\SGA.exe</Command>\n"
        xml_list[34] = "      <WorkingDirectory>" + self.Workdir + "</WorkingDirectory>\n"
        xml_dir["part2"] = xml_list
        with open(pstpath, 'w', encoding='utf-8') as x:
            json.dump(xml_dir, x, ensure_ascii=False, indent=1)

        f = open(rrspath, 'r', encoding='ansi')
        start_list = f.readlines()
        f.close()
        start_list[2] = "start /d \"%s\" SGA.exe\n" % self.Workdir
        f = open(prspath, 'w', encoding='ansi')
        f.writelines(start_list)
        f.close()

        f = open("resources/main/script/maacreate.bat", 'r', encoding='ansi')
        bat_list = f.readlines()
        f.close()
        bat_list[1] = f" cd. > \"{self.Workdir}/cache/maacomplete.txt\""
        f = open("personal/script/maacreate.bat", 'w', encoding='ansi')
        f.writelines(bat_list)
        f.close()

        rstvpath = "resources/main/script/start-SGA.vbs"
        pss = "personal/script/start-SGA.vbs"
        if not path.exists(pss):
            copyfile(rstvpath, pss)


info = SGAInfo()
