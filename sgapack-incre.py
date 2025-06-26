import subprocess
from os import path, chdir, walk, makedirs
import shutil
import sys
import hashlib


def calculate_file_hash(filepath, hash_algorithm='md5', buffer_size=65536):
    """计算文件的哈希值"""
    hash_func = hashlib.new(hash_algorithm)
    with open(filepath, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            hash_func.update(data)
    return hash_func.hexdigest()


if path.exists("dist"):
    shutil.rmtree("dist")
# 启动进程
cmdline = [sys.executable, "-m", "PyInstaller", "SGAv3.spec"]
result = subprocess.run(cmdline, shell=True, capture_output=True, text=True)
print("stdout, stderr, 返回码:", result.stdout, result.stderr, result.returncode)
if result.returncode:
    raise RuntimeError
if not path.exists("release/SGAv3"):
    print("未找到参照包体")
    exit()
lis = [["dist/SGAv3/_internal", "release/SGAv3/_internal"],
       ["dist/SGAv3/SGA.exe", "release/SGAv3/SGA.exe"],
       ["ocr-json", "release/SGAv3/ocr-json"],
       ["resources", "release/SGAv3/resources"],
       ["update.txt", "release/SGAv3/update.txt"]]
lis2 = []
for src, drc in lis:
    if path.isdir(src):
        for root, _, files in walk(src):
            for file in files:
                s0, d0 = path.join(src, root, file), path.join(drc, root, file)
                if path.exists(s0):
                    if path.exists(d0) and calculate_file_hash(s0) == calculate_file_hash(d0):
                        continue
                    lis2.append([s0, d0])
    else:
        if path.exists(src):
            if path.exists(drc) and calculate_file_hash(src) == calculate_file_hash(drc):
                continue
            lis2.append([src, drc])
version = "3.X"
_str = f"/SGAv3-{version}-replace/"
if path.exists(f"release/SGAv3-{version}-replace"):
    makedirs(f"release/SGAv3-{version}-replace")
for src, drc in lis2:
    shutil.copyfile(src, drc.replace("/SGAv3/", _str))
chdir("release")
rar_path = "D:/Program Files/WinRAR/WinRAR.exe"
cmdline = [rar_path, "a", f"SGAv3-{version}-replace.zip", f"SGAv3-{version}-replace"]
result = subprocess.run(cmdline, shell=True, capture_output=True, text=True)
print("stdout, stderr, 返回码:", result.stdout, result.stderr, result.returncode)
if result.returncode:
    raise RuntimeError
chdir("..")
print("sgapack-replace完成")
