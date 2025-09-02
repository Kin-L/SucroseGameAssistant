import winreg
from maincode.tools.core.logger import logger


def FindProgramPath(names, nametag="DisplayName", pathtag="DisplayIcon"):
    # 常见的注册表路径
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",  # 64位系统上的32位程序
    ]
    paths = []
    # 遍历注册表路径
    for reg_path in reg_paths:
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
            for i in range(0, winreg.QueryInfoKey(key)[0]):
                subkey_name = winreg.EnumKey(key, i)
                subkey = winreg.OpenKey(key, subkey_name)
                try:
                    display_name = winreg.QueryValueEx(subkey, nametag)[0]
                    # print(display_name)
                    for name in names:
                        if name.lower() in display_name.lower():
                            print(display_name)
                            install_path = winreg.QueryValueEx(subkey, pathtag)[0]
                            if install_path:
                                paths.append(install_path)
                except (WindowsError, FileNotFoundError):
                    continue
        except WindowsError as e:
            logger.warning(f"无法访问注册表路径 {reg_path}: {e}")
            continue
    return list(paths)
