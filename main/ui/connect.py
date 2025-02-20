from main.mainwindows import main_windows as mw
from main.tools.environment import env


def load_main_config():
    # 加载全局设置内容
    from main.ui.overall.timer.connect import timer_add_items, timer_load_set
    timer_add_items(env.config_name)
    timer_load_set(env.timer)
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
    if isinstance(env.current, dict):
        mw.module.load_module_config(env.current)
    # 运行路径变化时，基础文件初始化
    if env.workdir != env.current_work_path:
        pass


def function_connect():
    # 主面板操作
    from main.ui.mainwindow.connect import change_interface, open_log_dir
    from main.ui.module.connect import (change_lock, delete_plan, config_change,
                                        config_rename, config_box_add, change_module_stack,
                                        save_config)
    mw.main.button_set_home.toggled.connect(change_interface)
    mw.main.button_history.clicked.connect(open_log_dir)
    mw.module.button_config_lock.clicked.connect(change_lock)
    mw.module.button_config_unlock.clicked.connect(change_lock)
    mw.module.button_config_delete.clicked.connect(delete_plan)
    mw.module.box_config_change.currentIndexChanged.connect(config_change)
    mw.module.box_config_change.editingFinished.connect(config_rename)
    mw.module.button_config_add.clicked.connect(config_box_add)
    mw.module.box_module_change.currentIndexChanged.connect(change_module_stack)
    mw.module.button_config_save.clicked.connect(save_config)


def get_file_path(text):
    return "personal/config/%s.json" % (mw.state["plan"][text] + text)


def get_config_dir(text="current"):
    if text == "current":
        _num = mw.stack_module.currentIndex()
        _text = mw.state["name"][_num]
        module = eval(f"mw.{_text}")
        config_dir = module.output_config()
    else:
        with open(mw.get_file_path(text), 'r', encoding='utf-8') as c:
            config_dir = load(c)
    return config_dir


# 根据字典载入面板/根据字典和名称保存配置至文件
def send_config_dir(dictionary, text="current"):
    if text == "current":
        _num = dictionary["模块"]
        mw.change_module(_num)
        _text = mw.state["name"][_num]
        module = eval(f"mw.{_text}")
        module.input_config(dictionary)
    else:
        with open(mw.get_file_path(text), 'w', encoding='utf-8') as c:
            dump(dictionary, c, ensure_ascii=False, indent=1)


# 保存主设置
def save_main_data(mw):
    mw.config["timer"] = mw.overall.timer.save_set()
    mw.config["config"] = mw.state["text"]
    mw.config["lock"] = mw.state["locked"]
    mw.config["current"] = mw.get_config_dir()
    mw.config["update"] = mw.overall.auto_update.isChecked()
    for text in mw.state["name"][1:]:
        if mw.state[text]["load"]:
            module = eval(f"mw.{text}")
            mw.config[text] = module.get_run()
    with open("personal/main_config.json", 'w', encoding='utf-8') as c:
        dump(mw.config, c, ensure_ascii=False, indent=1)
    with open("personal/main_config_bak.json", 'w', encoding='utf-8') as c:
        dump(mw.config, c, ensure_ascii=False, indent=1)

def exit_save(mw):
    mw.save_main_data()
    while 1:
        v = get_pid("PaddleOCR-json.exe")
        if v:
            close(v)
        else:
            break

def add_path(config_dir):
    _name = mw.state["name"][config_dir["模块"]]
    config_dir["启动"] = mw.config[_name]
    return config_dir

# 获取运行信息
def get_config_run(text="current"):
    config_dir = mw.get_config_dir(text)
    if config_dir["模块"] == 0:
        for i in range(5):
            _name = config_dir["配置%s" % i]["name"]
            if _name == "<未选择>":
                continue
            else:
                _dir = mw.get_config_dir(_name)
                config_dir["配置%s" % i].update(mw.add_path(_dir))
    else:
        config_dir = mw.add_path(config_dir)
    return config_dir

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