from main.mainwindows import main_windows as mw
from main.tools.environment import env
import json


def load_main_config():
    # 加载全局设置内容
    from main.ui.overall.timer.connect import timer_load_items, timer_load_set
    timer_load_items(env.config_name)
    # noinspection PyBroadException
    try:
        timer_load_set(env.timer)
    except Exception:
        mw.indicate("定时配置损坏,进行重置")
        mw.sendbox(mode=3)
        env.main_config = {}
        timer_load_set()
    mw.overall.auto_update.setChecked(env.update)
    mw.overall.label_version.setText(env.version)
    # 加载模组设置
    mw.module.box_config_change.addItems(env.config_name)
    if env.config in env.config_name:
        mw.module.box_config_change.setCurrentText(env.config)
    else:
        mw.module.box_config_change.setCurrentIndex(0)
        env.config = mw.module.box_config_change.currentText()
    if env.lock:
        mw.module.button_config_lock.show()
        mw.module.button_config_unlock.hide()
        mw.module.button_config_delete.setDisabled(True)
        mw.module.button_config_add.setDisabled(True)
    else:
        mw.module.button_config_lock.hide()
        mw.module.button_config_unlock.show()
    # noinspection PyBroadException
    try:
        # noinspection PyBroadException
        try:
            num = env.current["模块"]
        except Exception:
            num = 0
        mw.module.load_module_window(num)
        mw.module.load_module_config(env.current)
    except Exception:
        mw.indicate("记忆配置损坏,进行重置")
        mw.sendbox(mode=3)
        env.main_config = {}
        mw.module.load_module_window(0)
        mw.module.load_module_config()
    if env.main_config:
        with open("personal/main_config_bak.json", 'w', encoding='utf-8') as c:
            json.dump(env.main_config, c, ensure_ascii=False, indent=1)
    # 运行路径变化时，基础文件初始化
    if env.workdir != env.current_work_path:
        basis_file_init()


def basis_file_init():
    from os import makedirs, path
    from shutil import copyfile
    if not path.exists("cache"):
        makedirs("cache")
    if not path.exists("personal/script"):
        makedirs("personal/script")
    with open("assets/main_window/schtasks_index.json", 'r', encoding='utf-8') as m:
        xml_dir = json.load(m)
    xml_list = xml_dir["part2"]
    xml_list[32] = f"      <Command>{env.workdir}\\SGA.exe</Command>\n"
    xml_list[34] = "      <WorkingDirectory>" + env.workdir + "</WorkingDirectory>\n"
    xml_dir["part2"] = xml_list
    with open("personal/schtasks_index.json", 'w', encoding='utf-8') as x:
        json.dump(xml_dir, x, ensure_ascii=False, indent=1)

    f = open("assets/main_window/script/restart.bat", 'r', encoding='utf-8')
    start_list = f.readlines()
    f.close()
    start_list[2] = "start /d \"%s\" SGA.exe\n" % env.workdir
    f = open("personal/script/restart.bat", 'w', encoding='utf-8')
    f.writelines(start_list)
    f.close()

    f = open("assets/main_window/script/maa_create.bat", 'r', encoding='ansi')
    bat_list = f.readlines()
    f.close()
    bat_list[1] = f" cd. > \"{env.workdir}/cache/maa_complete.txt\""
    f = open("personal/script/maa_create.bat", 'w', encoding='ansi')
    f.writelines(bat_list)
    f.close()

    if not path.exists("personal/script/restart.vbs"):
        copyfile(r"assets/main_window/script/restart.vbs",
                 "personal/script/restart.vbs")
    if not path.exists("personal/script/start-SGA.vbs"):
        copyfile(r"assets/main_window/script/restart.vbs",
                 "personal/script/start-SGA.vbs")


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
    mw.main.button_set_home.toggled.connect(change_interface)
    mw.main.button_history.clicked.connect(open_log_dir)
    atexit.register(exit_prepare)
    mw.module.button_config_lock.clicked.connect(change_lock)
    mw.module.button_config_unlock.clicked.connect(change_lock)
    mw.module.button_config_delete.clicked.connect(delete_plan)
    mw.module.box_config_change.currentIndexChanged.connect(config_change)
    mw.module.box_config_change.editingFinished.connect(config_rename)
    mw.module.button_config_add.clicked.connect(config_box_add)
    mw.module.box_module_change.currentIndexChanged.connect(change_module_stack)
    mw.module.button_config_save.clicked.connect(save_config)

    mw.overall.button_github.clicked.connect(lambda: weopen("https://github.com/Kin-L/SucroseGameAssistant"))
    mw.overall.button_gitee.clicked.connect(lambda: weopen("https://gitee.com/huixinghen/SucroseGameAssistant"))
    mw.overall.button_bilibili.clicked.connect(lambda: weopen("https://space.bilibili.com/406315493"))
    mw.overall.auto_update.toggled.connect(update_check_change)
    mw.overall.button_update_history.clicked.connect(open_update_history)
    mw.overall.timer.add.clicked.connect(lambda: item_change(True))
    mw.overall.timer.deduce.clicked.connect(lambda: item_change(False))
    mw.overall.timer.delete.clicked.connect(timer_delete)
    mw.overall.timer.apply.clicked.connect(apply_timer)


def thread_load(mw):
    from multithread.cycle import Cycle
    from multithread.run import Kill, SGARun
    from multithread.update import Update
    mw.cycle = Cycle(mw)
    mw.kill = Kill(mw)
    mw.sga_run = SGARun(mw)
    mw.update = Update(mw)


def start(_task=None):
    # noinspection PyBroadException
    try:
        mw.cycle.terminate()
        mw.save_main_data()
        mw.indicate("", 0)
        if _task:
            mw.task = _task
        else:
            mw.task = mw.get_config_run()
        mw.task["name"] = ""
        mw.task["current_mute"] = get_mute()
        if mw.task["静音"] and not mw.task["current_mute"]:
            change_mute()
        mw.box_info.clear()
        mw.indicate("", 1)
        mw.indicate("开始执行:实时计划")
        pixmap = QPixmap(r"assets\main_window\ui\ico\0.png")
        mw.label_status.setPixmap(pixmap)
        mw.button_pause.show()
        mw.button_start.hide()

        mw.kill.start()
        mw.sga_run.start()
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
        env.OCR.disable()
        mw.button_pause.hide()
        mw.button_start.show()
        mw.label_status.setPixmap(pixmap)
        mw.kill.terminate()
        mw.cycle.start()
    except Exception:
        logger.error("手动终止线程异常:\n%s\n" % format_exc())
        sysexit(1)