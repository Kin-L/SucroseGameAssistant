
# 配置重命名
def config_rename(self):
    text_past = self.state["text"]
    text_now = self.box_config_change.currentText()
    prefix = self.state["plan"][text_past]
    new_path = r"personal/config/%s.json" % (prefix + text_now)
    if text_now == text_past:
        pass
    elif text_now in self.state["plan"]:
        self.indicate("配置名重复：请键入其他名字", 3)
        self.box_config_change.setCurrentText(text_past)
    else:
        rename(r"personal/config/%s.json" % (prefix + text_past), new_path)
        self.overall.timer.overall_rename_item(text_past, text_now)
        if prefix != "00" and self.state["mix"]["load"]:
            self.mix.rename_item(text_past, text_now)
        self.state["plan"][text_now] = self.state["plan"].pop(text_past)
        self.state["text"] = text_now
        self.indicate("配置更名：%s >>> %s" % (text_past, text_now), 3)


# （加载并）切换模组设置页面
def change_module(self, num):
    name_list = self.state["name"]
    name = name_list[num]
    module = eval(f"self.{name}")
    if not self.state[name]["load"]:
        module = eval(f"self.{name}")
        module.load_window()

        if num == 0:
            module.load_single(self.state["single"])
        elif num < len(name_list):
            module.load_run(self.config[name])
        self.state[name]["load"] = True
    else:
        pass
    module.button.raise_()
    self.box_module_change.setCurrentIndex(num)
    self.stack_module.setCurrentIndex(num)

# 删除配置项
def delete_plan(self):
    # noinspection PyBroadException
    try:
        self.indicate("", 1)
        _text = self.box_config_change.currentText()
        _index = self.box_config_change.currentIndex()
        _num = len(self.box_config_change.items)
        if _num > 2:
            if _text in self.state["single"]:
                self.state["single"].remove(_text)
                if self.state["mix"]["load"]:
                    self.mix.remove_item(_text)
            elif _text in self.state["serial"]:
                self.state["serial"].remove(_text)
            self.overall.timer.delete_overall_plan(_index)
            remove(self.get_file_path(_text))
            if _index + 1 == _num:
                self.box_config_change.setCurrentIndex(_index-1)
                self.state["plan"].pop(_text)
                self.state["text"] = self.box_config_change.currentText()
                self.state["index"] = self.box_config_change.currentIndex()
            else:
                self.box_config_change.setCurrentIndex(_index+1)
                self.state["plan"].pop(_text)
                self.state["text"] = self.box_config_change.currentText()
                self.state["index"] = self.box_config_change.currentIndex()
            self.box_config_change.removeItem(_index)
            if self.state["locked"]:
                self.indicate("删除配置：" + _text)
                _dir = self.get_config_dir(self.state["text"])
                self.send_config_dir(_dir)
                self.indicate("载入配置：%s" % self.state["text"], 3)
            else:
                self.indicate("删除配置：" + _text, 3)
        else:
            self.indicate("删除配置失败：最少需要存在一项配置", 3)
    except Exception as e:
        logger.error("删除配置异常:\n%s\n" % format_exc())
        self.indicate(f"删除配置异常：{e}", 3, log=False)

# 选择方案改变 & 重命名 & 新建方案
def config_change(self):
    _index_now = self.box_config_change.currentIndex()
    # 新建方案
    if _index_now == 0:
        try:
            self.indicate("", 1)
            newname = "默认配置" + str(randint(999, 10000))
            copyfile(r"assets\main_window\default_config.json",
                     r"personal\config\00%s.json" % newname)
            # 更新方案列表
            self.state["plan"][newname] = "00"
            self.state["serial"] += [newname]
            self.box_config_change.addItem(newname)
            self.overall.timer.overall_add_item(newname)
        except Exception as e:
            logger.error("新建配置异常:\n%s\n" % format_exc())
            self.indicate(f"新建配置异常：{e}", 3, log=False)
            return 0
        try:
            # 加载配置
            if self.state["locked"]:
                self.indicate("新配置已创建：" + newname)
                _dir = self.get_config_dir(newname)
                self.send_config_dir(_dir)
                self.box_config_change.setCurrentText(newname)
                self.state["text"] = self.box_config_change.currentText()
                self.state["index"] = self.box_config_change.currentIndex()
                self.indicate("载入配置：" + newname, 3)
            else:
                self.box_config_change.setCurrentText(self.state["text"])
                self.indicate("新配置已创建：" + newname, 3)
        except Exception as e:
            logger.error("载入配置异常:\n%s\n" % format_exc())
            self.indicate(f"载入配置异常：{e}", 3, log=False)
    # 选择方案改变
    else:
        try:
            self.state["text"] = self.box_config_change.currentText()
            self.state["index"] = self.box_config_change.currentIndex()
            if self.state["locked"]:
                # 加载配置
                self.indicate("", 1)
                _dir = self.get_config_dir(self.state["text"])
                self.send_config_dir(_dir)
                self.indicate("载入配置：%s" % self.state["text"], 3)
        except Exception as e:
            logger.error("载入配置异常:\n%s\n" % format_exc())
            self.indicate(f"载入配置异常：{e}", 3, log=False)

# 设置锁定模式（并加载配置）
def set_config_lock(self, mode):
    self.set_lock(mode)
    if mode:
        _text = self.box_config_change.currentText()
        _dir = self.get_config_dir(_text)
        self.send_config_dir(_dir)

# 保存当前界面设置信息
def save_config(self):
    self.indicate("", 1)
    try:
        index_now = self.stack_module.currentIndex()
        text = self.box_config_change.currentText()
        prefix_past = self.state["plan"][text]
        name_past = prefix_past + text
        path = "personal/config/%s.json"
        if index_now == int(prefix_past):
            name_new = prefix_past + text
        else:
            new_prefix = self.state["prefix"][index_now]
            self.state["plan"][text] = new_prefix
            name_new = new_prefix + text
            rename(path % name_past, path % name_new)
            if prefix_past == "00" and index_now != 0:
                self.mix.add_item(text)
            else:
                self.mix.remove_item(name_past)
        with open(path % name_new, 'w', encoding='utf-8') as c:
            dump(self.get_config_dir(), c, ensure_ascii=False, indent=1)
        self.indicate("保存配置：%s" % text, 3)
    except Exception as e:
        logger.error("保存异常:\n%s\n" % format_exc())
        self.indicate(f"保存异常：{e}", 3, log=False)