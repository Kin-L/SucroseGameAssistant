
def get_file_path(self, text):
    return "personal/config/%s.json" % (self.state["plan"][text] + text)


def get_config_dir(self, text="current"):
    if text == "current":
        _num = self.stack_module.currentIndex()
        _text = self.state["name"][_num]
        module = eval(f"self.{_text}")
        config_dir = module.output_config()
    else:
        with open(self.get_file_path(text), 'r', encoding='utf-8') as c:
            config_dir = load(c)
    return config_dir


# 根据字典载入面板/根据字典和名称保存配置至文件
def send_config_dir(self, dictionary, text="current"):
    if text == "current":
        _num = dictionary["模块"]
        self.change_module(_num)
        _text = self.state["name"][_num]
        module = eval(f"self.{_text}")
        module.input_config(dictionary)
    else:
        with open(self.get_file_path(text), 'w', encoding='utf-8') as c:
            dump(dictionary, c, ensure_ascii=False, indent=1)

def load_main_config(self):
    self.config = {
        "work_path": "",
        "lock": True,
        "config": "",
        "genshin": {
            "server": 0,
            "game": "",
            "BGI": ""
        },
        "kleins": {
            "server": 0,
            "game": ""
        },
        "maa": {
            "maa_path": ""
        },
        "m7a": {
            "m7a_path": ""
        },
        "snow": {
            "server": 0,
            "snow_path": ""
        },
        "common": {},
        "presstrigger": {},
        "zzz": {},
        "update": False,
        "timer": {},
        "current": {"模块": 0}
    }
    self.state["version"] = self.overall.version
    self.state["hwnd"] = find_hwnd((True, "Qt5152QWindowIcon", "砂糖代理"))
    if exists("personal/main_config.json"):
        # noinspection PyBroadException
        try:
            with open("personal/main_config.json", 'r', encoding='utf-8') as c:
                config = load(c)
        except Exception:
            with open("personal/main_config_bak.json", 'r', encoding='utf-8') as c:
                config = load(c)
            with open("personal/main_config.json", 'w', encoding='utf-8') as c:
                dump(config, c, ensure_ascii=False, indent=1)
            self.indicate("主配置文件损坏,从备份中恢复")
        self.config.update(config)
    # 获取设置及分类
    if not exists("personal/config"):
        makedirs("personal/config")
    _listdir = listdir("personal/config")
    if not _listdir:
        newname = "默认配置" + str(randint(999, 10000))
        copyfile(r"assets\main_window\default_config.json",
                 r"personal\config\00%s.json" % newname)
        _listdir = listdir("personal/config")
    for file in listdir("personal/config"):
        name, suffix = splitext(file)
        if suffix == ".json":
            prefix = name[:2]
            name = name[2:]
            if prefix == "00":
                self.state["serial"] += [name]
            elif prefix in self.state["prefix"][1:]:
                self.state["single"] += [name]
            else:
                continue
            self.state["plan"][name] = prefix
    # 加载配置选框内容
    self.overall.timer.add_items(self.state["serial"] + self.state["single"])
    self.box_config_change.addItems(["点此项新建配置"] + self.state["serial"] + self.state["single"])
    self.change_module(0)
    # 加载模组设置
    self.overall.timer.load_set(self.config["timer"])
    self.overall.auto_update.setChecked(self.config["update"])
    self.stack_setting.setCurrentIndex(1)
    self.state["stack"] = 1
    _text = self.config["config"]
    # noinspection PyBroadException
    _num = self.box_config_change.count()
    config_list = []
    for i in range(1, _num):
        config_list += [self.box_config_change.itemText(i)]
    if _text in config_list:
        self.box_config_change.setCurrentText(_text)
        self.state["text"] = _text
        self.state["index"] = self.box_config_change.currentIndex()
    else:
        self.box_config_change.setCurrentIndex(1)
        self.state["index"] = 1
        self.state["text"] = self.box_config_change.currentText()
    self.set_lock(self.config["lock"])
    self.send_config_dir(self.config["current"])
    # 根据运行路径修改基础文件
    if env.workdir != self.config["work_path"]:
        if not exists("cache"):
            makedirs("cache")
        if not exists("personal/bat"):
            makedirs("personal/bat")
        self.config["work_path"] = env.workdir
        vbs_dir = "%s/personal/bat" % env.workdir
        vbs_path = "%s/personal/bat/start-SGA.vbs" % env.workdir
        with open("assets/main_window/schtasks_index.json", 'r', encoding='utf-8') as m:
            xml_dir = load(m)
        xml_list = xml_dir["part2"]
        xml_list[32] = "      <Command>" + vbs_path + "</Command>\n"
        xml_list[34] = "      <WorkingDirectory>" + vbs_dir + "</WorkingDirectory>\n"
        xml_dir["part2"] = xml_list
        with open("personal/schtasks_index.json", 'w', encoding='utf-8') as x:
            dump(xml_dir, x, ensure_ascii=False, indent=1)

        f = open("assets/main_window/bat_scr/start-SGA.bat", 'r', encoding='utf-8')
        start_list = f.readlines()
        f.close()
        start_list[5] = "start /d \"%s\" SGA.exe True\n" % env.workdir
        f = open("personal/bat/start-SGA.bat", 'w', encoding='utf-8')
        f.writelines(start_list)
        f.close()

        f = open("assets/main_window/bat_scr/restart.bat", 'r', encoding='utf-8')
        start_list = f.readlines()
        f.close()
        start_list[2] = "start /d \"%s\" SGA.exe\n" % env.workdir
        f = open("personal/bat/restart.bat", 'w', encoding='utf-8')
        f.writelines(start_list)
        f.close()

        f = open("assets/main_window/bat_scr/maa_create.bat", 'r', encoding='ansi')
        bat_list = f.readlines()
        f.close()
        bat_list[1] = f" cd. > \"{env.workdir}/cache/maa_complete.txt\""
        f = open("personal/bat/maa_create.bat", 'w', encoding='ansi')
        f.writelines(bat_list)
        f.close()

        if not exists("personal/bat/restart.vbs"):
            copyfile(r"assets/main_window/bat_scr/restart.vbs",
                     "personal/bat/restart.vbs")
        if not exists("personal/bat/start-SGA.vbs"):
            copyfile(r"assets/main_window/bat_scr/restart.vbs",
                     "personal/bat/start-SGA.vbs")

# 保存主设置
def save_main_data(self):
    self.config["timer"] = self.overall.timer.save_set()
    self.config["config"] = self.state["text"]
    self.config["lock"] = self.state["locked"]
    self.config["current"] = self.get_config_dir()
    self.config["update"] = self.overall.auto_update.isChecked()
    for text in self.state["name"][1:]:
        if self.state[text]["load"]:
            module = eval(f"self.{text}")
            self.config[text] = module.get_run()
    with open("personal/main_config.json", 'w', encoding='utf-8') as c:
        dump(self.config, c, ensure_ascii=False, indent=1)
    with open("personal/main_config_bak.json", 'w', encoding='utf-8') as c:
        dump(self.config, c, ensure_ascii=False, indent=1)

def exit_save(self):
    self.save_main_data()
    while 1:
        v = get_pid("PaddleOCR-json.exe")
        if v:
            close(v)
        else:
            break

def add_path(self, config_dir):
    _name = self.state["name"][config_dir["模块"]]
    config_dir["启动"] = self.config[_name]
    return config_dir

# 获取运行信息
def get_config_run(self, text="current"):
    config_dir = self.get_config_dir(text)
    if config_dir["模块"] == 0:
        for i in range(5):
            _name = config_dir["配置%s" % i]["name"]
            if _name == "<未选择>":
                continue
            else:
                _dir = self.get_config_dir(_name)
                config_dir["配置%s" % i].update(self.add_path(_dir))
    else:
        config_dir = self.add_path(config_dir)
    return config_dir

def thread_load(self):
    from multithread.cycle import Cycle
    from multithread.run import Kill, SGARun
    from multithread.update import Update
    self.cycle = Cycle(self)
    self.kill = Kill(self)
    self.sga_run = SGARun(self)
    self.update = Update(self)

def function_connect(self):
    # 主面板操作
    self.button_set_home.toggled.connect(self.change_interface)
    self.button_sponsor.clicked.connect(self.window_support.show)
    self.button_statement.clicked.connect(self.show_statement)
    self.button_instructions.clicked.connect(lambda: cmd_run("start "" Instructions.docx"))
    self.button_history.clicked.connect(lambda: cmd_run("start /d \"personal\" history.txt"))
    # 全局设置操作
    self.overall.timer.apply.clicked.connect(self.apply_timer)
    self.overall.button_check.clicked.connect(self.check_update)
    self.overall.button_update.clicked.connect(self.load_update)
    self.overall.timer.delete.clicked.connect(self.timer_delete)

    self.overall.button_update_history.clicked.connect(lambda: startfile(env.workdir + "/update_history.txt"))
    self.overall.button_logger.clicked.connect(lambda: startfile(env.workdir + "/personal/logs"))
    self.overall.button_github.clicked.connect(lambda: weopen("https://github.com/Kin-L/SucroseGameAssistant"))
    self.overall.button_gitee.clicked.connect(lambda: weopen("https://gitee.com/huixinghen/SucroseGameAssistant"))
    self.overall.button_bilibili.clicked.connect(lambda: weopen("https://space.bilibili.com/406315493"))
    # 配置操作
    self.button_config_delete.clicked.connect(self.delete_plan)
    self.box_config_change.currentIndexChanged.connect(self.config_change)
    self.box_config_change.editingFinished.connect(self.config_rename)
    self.button_config_lock.clicked.connect(lambda: self.set_config_lock(False))
    self.button_config_unlock.clicked.connect(lambda: self.set_config_lock(True))

    self.button_config_save.clicked.connect(self.save_config)
    self.button_start.clicked.connect(self.start)
    self.button_pause.clicked.connect(self.pause)
    # 切换面板
    self.box_module_change.currentIndexChanged.connect(self.change_module)
    # 信息输出
    self.kill.send.connect(self.indicate)
    self.sga_run.send.connect(self.indicate)
    self.cycle.send.connect(self.indicate)
    self.update.send.connect(self.indicate)

def start(self, _task=None):
    # noinspection PyBroadException
    try:
        self.cycle.terminate()
        self.save_main_data()
        self.indicate("", 0)
        if _task:
            self.task = _task
        else:
            self.task = self.get_config_run()
        self.task["name"] = ""
        self.task["current_mute"] = get_mute()
        if self.task["静音"] and not self.task["current_mute"]:
            change_mute()
        self.box_info.clear()
        self.indicate("", 1)
        self.indicate("开始执行:实时计划")
        pixmap = QPixmap(r"assets\main_window\ui\ico\0.png")
        self.label_status.setPixmap(pixmap)
        self.button_pause.show()
        self.button_start.hide()

        self.kill.start()
        self.sga_run.start()
    except Exception:
        logger.error("手动开始异常:\n%s\n" % format_exc())
        sysexit(1)

def pause(self):
    # noinspection PyBroadException
    try:
        self.state["wait_time"] = 5
        foreground(self.state["hwnd"])
        # noinspection PyBroadException
        try:
            self.sga_run.trigger.kill()
        except Exception:
            pass
        self.sga_run.terminate()
        pixmap = QPixmap(r"assets/main_window/ui/ico/2.png")
        self.indicate("手动终止", 3)
        env.OCR.disable()
        self.button_pause.hide()
        self.button_start.show()
        self.label_status.setPixmap(pixmap)
        self.kill.terminate()
        self.cycle.start()
    except Exception:
        logger.error("手动终止线程异常:\n%s\n" % format_exc())
        sysexit(1)