import re
import subprocess
from contextlib import contextmanager
from os import path, startfile
from time import sleep


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
                try:
                    startfile(self.exe_path)
                except Exception as e:
                    print(f"启动模拟器失败: {e}")
                for _ in range(20):
                    if self.adbconnect():
                        return True
                    sleep(2)
            raise RuntimeError(f"无法连接到 {emulator_ip}:{port}")

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
