from time import localtime
from cpufeature import CPUFeature
from traceback import format_exc
from win32con import SW_RESTORE
from win32gui import (IsIconic, ShowWindow,
                      SetForegroundWindow, GetForegroundWindow)
from time import sleep
from os import getcwd, path, makedirs
from typing import Optional, List
from sgacode.tools.configclass import SGAMainConfig, SGASubConfigGroup, ConfigTool
from sgacode.moduleclass import ModuleClass
from shutil import copyfile
import json
from sgacode.tools.main import logger


class SGAInfo:
    def __init__(self):
        self.version: str = "3.X"
        self.hwnd: int = 0  # SGA窗口句柄
        self.monitors: list = []  # 电脑显示器信息
        self.platform: str = ""  # 系统平台信息
        self.start_time = localtime()  # 记录SGA本次启动时间
        self.workdir = getcwd()  # 记录并检查SGA本次工作目录
        self.cpu_feature = CPUFeature["AVX2"]
        self.getmonitors()
        self.getplatform()

    def getmonitors(self) -> None:
        from screeninfo import get_monitors
        for i, monitor in enumerate(get_monitors(), start=1):
            self.monitors += [[i, (monitor.width, monitor.height), (monitor.x, monitor.y)]]

    def getplatform(self) -> None:
        import platform
        system = platform.system()
        release = platform.release()
        version = platform.version()
        if system == "Windows":
            if release == "10":
                build_number = int(version.split('.')[2])  # 获取构建版本号
                self.platform = "Windows 11" if build_number >= 22000 else "Windows 10"
            elif release == "7":
                self.platform = "Windows 7"
            else:
                self.platform = f"Windows-未知版本:{release}-Version: {version}）"
        else:
            self.platform = system

    def BasisFileInit(self):
        cachedir = "cache"
        scdir = "personal/script"
        rstpath = "resources/main/schtasks.json"
        pstpath = "personal/schtasks.json"
        rrspath = "resources/main/script/restart.bat"
        prspath = "personal/script/restart.bat"
        if not path.exists(cachedir):
            makedirs(cachedir)
        if not path.exists(scdir):
            makedirs(scdir)
        with open(rstpath, 'r', encoding='utf-8') as m:
            xml_dir = json.load(m)
        xml_list = xml_dir["part2"]
        xml_list[32] = f"      <Command>{self.workdir}\\SGA.exe</Command>\n"
        xml_list[34] = "      <WorkingDirectory>" + self.workdir + "</WorkingDirectory>\n"
        xml_dir["part2"] = xml_list
        with open(pstpath, 'w', encoding='utf-8') as x:
            json.dump(xml_dir, x, ensure_ascii=False, indent=1)

        f = open(rrspath, 'r', encoding='utf-8')
        start_list = f.readlines()
        f.close()
        start_list[2] = "start /d \"%s\" SGA.exe\n" % self.workdir
        f = open(prspath, 'w', encoding='utf-8')
        f.writelines(start_list)
        f.close()

        f = open("resources/main/script/maacreate.bat", 'r', encoding='ansi')
        bat_list = f.readlines()
        f.close()
        bat_list[1] = f" cd. > \"{self.workdir}/cache/maacomplete.txt\""
        f = open("personal/script/maacreate.bat", 'w', encoding='ansi')
        f.writelines(bat_list)
        f.close()

        rstvpath = "resources/main/script/restart.vbs"
        prsv = "personal/script/restart.vbs"
        pss = "personal/script/start-SGA.vbs"
        if not path.exists(prsv):
            copyfile(rstvpath, prsv)
        if not path.exists(pss):
            copyfile(rstvpath, pss)


class SGAGroup:
    def __init__(self, _logger):
        self.logger = _logger
        self.info = SGAInfo()
        self.runflag: Optional[bool] = None
        self.value: dict = {}
        self.mainconfig: Optional[SGAMainConfig] = None
        self.subconfig: Optional[SGASubConfigGroup] = None
        self.triggerflag: Optional[bool] = None
        self.running: bool = False

    def LoadConfig(self, configlist: List[ConfigTool]):
        # 配置信息加载
        self.subconfig = SGASubConfigGroup()  # 加载子配置信息
        self.subconfig.SetConfigList(configlist)
        self.subconfig.SetSignListt(ModuleClass.SignList)
        self.subconfig.LoadSubConfig()
        self.mainconfig = SGAMainConfig(self.subconfig)  # 加载主配置信息
        # 运行路径变化时，基础文件初始化
        if self.info.workdir != self.mainconfig["WorkDir"]:
            self.mainconfig["WorkDir"] = self.info.workdir
            self.info.BasisFileInit()

    def foreground(self) -> bool:
        if not self.info.hwnd:
            self.logger.debug("Environment.hwnd 未初始化")
            return False
        for i in range(10):
            current_hwnd = GetForegroundWindow()
            if current_hwnd == self.info.hwnd:
                self.logger.info("SGA窗口唤起成功")
                return True
            if IsIconic(self.info.hwnd):
                ShowWindow(self.info.hwnd, SW_RESTORE)
                sleep(0.2)
            if current_hwnd != self.info.hwnd:
                try:
                    SetForegroundWindow(self.info.hwnd)
                except Exception as e:
                    self.logger.debug(str(e) + format_exc() + "\nSGA窗口唤起异常：SetForegroundWindow")
                sleep(0.2)
        self.logger.info("SGA窗口唤起失败")
        return False

    def logger_environment_info(self):
        _str = (f"\n运行环境:\n"
                f"  工作目录:{self.info.workdir}\n"
                f"  CPUFeature:{self.info.cpu_feature}\n"
                f"  系统:{self.info.platform}\n"
                f"显示器:")
        for i, (w, h), (x, y) in self.info.monitors:
            _str += f"\n  编号:{i} 分辨率:{w}×{h} 位置:{x},{y}"
        self.logger.info(_str)

    def GetTriggerFlag(self) -> Optional[bool]:
        return self.triggerflag

    def SetTriggerFlag(self, state: Optional[bool]):
        self.triggerflag = state

    def GetRunning(self):
        return self.running

    def SetRunning(self, state: bool):
        self.running = state


sg = SGAGroup(logger)
if __name__ == '__main__':
    pass
