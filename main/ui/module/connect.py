import json
from os.path import exists, splitext
from os import listdir, makedirs, rename
from main.mainwindows import smw
from main.mainenvironment import sme
from main.tools.logger import logger
from os import remove, path
from traceback import format_exc
from shutil import copyfile
from random import randint


# 设置锁定模式
def change_lock():
    if sme.lock:
        smw.module.button_config_lock.hide()
        smw.module.button_config_unlock.show()
        smw.module.button_config_delete.setDisabled(False)
        smw.module.button_config_add.setDisabled(False)
        sme.lock = False
    else:
        smw.module.button_config_unlock.hide()
        smw.module.button_config_lock.show()
        smw.module.button_config_delete.setDisabled(True)
        smw.module.button_config_add.setDisabled(True)
        sme.lock = True
        smw.sendbox(mode=1)
        _text = smw.module.box_config_change.currentText()
        try:
            smw.module.load_module_config(read_config_dir(_text))
            smw.sendbox(f"载入配置:{_text}", mode=2)
        except Exception as e:
            logger.error("载入配置异常:\n%s\n" % format_exc())
            smw.sendbox(f"载入配置异常:{e}", mode=2)
        smw.sendbox(mode=3)


# 删除配置项
def delete_plan():
    # noinspection PyBroadException
    smw.sendbox(mode=1)
    try:
        _text = smw.module.box_config_change.currentText()
        _index = smw.module.box_config_change.currentIndex()
        _num = len(smw.module.box_config_change.items)
        if _num > 1:
            remove(f"personal/config/{_text}.json")
            config_index = sme.config_name.index(_text)
            del sme.config_name[config_index], sme.config_type[config_index]
            smw.module.box_config_change.removeItem(_index)
            smw.sendbox(f"删除配置：{_text}", mode=2)
        else:
            smw.sendbox("删除配置失败：最少需要存在一项配置", mode=2)
    except Exception as e:
        logger.error("删除配置异常:\n%s\n" % format_exc())
        smw.sendbox(f"删除配置异常:{e}", mode=2)
    config_box_refresh()
    smw.sendbox(mode=3)


def read_config_dir(_text):
    _path = path.join(sme.workdir, f"personal/config/{_text}.json")
    if path.exists(_path):
        with open(_path, 'r', encoding='utf-8') as c:
            config_dir = json.load(c)
    return config_dir


# 选择方案改变
def config_change():
    sme.config = smw.module.box_config_change.currentText()
    if sme.lock:
        smw.sendbox(mode=1)
        try:
            smw.module.load_module_config(read_config_dir(sme.config))
            smw.sendbox(f"切换配置:{sme.config}", mode=2)
        except Exception as e:
            logger.error("切换配置异常:\n%s\n" % format_exc())
            smw.sendbox(f"切换配置异常:{e}", mode=2)
        smw.sendbox(mode=3)


def config_box_refresh():
    sme.config_name = []
    sme.config_type = []
    # 获取设置及分类
    if not exists("personal/config"):
        makedirs("personal/config")
    _listdir = listdir("personal/config")
    if not _listdir:
        newname = "默认配置" + str(randint(999, 10000))
        copyfile(r"assets\main_window\default_config.json",
                 r"personal\config\%s.json" % newname)
        _listdir = listdir("personal/config")
    _dir = path.join(sme.workdir, "personal/config")
    for file in listdir(_dir):
        name, suffix = splitext(file)
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
    from main.ui.overall.timer.connect import timer_box_refresh
    timer_box_refresh(sme.config_name)
    smw.module.box_config_change.disconnect()
    smw.module.box_config_change.clear()
    smw.module.box_config_change.addItems(sme.config_name)
    smw.module.box_config_change.editingFinished.connect(config_rename)
    if sme.load[0]:
        from main.ui.module.mix import mix_box_refresh
        mix_box_refresh()
    smw.sendbox("刷新配置栏", mode=2)


def config_box_add():
    smw.sendbox(mode=1)
    newname = "默认配置" + str(randint(999, 10000))
    copyfile(r"assets\main_window\default_config.json",
             r"personal\config\%s.json" % newname)
    _listdir = listdir("personal/config")
    smw.sendbox(f"新建配置：{newname}", mode=2)
    config_box_refresh()
    smw.sendbox(mode=3)


# 配置重命名
def config_rename():
    text_past = sme.config
    text_now = smw.module.box_config_change.currentText()
    if text_now == text_past:
        pass
    else:

        new_path = f"personal/config/{text_now}.json"
        past_path = f"personal/config/{text_past}.json"
        if path.exists(past_path) and not path.exists(new_path):
            smw.sendbox(mode=1)
            rename(past_path, new_path)
            smw.sendbox("配置更名：%s >>> %s" % (text_past, text_now), 2)
            config_box_refresh()
            smw.sendbox(mode=3)
        sme.config = text_now


# （加载并）切换模组设置页面
def change_module_stack():
    _num = smw.module.box_module_change.currentIndex()
    smw.module.load_module_window(_num)


# 保存当前界面设置信息
def save_config():
    smw.sendbox(mode=1)
    try:
        _dict = smw.module.collect_module_config()
        _text = smw.module.box_config_change.currentText()
        _path = path.join(sme.workdir, f"personal/config/{_text}.json")
        with open(_path, 'w', encoding='utf-8') as c:
            json.dump(_dict, c, ensure_ascii=False, indent=1)
        smw.sendbox(f"保存配置：{_text}", 2)
    except Exception as e:
        logger.error("保存异常:\n%s\n" % format_exc())
        smw.sendbox(f"保存异常：{e}", 2)
    smw.sendbox(mode=3)
