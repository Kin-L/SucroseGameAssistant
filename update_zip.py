import os
import zipfile
import shutil
import json


def edit_version(_ver):
    with open("assets/main_window/version.json", 'r', encoding='utf-8') as m:
        _dir = json.load(m)
    if _ver != _dir["version"]:
        old_ver = _dir["version"]
        _dir["version"] = _ver
        with open("assets/main_window/version.json", 'w', encoding='utf-8') as x:
            json.dump(_dir, x, ensure_ascii=False, indent=1)
        print(f"版本号更新：{old_ver}>>>{_ver}")
    else:
        print(f"\033[1;33m版本号已存在：{_ver}\033[0m")


def copy_file(_file_dir, _ver, full):
    _cd1 = f"releases/SGA_{_ver}"
    if full:
        _cd2 = f"releases/SGA_{_ver}"
    else:
        _cd2 = f"releases/SGA_{_ver}/SGA_{_ver}"
    if os.path.exists(_cd1):
        shutil.rmtree(_cd1)
        print(f"\033[1;33m路径存在，进行清除覆盖：{_cd1}\033[0m")
    else:
        os.makedirs(_cd1)
    print("\033[1;32m文件复制中，请稍等...\033[0m")
    files = list(_file_dir.keys())
    for f in files:
        if os.path.exists(f):
            if _file_dir[f]:
                out_path = f"{_cd2}/{_file_dir[f]}/{os.path.split(f)[-1]}"
            else:
                out_path = f"{_cd2}/{os.path.split(f)[-1]}"
            if os.path.isfile(f):
                _d = os.path.split(out_path)[0]
                if not os.path.exists(_d):
                    os.makedirs(_d)
                shutil.copyfile(f, out_path)
            elif os.path.isdir(f):
                if os.path.exists(out_path):
                    shutil.rmtree(out_path)
                shutil.copytree(f, out_path)
            else:
                print(f"未知错误路径:{f}")
        else:
            print(f"未知错误路径:{f}")
    print(f"复制更新文件完成：{_cd1}")


def zip_folder(_ver, full):
    if full:
        dirpath = f"releases/SGA_{_ver}"
        out = f"releases/SGA_{_ver}.rar"
    else:
        dirpath = f"releases/SGA_{_ver}"
        out = f"releases/SGA_{_ver}.zip"
    if os.path.exists(out):
        os.remove(out)
        print(f"\033[1;33m文件存在，进行清除覆盖：{out}\033[0m")
    print("\033[1;32m打包中，请稍等...\033[0m")
    if full:
        # 本地WinRAR.exe地址
        rar_path = "\"D:/Program Files/WinRAR/WinRAR.exe\""
        os.chdir("releases")
        os.system(f"{rar_path} a  SGA_{_ver}.rar SGA_{_ver}")
        os.chdir("..")
    else:
        _zip = zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED)
        for path, dirnames, filenames in os.walk(dirpath):
            # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
            fpath = path.replace(dirpath, '')

            for filename in filenames:
                _zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        _zip.close()
    print(f"输出更新包：{out}")
    shutil.rmtree(dirpath)
    print(f"清除缓存文件夹：{dirpath}")


def pack(_d, _v, full=False):
    if full:
        _d = {
            "dist/SGA2.0-demo/_internal": "",
            "dist/SGA2.0-demo/SGA.exe": "",
            "Instructions.docx": "",
            "SGA快速上手.docx": "",
            "update_history.txt": "",
            "README.md": "",
            "assets": "",
            "multithread": "_internal",
            "tools": "_internal",
            "ui": "_internal",
            "task": "_internal"
        }
        _v = _v + "_full"
    else:
        _v = _v + "_replace"
    copy_file(_d, _v, full)
    zip_folder(_v, full)
    if full:
        print(f"\033[1;32mfull自动打包完成！\033[0m")
    else:
        print(f"\033[1;32mreplace自动打包完成！\033[0m")


# 更新包自动打包脚本
if __name__ == '__main__':
    _ver = "v2.3.2"
    file_dir = {
        "update_history.txt": "",
        # "README.md": "",
        "assets": "",
        # "assets/main_window/version.json": "",
        "multithread": "_internal",
        "tools": "_internal",
        "ui": "_internal",
        "task": "_internal"
    }
    edit_version(_ver)
    pack(file_dir, _ver.lstrip("v"),
         # full=True
         )
