import os
import subprocess
from os import path, chdir
import shutil
import sys
if path.exists("dist"):
    shutil.rmtree("dist")
# 启动进程
cmdline = [sys.executable, "-m", "PyInstaller", "SGAv3.spec"]
result = subprocess.run(cmdline, shell=True, capture_output=True, text=True)
print("stdout, stderr, 返回码:", result.stdout, result.stderr, result.returncode)
if result.returncode:
    raise RuntimeError
if path.exists("release"):
    shutil.rmtree("release")

lis = [["dist/SGAv3/_internal", "release/SGAv3/_internal"],
       ["dist/SGAv3/SGA.exe", "release/SGAv3/SGA.exe"],
       ["dist/SGAv3/SGA-c.exe", "release/SGAv3/SGA-c.exe"],
       ["ocr-json", "release/SGAv3/ocr-json"],
       ["resources", "release/SGAv3/resources"],
       ["update.txt", "release/SGAv3/update.txt"],
       ["readme.md", "release/SGAv3/readme.md"],
       ["mdpic", "release/SGAv3/mdpic"]
       ]
# shutil.copytree("dist/SGAv3", "release/SGAv3")
for src, drc in lis:
    if path.isdir(src):
        shutil.copytree(src, drc)
    else:
        shutil.copyfile(src, drc)
chdir("release")
rar_path = "D:/Program Files/WinRAR/WinRAR.exe"
version = "3.0.2"
cmdline = [rar_path,
           "a",
           f"SGAv3-{version}-full.rar", "SGAv3"]
result = subprocess.run(cmdline, shell=True, capture_output=True, text=True)
print("stdout1, stderr1, 返回码:", result.stdout, result.stderr, result.returncode)
shutil.rmtree("SGAv3/ocr-json")
cmdline = [rar_path,
           "a",
           f"SGAv3-{version}-full-withoutOCR.rar", "SGAv3"]
result = subprocess.run(cmdline, shell=True, capture_output=True, text=True)
print("stdout2, stderr2, 返回码:", result.stdout, result.stderr, result.returncode)
if result.returncode:
    raise RuntimeError
chdir("..")
print("sgapack-full完成")
