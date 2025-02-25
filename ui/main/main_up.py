from .main_down import MainDown
from tools.environment import *
from traceback import format_exc
from shutil import copyfile
from random import randint
from os import remove, rename
from json import dump, load
from time import strftime
from subprocess import run as cmd_run
from datetime import timedelta, datetime


class MainUp(MainDown):
    def __init__(self):
        super().__init__()

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

    # 应用定时
    def apply_timer(self):
        self.indicate("", 1)
        try:
            with open(r"personal\schtasks_index.json", 'r', encoding='utf-8') as x:
                xml_dir = load(x)
            auto, awake = [], []
            for num in range(self.overall.timer.time_item):
                daily = eval("self.overall.timer.execute%s" % num).currentIndex()
                _text = eval("self.overall.timer.text%s" % num).currentIndex()
                _awake = eval("self.overall.timer.awake%s" % num).isChecked()
                if daily and _text != "<未选择>":
                    if daily == 1:
                        _item = xml_dir["daily"]
                    else:
                        _item = xml_dir["weekly"]
                        week = \
                            ["", "", "Monday", "Tuesday", "Wednesday", "Thursday",
                             "Friday", "Saturday", "Sunday"][daily]
                        _item[5] = "          <" + week + " />\n"
                    _str = eval("self.overall.timer.timer%s" % num).getTime().toString()
                    pydatetime = datetime.strptime(_str, "%H:%M:%S") - timedelta(minutes=2)
                    wake_time = strftime("%H:%M", pydatetime.timetuple())
                    _item[1] = f"      <StartBoundary>2023-09-20T{wake_time}</StartBoundary>\n"
                    if _awake:
                        awake += _item
                    else:
                        auto += _item
            if auto or awake:
                if auto:
                    _p2 = xml_dir["part2"]
                    _p2[22] = f"<WakeToRun>false</WakeToRun>"
                    auto = xml_dir["part1"] + auto + _p2
                    xml_path = r"cache\SGA-auto.xml"
                    f = open(xml_path, 'w', encoding='utf-16')
                    f.writelines(auto)
                    f.close()
                    cmd_run("schtasks.exe /create /tn SGA-auto /xml \"%s\" /f" % xml_path, shell=True)
                else:
                    cmd_run("schtasks.exe /DELETE /tn SGA-auto /f", shell=True)
                if awake:
                    _p2 = xml_dir["part2"]
                    _p2[22] = f"<WakeToRun>true</WakeToRun>"
                    awake = xml_dir["part1"] + awake + _p2
                    xml_path = r"cache\SGA-awake.xml"
                    f = open(xml_path, 'w', encoding='utf-16')
                    f.writelines(awake)
                    f.close()
                    cmd_run("schtasks.exe /create /tn SGA-awake /xml \"%s\" /f" % xml_path, shell=True)
                else:
                    cmd_run("schtasks.exe /DELETE /tn SGA-awake /f", shell=True)
                self.indicate("应用定时成功", 3)
            else:
                cmd_run("schtasks.exe /DELETE /tn SGA-auto /f", shell=True)
                cmd_run("schtasks.exe /DELETE /tn SGA-awake /f", shell=True)
                self.indicate("清除定时", 3)
        except Exception as e:
            logger.error("应用定时异常:\n%s\n" % format_exc())
            self.indicate(f"应用定时异常：{e}", 3, log=False)

    def timer_delete(self):
        self.indicate("", 1)
        cmd_run("schtasks.exe /DELETE /tn SGA-auto /f", shell=True)
        cmd_run("schtasks.exe /DELETE /tn SGA-awake /f", shell=True)
        self.indicate("清除定时", 3)
