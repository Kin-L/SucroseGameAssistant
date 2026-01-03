from maincode.config.info import info
from maincode.tools.core.baseclass import CtrlBase
from maincode.tools.controller.adb import ADBController
from typing import Union
import subprocess
from time import time, strftime, localtime
from maincode.tools.system.notification import GetTracebackInfo
from PIL import ImageGrab, Image
from os import path, makedirs
import numpy as np
from maincode.tools.core.logger import logger
from ctypes import windll
import mss
import mss.tools


class SGAScreen(CtrlBase, ADBController):

    def screenshot_win(self, zone="FULL", save=False) -> Union[Image.Image, str]:
        """
        Windows平台截图方法

        Args:
            zone: 截图区域
            save: 是否保存截图

        Returns:
            Image.Image或str: 截图结果
        """
        self.checkrun()
        try:
            if zone == "WINDOW":
                zone = self.Operate.zone
            elif isinstance(zone, tuple):
                ...
            elif zone == "FULL":
                zone = None
            else:
                raise ValueError(f"zone参数异常： {zone}")
            try:
                shot = ImageGrab.grab(zone)
            except OSError:
                with mss.mss() as sct:
                    if zone is None:
                        monitor = sct.monitors[0]
                    else:
                        left, top, width, height = zone
                        monitor = {
                            "left": left,
                            "top": top,
                            "width": width,
                            "height": height
                        }
                    sct_img = sct.grab(monitor)
                    shot = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            except Exception:
                raise
            return self._save_screenshot(shot, save)
        except Exception as e:
            logger.error(f"Windows截图失败: {str(e)}")
            raise

    def screenshot_adb(self, zone=None, save=False) -> Union[Image.Image, str]:
        """
        ADB方式截图方法（用于安卓模拟器）

        Args:
            zone: 截图区域
            save: 是否保存截图

        Returns:
            Image.Image或str: 截图结果
        """
        self.checkrun()
        try:
            process = subprocess.Popen(
                [self.adb_path, "-s", self.device_serial, 'exec-out', 'screencap'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=2 ** 22
            )
            stdout, error = process.communicate()

            # 检查是否有错误输出
            if error:
                raise RuntimeError(f"ADB截图命令执行失败: {error.decode()}")

            # 将二进制数据转换为Pillow图像
            try:
                header = stdout[:12]
                width = int.from_bytes(header[0:4], byteorder='little')
                height = int.from_bytes(header[4:8], byteorder='little')
                format_code = int.from_bytes(header[8:12], byteorder='little')

                # 验证格式 (通常为RGBA或RGBX)
                if format_code not in [1, 3, 4]:
                    raise RuntimeError(f"不支持的像素格式: {format_code}")

                # 提取像素数据 (跳过16字节头部)
                pixel_data = stdout[16:]

                # 转换为numpy数组
                if format_code == 1:  # RGBA
                    img_array = np.frombuffer(pixel_data, dtype=np.uint8).reshape((height, width, 4))
                    mode = 'RGBA'
                else:  # RGBX或其他格式
                    img_array = np.frombuffer(pixel_data, dtype=np.uint8).reshape((height, width, 4))
                    mode = 'RGBX'

                # 转换为Pillow图像
                shot = Image.fromarray(img_array, mode)
            except Exception as e:
                raise RuntimeError(f"图像转换失败: {str(e)}")

            if isinstance(zone, tuple):
                shot = shot.crop(zone)

            return self._save_screenshot(shot, save)
        except Exception as e:
            logger.error(f"ADB截图失败: {str(e)}")
            raise

    @staticmethod
    def _save_screenshot(image: Image.Image, save: Union[bool, str]) -> Union[Image.Image, str]:
        """
        保存截图的通用方法

        Args:
            image: 要保存的图像
            save: 保存选项（False=不保存, True=自动命名保存, str=指定路径保存）

        Returns:
            Image.Image或str: 根据save参数返回图像对象或文件路径
        """
        if not save:
            return image

        # 确保缓存目录存在
        cache_dir = "cache"
        if not path.exists(cache_dir):
            makedirs(cache_dir)

        if isinstance(save, str):
            try:
                image.save(save)
                return save
            except Exception as e:
                _path = path.join(cache_dir, f"{str(time())[-5:]}.png")
                _str = GetTracebackInfo(e) + f"保存截图错误，进行默认路径保存：{_path}"
                logger.debug(_str)
        else:
            _path = path.join(cache_dir, f"{str(time())[-5:]}.png")

        image.save(_path)
        return _path

    @staticmethod
    def SaveShot(image, name):
        if isinstance(image, Image.Image):
            now = strftime("%Y-%m-%d %H-%M-%S", localtime())
            name = name + now
            _path = f"personal/errorsc/{name}.png"
            if not path.exists(r"personal/errorsc"):
                makedirs("personal/errorsc")
            image.save(_path)
            logger.info(f"保存图片：{_path}")
            return _path
        else:
            logger.error(f"error: SaveShot 无效传入 {type(image)}")
            logger.error(image)
            return f"SaveShot 无效传入 {type(image)}"

    def SaveShotBA(self, bef_pic, aft_pic):
        _path1 = self.SaveShot(bef_pic, "bef")
        _path2 = self.SaveShot(aft_pic, "aft")
        logger.error(f"截图导出bef: {_path1}")
        logger.error(f"截图导出aft: {_path2}")

    def SetLocal(self, monitor_num=0):
        (w, h), (x, y) = info.Monitors[monitor_num]
        self.InitLocal((x, y, w, h))

    def SetScale(self):
        user32 = windll.user32
        user32.SetProcessDPIAware()
        now_wid = user32.GetSystemMetrics(0)
        if now_wid == 0:
            raise RuntimeError("获取屏幕宽度失败")
        ori_wid = user32.GetSystemMetrics(0)
        self.scaling = round(ori_wid / now_wid, 2)

    def DeviceMode(self, device="windows", exe_path=None):
        if device == "windows":
            self.__class__.screenshot = self.__class__.screenshot_win
        elif device == "emulator":
            self.exe_path = exe_path
            self.__class__.screenshot = self.__class__.screenshot_adb
            try:
                self.connect_to_emulator()
                self.WaitTime = (0, 10)
                h, w = self.getresolution()
                self.ChangeOperate((0, 0, w, h))
            except Exception as e:
                logger.error(f"连接模拟器失败: {e}")
                raise
