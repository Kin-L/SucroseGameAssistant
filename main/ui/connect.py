from main.mainwindows import smw
from main.mainenvironment import sme
from os import listdir, makedirs, path
from random import randint
from shutil import copyfile
import json
from main.ui.overall.timer.connect import timer_dir_template
from main.ui.module.mix import mix_dir_template
_main_config_template = {
            "timer": timer_dir_template,
            "update": True,
            "lock": True,
            "config": "",
            "current": mix_dir_template,
            "current_work_path": "",
            "launch": {}
        }


def load_config_list():
    # 获取设置及分类
    if not path.exists("personal/config"):
        makedirs("personal/config")
    _listdir = listdir("personal/config")
    if not _listdir:
        newname = "默认配置" + str(randint(999, 10000))
        copyfile(r"assets\main_window\default_config.json",
                 r"personal\config\%s.json" % newname)
        _listdir = listdir("personal/config")
    _dir = path.join(sme.workdir, "personal/config")
    for file in listdir(_dir):
        name, suffix = path.splitext(file)
        if suffix == ".json":
            _path = path.join(_dir, file)
            # noinspection PyBroadException
            try:
                with open(_path, 'r', encoding='utf-8') as c:
                    _config = json.load(c)
                if _config["模块"] < len(sme.name):
                    pass
                else:
                    continue
            except Exception:
                continue
            sme.config_name += [name]
            sme.config_type += [_config["模块"]]
    # 加载配置列表box
    from main.ui.overall.timer.connect import timer_box_refresh
    timer_box_refresh(sme.config_name)
    smw.module.box_config_change.addItems(sme.config_name)


def read_config_file(_path):
    if path.exists(_path):
        # noinspection PyBroadException
        try:
            with open(_path, 'r', encoding='utf-8') as c:
                return True, json.load(c)
        except Exception:
            return True, None
    else:
        return False, None


def load_main_window_config(_config):
    from main.ui.overall.timer.connect import timer_load_set
    timer_load_set(_config["timer"])
    smw.overall.auto_update.setChecked(_config["update"])
    if _config["lock"]:
        smw.module.button_config_lock.show()
        smw.module.button_config_unlock.hide()
        smw.module.button_config_delete.setDisabled(True)
        smw.module.button_config_add.setDisabled(True)
    else:
        smw.module.button_config_lock.hide()
        smw.module.button_config_unlock.show()
    if _config["config"] in sme.config_name:
        smw.module.box_config_change.setCurrentText(_config["config"])
    else:
        smw.module.box_config_change.setCurrentIndex(0)
        _config["config"] = smw.module.box_config_change.currentText()
    smw.module.load_module_window(_config["current"]["模块"])
    smw.module.load_module_config(_config["current"])


def load_main_environment_config(_config):
    sme.timer = _config["timer"]
    sme.update = _config["update"]
    sme.lock = _config["lock"]
    sme.config = _config["config"]
    sme.current = _config["current"]
    sme.current_work_path = _config["current_work_path"]
    sme.launch = _config["launch"]


def basis_file_init():
    # 运行路径变化时，基础文件初始化
    if sme.workdir != sme.current_work_path:
        from os import makedirs, path
        from shutil import copyfile
        if not path.exists("cache"):
            makedirs("cache")
        if not path.exists("personal/script"):
            makedirs("personal/script")
        with open("assets/main_window/schtasks_index.json", 'r', encoding='utf-8') as m:
            xml_dir = json.load(m)
        xml_list = xml_dir["part2"]
        xml_list[32] = f"      <Command>{sme.workdir}\\SGA.exe</Command>\n"
        xml_list[34] = "      <WorkingDirectory>" + sme.workdir + "</WorkingDirectory>\n"
        xml_dir["part2"] = xml_list
        with open("personal/schtasks_index.json", 'w', encoding='utf-8') as x:
            json.dump(xml_dir, x, ensure_ascii=False, indent=1)

        f = open("assets/main_window/script/restart.bat", 'r', encoding='utf-8')
        start_list = f.readlines()
        f.close()
        start_list[2] = "start /d \"%s\" SGA.exe\n" % sme.workdir
        f = open("personal/script/restart.bat", 'w', encoding='utf-8')
        f.writelines(start_list)
        f.close()

        f = open("assets/main_window/script/maa_create.bat", 'r', encoding='ansi')
        bat_list = f.readlines()
        f.close()
        bat_list[1] = f" cd. > \"{sme.workdir}/cache/maa_complete.txt\""
        f = open("personal/script/maa_create.bat", 'w', encoding='ansi')
        f.writelines(bat_list)
        f.close()

        if not path.exists("personal/script/restart.vbs"):
            copyfile(r"assets/main_window/script/restart.vbs",
                     "personal/script/restart.vbs")
        if not path.exists("personal/script/start-SGA.vbs"):
            copyfile(r"assets/main_window/script/restart.vbs",
                     "personal/script/start-SGA.vbs")


def load_main_config():
    load_config_list()
    # noinspection PyBroadException
    try:
        _flag, _config = read_config_file(r"personal/main_config.json")
        if _flag:
            load_main_window_config(_config)
            with open("personal/main_config_bak.json", 'w', encoding='utf-8') as c:
                json.dump(_config, c, ensure_ascii=False, indent=1)
        else:
            load_main_window_config(_main_config_template)
            _config = _main_config_template
    except Exception:
        from traceback import format_exc
        print(format_exc())
        smw.sendbox(mode=1)
        # noinspection PyBroadException
        try:
            _config = read_config_file(r"personal/main_config_bak.json")
            load_main_window_config(_config)
            smw.indicate("主配置损坏，从备份恢复")
        except Exception:
            load_main_window_config(_main_config_template)
            smw.indicate("主配置损坏，进行重置")
            _config = _main_config_template
        smw.sendbox(mode=3)
    load_main_environment_config(_config)
    basis_file_init()


def function_connect():
    # 主面板操作
    from main.ui.mainwindow.connect import change_interface, open_log_dir, exit_prepare
    from main.ui.module.connect import (change_lock, delete_plan, config_change,
                                        config_rename, config_box_add, change_module_stack,
                                        save_config)
    from main.ui.overall.timer.connect import item_change, timer_delete, apply_timer
    from main.ui.overall.connect import update_check_change, open_update_history
    from webbrowser import open as weopen
    import atexit
    smw.main.button_set_home.toggled.connect(change_interface)
    smw.main.button_history.clicked.connect(open_log_dir)
    atexit.register(exit_prepare)
    smw.module.button_config_lock.clicked.connect(change_lock)
    smw.module.button_config_unlock.clicked.connect(change_lock)
    smw.module.button_config_delete.clicked.connect(delete_plan)
    smw.module.box_config_change.currentIndexChanged.connect(config_change)
    smw.module.box_config_change.editingFinished.connect(config_rename)
    smw.module.button_config_add.clicked.connect(config_box_add)
    smw.module.box_module_change.currentIndexChanged.connect(change_module_stack)
    smw.module.button_config_save.clicked.connect(save_config)

    smw.overall.button_github.clicked.connect(lambda: weopen("https://github.com/Kin-L/SucroseGameAssistant"))
    smw.overall.button_gitee.clicked.connect(lambda: weopen("https://gitee.com/huixinghen/SucroseGameAssistant"))
    smw.overall.button_bilibili.clicked.connect(lambda: weopen("https://space.bilibili.com/406315493"))
    smw.overall.auto_update.toggled.connect(update_check_change)
    smw.overall.button_update_history.clicked.connect(open_update_history)
    smw.overall.timer.add.clicked.connect(lambda: item_change(True))
    smw.overall.timer.deduce.clicked.connect(lambda: item_change(False))
    smw.overall.timer.delete.clicked.connect(timer_delete)
    smw.overall.timer.apply.clicked.connect(apply_timer)
    # 启动线程
    sme.thread_load()


def start(_task=None):
    # noinspection PyBroadException
    try:
        smw.cycle_thread.terminate()
        smw.save_main_data()
        smw.indicate("", 0)
        if _task:
            smw.task_thread = _task
        else:
            smw.task_thread = smw.get_config_run()
        smw.task_thread["name"] = ""
        smw.task_thread["current_mute"] = get_mute()
        if smw.task_thread["静音"] and not smw.task_thread["current_mute"]:
            change_mute()
        smw.box_info.clear()
        smw.indicate("", 1)
        smw.indicate("开始执行:实时计划")
        pixmap = QPixmap(r"assets\main_window\ui\ico\0.png")
        smw.label_status.setPixmap(pixmap)
        smw.button_pause.show()
        smw.button_start.hide()

        smw.kill.start()
        smw.sga_run.start()
    except Exception:
        logger.error("手动开始异常:\n%s\n" % format_exc())
        sysexit(1)

def pause(mw):
    # noinspection PyBroadException
    try:
        mw.state["wait_time"] = 5
        foreground(mw.state["hwnd"])
        # noinspection PyBroadException
        try:
            mw.sga_run.trigger.kill()
        except Exception:
            pass
        mw.sga_run.terminate()
        pixmap = QPixmap(r"assets/main_window/ui/ico/2.png")
        mw.indicate("手动终止", 3)
        sme.OCR.disable()
        mw.button_pause.hide()
        mw.button_start.show()
        mw.label_status.setPixmap(pixmap)
        mw.kill.terminate()
        mw.cycle_thread.start()
    except Exception:
        logger.error("手动终止线程异常:\n%s\n" % format_exc())
        sysexit(1)