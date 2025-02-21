from main.mainwindows import main_windows as mw
from main.tools.environment import env

    
# 切换页面
def change_interface():
    if env.setting:
        mw.main.stack_setting.setCurrentIndex(0)
        env.setting = 0
    else:
        mw.main.stack_setting.setCurrentIndex(1)
        env.setting = 1


def open_log_dir():
    from os import startfile
    startfile(env.workdir + "/personal/logs")
    mw.sendbox(mode=1)
    mw.sendbox("打开日志文件夹")
    mw.sendbox(mode=3)


def save_env_data():
    import json
    _config = dict()
    _config["current_work_path"] = env.current_work_path
    _config["timer"] = env.timer
    _config["update"] = env.update
    _config["lock"] = env.lock
    _config["config"] = env.config
    _config["current"] = env.current
    _config["launch"] = env.launch
    with open("personal/main_config.json", 'w', encoding='utf-8') as c:
        json.dump(_config, c, ensure_ascii=False, indent=1)


# 全局设置:退出前保存 & 每10秒自动保存
def exit_prepare():
    from main.tools.system import get_pid, close
    env.current = mw.module.collect_module_config()
    save_env_data()
    if env.cpu_feature:
        _ocr_name = "PaddleOCR-json.exe"
    else:
        _ocr_name = "RapidOCR-json.exe"
    while 1:
        if v := get_pid(_ocr_name):
            close(v)
        else:
            break
