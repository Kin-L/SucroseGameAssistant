from main.mainwindows import smw
from main.mainenvironment import sme

    
# 切换页面
def change_interface():
    if sme.setting:
        smw.main.stack_setting.setCurrentIndex(0)
        sme.setting = 0
    else:
        smw.main.stack_setting.setCurrentIndex(1)
        sme.setting = 1


def open_log_dir():
    from os import startfile
    startfile(sme.workdir + "/personal/logs")
    smw.sendbox(mode=1)
    smw.sendbox("打开日志文件夹")
    smw.sendbox(mode=3)


def save_env_data():
    import json
    _config = dict()
    _config["current_work_path"] = sme.current_work_path
    import copy
    _config["timer"] = copy.deepcopy(sme.timer)
    from time import strftime
    _time_list = []
    for i in sme.timer["time"]:
        _time_list += [strftime("%H:%M:%S", i)]
    _config["timer"]["time"] = _time_list
    _config["update"] = sme.update
    _config["lock"] = sme.lock
    _config["config"] = sme.config
    _config["current"] = sme.current
    _config["ocrpath"] = sme.ocrdir
    _config["launch"] = sme.launch
    with open("personal/main_config.json", 'w', encoding='utf-8') as c:
        json.dump(_config, c, ensure_ascii=False, indent=1)


# 全局设置:退出前保存 & 每10秒自动保存
def exit_prepare():
    from main.tools.system import get_pid, close
    sme.current = smw.module.collect_module_config()
    save_env_data()
    if sme.cpu_feature:
        _ocr_name = "PaddleOCR-json.exe"
    else:
        _ocr_name = "RapidOCR-json.exe"
    while 1:
        if v := get_pid(_ocr_name):
            close(v)
        else:
            break
