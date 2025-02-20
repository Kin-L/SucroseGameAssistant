from PyQt5.QtCore import QTime
from main.mainwindows import main_windows as mw
from main.tools.environment import env, logger
from subprocess import run as cmd_run
from time import localtime, strptime, strftime
_timer_dir = {
            "item_num": 3,
            "execute": [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
            "time": ["06:30:00", "12:30:00", "21:30:00",
                     "23:35:00", "11:07:00", "11:07:00",
                     "11:07:00", "11:07:00", "11:08:00",
                     "11:08:00", ],
            "text": ["<未选择>", "<未选择>", "<未选择>",
                     "<未选择>", "<未选择>", "<未选择>",
                     "<未选择>", "<未选择>", "<未选择>",
                     "<未选择>"],
            "awake": [False, False, False,
                      False, False, False,
                      False, False, False,
                      False]
        }
_timer = mw.overall.timer
_execute_list = [_timer.execute0, _timer.execute1,
                 _timer.execute2, _timer.execute3,
                 _timer.execute4, _timer.execute5,
                 _timer.execute6, _timer.execute7,
                 _timer.execute8, _timer.execute9]
_text_list = [_timer.text0, _timer.text1,
              _timer.text2, _timer.text3,
              _timer.text4, _timer.text5,
              _timer.text6, _timer.text7,
              _timer.text8, _timer.text9]
_awake_list = [_timer.awake0, _timer.awake1,
               _timer.awake2, _timer.awake3,
               _timer.awake4, _timer.awake5,
               _timer.awake6, _timer.awake7,
               _timer.awake8, _timer.awake9]
_timer_list = [_timer.timer0, _timer.timer1,
               _timer.timer2, _timer.timer3,
               _timer.timer4, _timer.timer5,
               _timer.timer6, _timer.timer7,
               _timer.timer8, _timer.timer9]


def timer_load_set(_dir=None):
    if not _dir:
        _dir = _timer_dir
    # 加载定时设置
    _timer.widget.setFixedHeight(40 * _dir["item_num"])
    _execute = _dir["execute"]
    _timer.execute0.setCurrentIndex(_execute[0])
    _timer.execute1.setCurrentIndex(_execute[1])
    _timer.execute2.setCurrentIndex(_execute[2])
    _timer.execute3.setCurrentIndex(_execute[3])
    _timer.execute4.setCurrentIndex(_execute[4])
    _timer.execute5.setCurrentIndex(_execute[5])
    _timer.execute6.setCurrentIndex(_execute[6])
    _timer.execute7.setCurrentIndex(_execute[7])
    _timer.execute8.setCurrentIndex(_execute[8])
    _timer.execute9.setCurrentIndex(_execute[9])
    _time = _dir["time"]
    _timer.timer0.setTime(QTime.fromString(_time[0]))
    _timer.timer1.setTime(QTime.fromString(_time[1]))
    _timer.timer2.setTime(QTime.fromString(_time[2]))
    _timer.timer3.setTime(QTime.fromString(_time[3]))
    _timer.timer4.setTime(QTime.fromString(_time[4]))
    _timer.timer5.setTime(QTime.fromString(_time[5]))
    _timer.timer6.setTime(QTime.fromString(_time[6]))
    _timer.timer7.setTime(QTime.fromString(_time[7]))
    _timer.timer8.setTime(QTime.fromString(_time[8]))
    _timer.timer9.setTime(QTime.fromString(_time[9]))
    _text = _dir["text"]
    _timer.text0.setCurrentText(_text[0])
    _timer.text1.setCurrentText(_text[1])
    _timer.text2.setCurrentText(_text[2])
    _timer.text3.setCurrentText(_text[3])
    _timer.text4.setCurrentText(_text[4])
    _timer.text5.setCurrentText(_text[5])
    _timer.text6.setCurrentText(_text[6])
    _timer.text7.setCurrentText(_text[7])
    _timer.text8.setCurrentText(_text[8])
    _timer.text9.setCurrentText(_text[9])
    _awake = _dir["awake"]
    _timer.awake0.setChecked(_awake[0])
    _timer.awake1.setChecked(_awake[1])
    _timer.awake2.setChecked(_awake[2])
    _timer.awake3.setChecked(_awake[3])
    _timer.awake4.setChecked(_awake[4])
    _timer.awake5.setChecked(_awake[5])
    _timer.awake6.setChecked(_awake[6])
    _timer.awake7.setChecked(_awake[7])
    _timer.awake8.setChecked(_awake[8])
    _timer.awake9.setChecked(_awake[9])


def timer_save_set():
    _dir = dict()
    _dir["item_num"] = _timer.time_item
    _dir["execute"] = [_timer.execute0.currentIndex(), _timer.execute1.currentIndex(), 
                       _timer.execute2.currentIndex(), _timer.execute3.currentIndex(), 
                       _timer.execute4.currentIndex(), _timer.execute5.currentIndex(), 
                       _timer.execute6.currentIndex(), _timer.execute7.currentIndex(), 
                       _timer.execute8.currentIndex(), _timer.execute9.currentIndex()]
    _dir["time"] = [_timer.timer0.getTime().toString(), _timer.timer1.getTime().toString(), 
                    _timer.timer2.getTime().toString(), _timer.timer3.getTime().toString(), 
                    _timer.timer4.getTime().toString(), _timer.timer5.getTime().toString(), 
                    _timer.timer6.getTime().toString(), _timer.timer7.getTime().toString(), 
                    _timer.timer8.getTime().toString(), _timer.timer9.getTime().toString()]
    _dir["text"] = [_timer.text0.currentText(), _timer.text1.currentText(), 
                    _timer.text2.currentText(), _timer.text3.currentText(), 
                    _timer.text4.currentText(), _timer.text5.currentText(), 
                    _timer.text6.currentText(), _timer.text7.currentText(), 
                    _timer.text8.currentText(), _timer.text9.currentText()]
    _dir["awake"] = [_timer.awake0.isChecked(), _timer.awake1.isChecked(), 
                     _timer.awake2.isChecked(), _timer.awake3.isChecked(), 
                     _timer.awake4.isChecked(), _timer.awake5.isChecked(), 
                     _timer.awake6.isChecked(), _timer.awake7.isChecked(), 
                     _timer.awake8.isChecked(), _timer.awake9.isChecked()]
    return _dir


def timer_load_items(filelist):
    _filelist = ["<未选择>"] + filelist
    # 加载已有方案选项
    _timer.text0.clear()
    _timer.text1.clear()
    _timer.text2.clear()
    _timer.text3.clear()
    _timer.text4.clear()
    _timer.text5.clear()
    _timer.text6.clear()
    _timer.text7.clear()
    _timer.text8.clear()
    _timer.text9.clear()
    _timer.text0.addItems(_filelist)
    _timer.text1.addItems(_filelist)
    _timer.text2.addItems(_filelist)
    _timer.text3.addItems(_filelist)
    _timer.text4.addItems(_filelist)
    _timer.text5.addItems(_filelist)
    _timer.text6.addItems(_filelist)
    _timer.text7.addItems(_filelist)
    _timer.text8.addItems(_filelist)
    _timer.text9.addItems(_filelist)


def item_change(add: bool):
    if add:
        if env.timer["item_num"] < 10:
            env.timer["item_num"] += 1
            mw.overall.timer.widget.setFixedHeight(40 * env.timer["item_num"])
        else:
            mw.sendbox(mode=1)
            mw.sendbox("条目数已达上限：10", mode=2)
            mw.sendbox(mode=3)
    else:
        if env.timer["item_num"] > 3:
            env.timer["item_num"] -= 1
            mw.overall.timer.widget.setFixedHeight(40 * env.timer["item_num"])
        else:
            mw.sendbox(mode=1)
            mw.sendbox("条目数达下限：3", mode=2)
            mw.sendbox(mode=3)


def check_timer():
    now_time = localtime()
    for num in range(env.timer["item_num"]):
        execute = _execute_list[num].currentIndex()
        time_str = _timer_list[num].getTime().toString()
        timetuple = strptime(time_str, "%H:%M:%S").timetuple()
        if execute in [now_time[6] + 2, 1]:
            if now_time[3:5] == timetuple[3:5]:
                _text = _text_list[num].currentText()
                if _text != "<未选择>":
                    return _text
    return 0


# 应用定时
def apply_timer():
    mw.sendbox(mode=1)
    try:
        import json
        from datetime import timedelta, datetime
        with open(r"personal\schtasks_index.json", 'r', encoding='utf-8') as x:
            xml_dir = json.load(x)
        auto, awake = [], []
        for num in range(env.timer["item_num"]):
            daily = _execute_list[num].currentIndex()
            _text = _text_list[num].currentIndex()
            _awake = _awake_list[num].isChecked()
            if daily and _text != "<未选择>":
                if daily == 1:
                    _item = xml_dir["daily"]
                else:
                    _item = xml_dir["weekly"]
                    week = \
                        ["", "", "Monday", "Tuesday", "Wednesday", "Thursday",
                         "Friday", "Saturday", "Sunday"][daily]
                    _item[5] = "          <" + week + " />\n"
                _str = _timer_list[num].getTime().toString()
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
                cmd_run("schtasks.exe /create /tn SGA-auto /xml \"%s\" /f" % xml_path)
            else:
                cmd_run("schtasks.exe /DELETE /tn SGA-auto /f")
            if awake:
                _p2 = xml_dir["part2"]
                _p2[22] = f"<WakeToRun>true</WakeToRun>"
                awake = xml_dir["part1"] + awake + _p2
                xml_path = r"cache\SGA-awake.xml"
                f = open(xml_path, 'w', encoding='utf-16')
                f.writelines(awake)
                f.close()
                cmd_run(f"schtasks.exe /create /tn SGA-awake /xml \"{xml_path}\" /f", shell=True)
            else:
                cmd_run("schtasks.exe /DELETE /tn SGA-awake /f", shell=True)
            mw.sendbox("更新定时任务，并应用唤醒", mode=2)
        else:
            cmd_run("schtasks.exe /DELETE /tn SGA-auto /f", shell=True)
            cmd_run("schtasks.exe /DELETE /tn SGA-awake /f", shell=True)
            mw.sendbox("取消唤醒", mode=2)
    except Exception as e:
        from traceback import format_exc
        logger.error("应用定时异常:\n%s\n" % format_exc())
        mw.sendbox(f"应用定时异常：{e}", mode=2)
    mw.sendbox(mode=3)


def timer_delete():
    mw.sendbox(mode=1)
    cmd_run("schtasks.exe /DELETE /tn SGA-auto /f", shell=True)
    cmd_run("schtasks.exe /DELETE /tn SGA-awake /f", shell=True)
    mw.sendbox("清除定时", mode=2)
    mw.sendbox(mode=3)
