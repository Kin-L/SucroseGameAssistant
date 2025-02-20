from main.mainwindows import main_windows as mw


def snow_input_config(_dir):
    _snow = mw.module.snow
    config = {
        "模块": 5,
        "预下载": False,
        "更新": False,
        "静音": False,
        "关闭软件": False,
        "完成后": 0,
        "SGA关闭": False,
        "账号选择": "",
        "功能0": False,
        "功能1": False,
        "功能2": False,
        "功能3": False,
        "功能4": False,
        "感知互赠": False,
        "每日配给": False,
        "使用试剂": False,
        "行动选择": 0,
        "后勤选择": "底比斯小队",
        "活动后勤选择": "明夷小队",
        "个人故事": [False, False, "未选择", "未选择", "未选择", "未选择"],
        "拟境扫荡": False,
        "商店购物": [False, "新手战斗记录", "初级职级认证"],
        "武器升级": False,
        "领取日常": False,
        "领取凭证": False,
        "活动每日": False,
        "共鸣记录": [False, False, False, False, False, False, False, False]
    }
    config.update(_dir)
    _snow.set.local.check_preload.setChecked(config["预下载"])
    _snow.set.local.check_update.setChecked(config["更新"])
    _snow.set.local.independent.check_mute.setChecked(config["静音"])
    _snow.set.local.independent.check_kill_game.setChecked(config["关闭软件"])
    _snow.set.local.independent.combo_after.setCurrentIndex(config["完成后"])
    _snow.set.local.independent.check_kill_sga.setChecked(config["SGA关闭"])
    _snow.set.local.line_account.setText(config["账号选择"])
    _snow.set.local.line_account.setSelection(0, 0)

    _snow.list.check_fight.setChecked(config["功能0"])
    _snow.list.check_daily.setChecked(config["功能1"])
    _snow.list.check_mail.setChecked(config["功能2"])
    _snow.list.check_roll.setChecked(config["功能3"])

    _snow.set.fight.check_share.setChecked(config["感知互赠"])
    _snow.set.fight.check_supply.setChecked(config["每日配给"])
    _snow.set.fight.check_reagent.setChecked(config["使用试剂"])
    _snow.set.fight.mat.setCurrentIndex(config["行动选择"])
    _snow.set.fight.logistics.setCurrentText(config["后勤选择"])
    _snow.set.fight.logistics1.setCurrentText(config["活动后勤选择"])

    _snow.set.daily.check_character.setChecked(config["个人故事"][0])
    _snow.set.daily.check_supplement.setChecked(config["个人故事"][1])
    _snow.set.daily.character1.setCurrentText(config["个人故事"][2])
    _snow.set.daily.character2.setCurrentText(config["个人故事"][3])
    _snow.set.daily.character3.setCurrentText(config["个人故事"][4])
    _snow.set.daily.character4.setCurrentText(config["个人故事"][5])

    _snow.set.daily.check_imitate.setChecked(config["拟境扫荡"])
    _snow.set.daily.check_market.setChecked(config["商店购物"][0])
    _snow.set.daily.box_market1.setCurrentText(config["商店购物"][1])
    _snow.set.daily.box_market2.setCurrentText(config["商店购物"][2])
    _snow.set.daily.check_weapon.setChecked(config["武器升级"])
    _snow.set.daily.check_daily.setChecked(config["领取日常"])
    _snow.set.daily.check_daily2.setChecked(config["领取凭证"])
    _snow.set.daily.check_daily3.setChecked(config["活动每日"])
    _snow.set.roll.check_roll0.setChecked(config["共鸣记录"][0])
    _snow.set.roll.check_roll1.setChecked(config["共鸣记录"][1])
    _snow.set.roll.check_roll2.setChecked(config["共鸣记录"][2])
    _snow.set.roll.check_roll3.setChecked(config["共鸣记录"][3])
    _snow.set.roll.check_roll4.setChecked(config["共鸣记录"][4])
    _snow.set.roll.check_roll5.setChecked(config["共鸣记录"][5])
    _snow.set.roll.check_roll6.setChecked(config["共鸣记录"][6])
    _snow.set.roll.check_opensheet.setChecked(config["共鸣记录"][7])


def snow_collect_config():
    _snow = mw.module.snow
    config = dict()
    config["模块"] = 5

    config["预下载"] = _snow.set.local.check_preload.isChecked()
    config["更新"] = _snow.set.local.check_update.isChecked()
    config["静音"] = _snow.set.local.independent.check_mute.isChecked()
    config["关闭软件"] = _snow.set.local.independent.check_kill_game.isChecked()
    config["完成后"] = _snow.set.local.independent.combo_after.currentIndex()
    config["SGA关闭"] = _snow.set.local.independent.check_kill_sga.isChecked()
    config["账号选择"] = _snow.set.local.line_account.text()

    config["功能0"] = _snow.list.check_fight.isChecked()
    config["功能1"] = _snow.list.check_daily.isChecked()
    config["功能2"] = _snow.list.check_mail.isChecked()
    config["功能3"] = _snow.list.check_roll.isChecked()

    config["感知互赠"] = _snow.set.fight.check_share.isChecked()
    config["每日配给"] = _snow.set.fight.check_supply.isChecked()
    config["使用试剂"] = _snow.set.fight.check_reagent.isChecked()
    config["行动选择"] = _snow.set.fight.mat.currentIndex()
    config["后勤选择"] = _snow.set.fight.logistics.currentText()
    config["活动后勤选择"] = _snow.set.fight.logistics1.currentText()
    config["个人故事"] = [
        _snow.set.daily.check_character.isChecked(),
        _snow.set.daily.check_supplement.isChecked(),
        _snow.set.daily.character1.currentText(),
        _snow.set.daily.character2.currentText(),
        _snow.set.daily.character3.currentText(),
        _snow.set.daily.character4.currentText()]
    config["拟境扫荡"] = _snow.set.daily.check_imitate.isChecked()
    config["商店购物"] = [
        _snow.set.daily.check_market.isChecked(),
        _snow.set.daily.box_market1.currentText(),
        _snow.set.daily.box_market2.currentText()]
    config["武器升级"] = _snow.set.daily.check_weapon.isChecked()
    config["领取日常"] = _snow.set.daily.check_daily.isChecked()
    config["领取凭证"] = _snow.set.daily.check_daily2.isChecked()
    config["活动每日"] = _snow.set.daily.check_daily3.isChecked()
    config["共鸣记录"] = [
        _snow.set.roll.check_roll0.isChecked(),
        _snow.set.roll.check_roll1.isChecked(),
        _snow.set.roll.check_roll2.isChecked(),
        _snow.set.roll.check_roll3.isChecked(),
        _snow.set.roll.check_roll4.isChecked(),
        _snow.set.roll.check_roll5.isChecked(),
        _snow.set.roll.check_roll6.isChecked(),
        _snow.set.roll.check_opensheet.isChecked()]
    return config
