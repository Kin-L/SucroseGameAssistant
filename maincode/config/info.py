from time import localtime
from cpufeature import CPUFeature
from os import getcwd, makedirs
from shutil import copyfile
import json
import platform
from screeninfo import get_monitors
from pathlib import Path
from maincode.tools.core.baseclass import SGAStop
from maincode.tools.core.constant import spr
from maincode.tools.system.window import GetWindow


class SGAInfo:
    # 路径常量
    CACHE_DIR = spr.CACHE_DIR
    SCRIPT_DIR = spr.SCRIPT_DIR
    SCHTASKS_SRC = spr.SCHTASKS_SRC
    SCHTASKS_DST = spr.SCHTASKS_DST
    BAT_SRC = spr.BAT_SRC
    BAT_DST = spr.BAT_DST
    MAA_BAT_SRC = spr.MAA_BAT_SRC
    MAA_BAT_DST = spr.MAA_BAT_DST
    VBS_SRC = spr.VBS_SRC
    VBS_DST = spr.VBS_DST

    def __init__(self):
        self.Version: str = "v3.1.2"
        self.Window = GetWindow("砂糖代理")
        self.Monitors: list = []
        self.Platform: str = ""
        self.StartTime = localtime()
        self.CurrentDate = None
        self.Workdir = getcwd()
        self.CpuFeature = CPUFeature["AVX2"]
        self.OcrPath = ""
        self.TaskError = None
        self.StopFlag = None
        self.OtherConfig = {}

        self.getmonitors()
        self.getplatform()
        self.BasisFileInit()

    def checkrun(self):
        if self.StopFlag:
            raise SGAStop

    def getmonitors(self) -> None:
        for i, monitor in enumerate(get_monitors(), start=1):
            self.Monitors.append([i, (monitor.width, monitor.height), (monitor.x, monitor.y)])

    def getplatform(self) -> None:
        system = platform.system()
        release = platform.release()
        version = platform.version()
        if system == "Windows":
            if release == "10":
                try:
                    build_number = int(version.split('.')[2])
                    self.Platform = "Windows 11" if build_number >= 22000 else "Windows 10"
                except (IndexError, ValueError):
                    self.Platform = f"Windows-未知版本:{release}-Version: {version}）"
            elif release == "7":
                self.Platform = "Windows 7"
            else:
                self.Platform = f"Windows-未知版本:{release}-Version: {version}）"
        else:
            self.Platform = system

    def GetEnvironmentInfoStr(self):
        _ocr = self.OcrPath if self.OcrPath else "默认"
        _str = (
            f"\n运行环境:\n"
            f"  SGA版本:{self.Version}\n"
            f"  工作目录:{self.Workdir}\n"
            f"  CPUFeature:{self.CpuFeature}\n"
            f"  系统:{self.Platform}\n"
            f"  OCR路径:{_ocr}\n"
            f"显示器:"
        )
        for i, (w, h), (x, y) in self.Monitors:
            _str += f"\n  编号:{i} 分辨率:{w}×{h} 位置:{x},{y}"
        return _str

    @staticmethod
    def _safe_write_file(src_path, dst_path, line_updates):
        """通用文件读写函数，支持行替换"""
        try:
            with open(src_path, 'r', encoding='ansi') as f:
                lines = f.readlines()
            for line_no, new_line in line_updates.items():
                lines[line_no] = new_line
            with open(dst_path, 'w', encoding='ansi') as f:
                f.writelines(lines)
        except Exception as e:
            print(f"文件写入失败: {src_path} -> {dst_path}, 错误: {e}")

    def BasisFileInit(self):
        # 创建目录
        for dir_path in [self.CACHE_DIR, self.SCRIPT_DIR]:
            if not Path(dir_path).exists():
                try:
                    makedirs(dir_path)
                except Exception as e:
                    print(f"目录创建失败: {dir_path}, 错误: {e}")

        # 处理 schtasks.json
        try:
            with open(self.SCHTASKS_SRC, 'r', encoding='utf-8') as f:
                xml_dir = json.load(f)
            xml_list = xml_dir["part2"]
            xml_list[32] = f"      <Command>{self.Workdir}\\SGA.exe</Command>\n"
            xml_list[34] = f"      <WorkingDirectory>{self.Workdir}</WorkingDirectory>\n"
            xml_dir["part2"] = xml_list
            with open(self.SCHTASKS_DST, 'w', encoding='utf-8') as f:
                json.dump(xml_dir, f, ensure_ascii=False, indent=1)
        except Exception as e:
            print(f"schtasks.json 处理失败: {e}")

        # 处理 start-SGA.bat
        self._safe_write_file(
            self.BAT_SRC,
            self.BAT_DST,
            {2: f"start /d \"{self.Workdir}\" SGA.exe\n"}
        )

        # 处理 maacreate.bat
        self._safe_write_file(
            self.MAA_BAT_SRC,
            self.MAA_BAT_DST,
            {1: f" cd. > \"{self.Workdir}/cache/maacomplete.txt\"\n"}
        )

        # 复制 vbs 文件
        if not Path(self.VBS_DST).exists():
            try:
                copyfile(self.VBS_SRC, self.VBS_DST)
            except Exception as e:
                print(f"VBS 文件复制失败: {e}")


info = SGAInfo()
