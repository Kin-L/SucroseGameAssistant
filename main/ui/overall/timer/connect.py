from PyQt5.QtCore import QTime
from main.mainwindows import main_windows as mw


def timer_load_set(_dir):
    _timer = mw.overall.timer
    timer_dir = {
        "item_num": 3,
        "execute": [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        "time": ["06:30:00", "12:30:00", "21:30:00", 
                 "23:35:00", "11:07:00", "11:07:00", 
                 "11:07:00", "11:07:00", "11:08:00", 
                 "11:08:00",],
        "text": ["<未选择>", "<未选择>", "<未选择>", 
                 "<未选择>", "<未选择>", "<未选择>", 
                 "<未选择>", "<未选择>", "<未选择>", 
                 "<未选择>"],
        "awake": [False, False, False,
                  False, False, False,
                  False, False, False,
                  False]
    }
    timer_dir.update(_dir)
    # 加载定时设置
    _timer.widget.setFixedHeight(40 * timer_dir["item_num"])
    _execute = timer_dir["execute"]
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
    _time = timer_dir["time"]
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
    _text = timer_dir["text"]
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
    _awake = timer_dir["awake"]
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
    _timer = mw.overall.timer
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


def timer_add_items(filelist):
    _filelist = ["<未选择>"] + filelist
    _timer = mw.overall.timer
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
        if self.time_item < 10:
            self.time_item += 1
            self.widget.setFixedHeight(40 * self.time_item)
        else:
            print("条目数达上限：10", self.time_item)
    else:
        if self.time_item > 3:
            self.time_item -= 1
            self.widget.setFixedHeight(40 * self.time_item)
        else:
            print("条目数达下限：3", self.time_item)