import json
from os.path import exists, splitext
from os import listdir, makedirs, rename
from main.mainwindows import main_windows as mw
from main.tools.environment import env
from main.tools.logger import logger
from os import remove, path
from traceback import format_exc
from shutil import copyfile
from random import randint


# 设置锁定模式
def change_lock():
    if env.lock:
        mw.module.button_config_lock.hide()
        mw.module.button_config_unlock.show()
        mw.module.button_config_delete.setDisabled(False)
        mw.module.button_config_add.setDisabled(False)
        env.lock = False
    else:
        mw.module.button_config_unlock.hide()
        mw.module.button_config_lock.show()
        mw.module.button_config_delete.setDisabled(True)
        mw.module.button_config_add.setDisabled(True)
        env.lock = True
        mw.sendbox(mode=1)
        _text = mw.module.box_config_change.currentText()
        try:
            mw.module.load_module_config(read_config_dir(_text))
            mw.sendbox(f"载入配置:{_text}", mode=2)
        except Exception as e:
            logger.error("载入配置异常:\n%s\n" % format_exc())
            mw.sendbox(f"载入配置异常:{e}", mode=2)
        mw.sendbox(mode=3)


# 删除配置项
def delete_plan():
    # noinspection PyBroadException
    mw.sendbox(mode=1)
    try:
        _text = mw.module.box_config_change.currentText()
        _index = mw.module.box_config_change.currentIndex()
        _num = len(mw.module.box_config_change.items)
        if _num > 1:
            remove(f"personal/config/{_text}.json")
            config_index = env.config_name.index(_text)
            del env.config_name[config_index], env.config_type[config_index]
            mw.module.box_config_change.removeItem(_index)
            mw.sendbox(f"删除配置：{_text}", mode=2)
        else:
            mw.sendbox("删除配置失败：最少需要存在一项配置", mode=2)
    except Exception as e:
        logger.error("删除配置异常:\n%s\n" % format_exc())
        mw.sendbox(f"删除配置异常:{e}", mode=2)
    config_box_refresh()
    mw.sendbox(mode=3)


def read_config_dir(_text):
    _path = path.join(env.workdir, f"personal/config/{_text}.json")
    if path.exists(_path):
        with open(_path, 'r', encoding='utf-8') as c:
            config_dir = json.load(c)
    return config_dir


# 选择方案改变
def config_change():
    env.config = mw.module.box_config_change.currentText()
    if env.lock:
        mw.sendbox(mode=1)
        try:
            mw.module.load_module_config(read_config_dir(env.config))
            mw.sendbox(f"切换配置:{env.config}", mode=2)
        except Exception as e:
            logger.error("切换配置异常:\n%s\n" % format_exc())
            mw.sendbox(f"切换配置异常:{e}", mode=2)
        mw.sendbox(mode=3)


def config_box_refresh():
    env.config_name = []
    env.config_type = []
    # 获取设置及分类
    if not exists("personal/config"):
        makedirs("personal/config")
    _listdir = listdir("personal/config")
    if not _listdir:
        newname = "默认配置" + str(randint(999, 10000))
        copyfile(r"assets\main_window\default_config.json",
                 r"personal\config\%s.json" % newname)
        _listdir = listdir("personal/config")
    _dir = path.join(env.workdir, "personal/config")
    for file in listdir(_dir):
        name, suffix = splitext(file)
        if suffix == ".json":
            _path = path.join(_dir, file)
            # noinspection PyBroadException
            try:
                with open(_path, 'r', encoding='utf-8') as c:
                    _config = json.load(c)
                if _config["模块"] < len(env.name):
                    pass
                else:
                    continue
            except Exception:
                continue
            env.config_name += [name]
            env.config_type += [_config["模块"]]
    from main.ui.overall.timer.connect import timer_load_items
    timer_load_items(env.config_name)
    mw.module.box_config_change.disconnect()
    mw.module.box_config_change.clear()
    mw.module.box_config_change.addItems(env.config_name)
    mw.module.box_config_change.editingFinished.connect(config_rename)
    if env.load[0]:
        from main.ui.module.mix import mix_box_refresh
        mix_box_refresh(env.config_name)
    mw.sendbox("刷新配置栏", mode=2)


def config_box_add():
    mw.sendbox(mode=1)
    newname = "默认配置" + str(randint(999, 10000))
    copyfile(r"assets\main_window\default_config.json",
             r"personal\config\%s.json" % newname)
    _listdir = listdir("personal/config")
    mw.sendbox(f"新建配置：{newname}", mode=2)
    config_box_refresh()
    mw.sendbox(mode=3)


# 配置重命名
def config_rename():
    text_past = env.config
    text_now = mw.module.box_config_change.currentText()
    if text_now == text_past:
        pass
    else:

        new_path = f"personal/config/{text_now}.json"
        past_path = f"personal/config/{text_past}.json"
        if path.exists(past_path) and not path.exists(new_path):
            mw.sendbox(mode=1)
            rename(past_path, new_path)
            mw.sendbox("配置更名：%s >>> %s" % (text_past, text_now), 2)
            config_box_refresh()
            mw.sendbox(mode=3)
        env.config = text_now


# （加载并）切换模组设置页面
def change_module_stack():
    _num = mw.module.box_module_change.currentIndex()
    mw.module.load_module_config({"模块": _num})
    mw.module.stack_module.setCurrentIndex(_num)


# 保存当前界面设置信息
def save_config():
    mw.sendbox(mode=1)
    try:
        _dict = mw.module.collect_module_config()
        _text = mw.module.box_config_change.currentText()
        _path = path.join(env.workdir, f"personal/config/{_text}.json")
        with open(_path, 'w', encoding='utf-8') as c:
            json.dump(_dict, c, ensure_ascii=False, indent=1)
        mw.sendbox(f"保存配置：{_text}", 2)
    except Exception as e:
        logger.error("保存异常:\n%s\n" % format_exc())
        mw.sendbox(f"保存异常：{e}", 2)
    mw.sendbox(mode=3)
