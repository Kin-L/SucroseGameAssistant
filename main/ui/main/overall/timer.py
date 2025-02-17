from PyQt5.QtCore import QTime


class Timer:
    def __init__(self):
        self.add.clicked.connect(lambda: self.item_change(True))
        self.deduce.clicked.connect(lambda: self.item_change(False))

    def item_change(self, add):
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

    def add_items(self, filelist):
        # 加载已有方案选项
        self.text0.addItems(filelist)
        self.text1.addItems(filelist)
        self.text2.addItems(filelist)
        self.text3.addItems(filelist)
        self.text4.addItems(filelist)
        self.text5.addItems(filelist)
        self.text6.addItems(filelist)
        self.text7.addItems(filelist)
        self.text8.addItems(filelist)
        self.text9.addItems(filelist)

    def load_set(self, _dir):
        timer_dir = {
                "item_num": 3,
                "execute0": 1,
                "execute1": 1,
                "execute2": 1,
                "execute3": 0,
                "execute4": 0,
                "execute5": 0,
                "execute6": 0,
                "execute7": 0,
                "execute8": 0,
                "execute9": 0,
                "time0": "06:30:00",
                "time1": "12:30:00",
                "time2": "21:30:00",
                "time3": "23:35:00",
                "time4": "11:07:00",
                "time5": "11:07:00",
                "time6": "11:07:00",
                "time7": "11:07:00",
                "time8": "11:08:00",
                "time9": "11:08:00",
                "text0": "<未选择>",
                "text1": "<未选择>",
                "text2": "<未选择>",
                "text3": "<未选择>",
                "text4": "<未选择>",
                "text5": "<未选择>",
                "text6": "<未选择>",
                "text7": "<未选择>",
                "text8": "<未选择>",
                "text9": "<未选择>",
                "awake0": True,
                "awake1": True,
                "awake2": True,
                "awake3": True,
                "awake4": True,
                "awake5": True,
                "awake6": True,
                "awake7": True,
                "awake8": True,
                "awake9": True,
            }
        timer_dir.update(_dir)
        # 加载定时设置
        self.time_item = timer_dir["item_num"]
        self.widget.setFixedHeight(40 * self.time_item)
        self.execute0.setCurrentIndex(timer_dir["execute0"])
        self.execute1.setCurrentIndex(timer_dir["execute1"])
        self.execute2.setCurrentIndex(timer_dir["execute2"])
        self.execute3.setCurrentIndex(timer_dir["execute3"])
        self.execute4.setCurrentIndex(timer_dir["execute4"])
        self.execute5.setCurrentIndex(timer_dir["execute5"])
        self.execute6.setCurrentIndex(timer_dir["execute6"])
        self.execute7.setCurrentIndex(timer_dir["execute7"])
        self.execute8.setCurrentIndex(timer_dir["execute8"])
        self.execute9.setCurrentIndex(timer_dir["execute9"])
        self.timer0.setTime(QTime.fromString(timer_dir["time0"]))
        self.timer1.setTime(QTime.fromString(timer_dir["time1"]))
        self.timer2.setTime(QTime.fromString(timer_dir["time2"]))
        self.timer3.setTime(QTime.fromString(timer_dir["time3"]))
        self.timer4.setTime(QTime.fromString(timer_dir["time4"]))
        self.timer5.setTime(QTime.fromString(timer_dir["time5"]))
        self.timer6.setTime(QTime.fromString(timer_dir["time6"]))
        self.timer7.setTime(QTime.fromString(timer_dir["time7"]))
        self.timer8.setTime(QTime.fromString(timer_dir["time8"]))
        self.timer9.setTime(QTime.fromString(timer_dir["time9"]))
        self.text0.setCurrentText(timer_dir["text0"])
        self.text1.setCurrentText(timer_dir["text1"])
        self.text2.setCurrentText(timer_dir["text2"])
        self.text3.setCurrentText(timer_dir["text3"])
        self.text4.setCurrentText(timer_dir["text4"])
        self.text5.setCurrentText(timer_dir["text5"])
        self.text6.setCurrentText(timer_dir["text6"])
        self.text7.setCurrentText(timer_dir["text7"])
        self.text8.setCurrentText(timer_dir["text8"])
        self.text9.setCurrentText(timer_dir["text9"])
        self.awake0.setChecked(timer_dir["awake0"])
        self.awake1.setChecked(timer_dir["awake1"])
        self.awake2.setChecked(timer_dir["awake2"])
        self.awake3.setChecked(timer_dir["awake3"])
        self.awake4.setChecked(timer_dir["awake4"])
        self.awake5.setChecked(timer_dir["awake5"])
        self.awake6.setChecked(timer_dir["awake6"])
        self.awake7.setChecked(timer_dir["awake7"])
        self.awake8.setChecked(timer_dir["awake8"])
        self.awake9.setChecked(timer_dir["awake9"])

    def save_set(self):
        _dir = dict()
        _dir["item_num"] = self.time_item

        _dir["execute0"] = self.execute0.currentIndex()
        _dir["execute1"] = self.execute1.currentIndex()
        _dir["execute2"] = self.execute2.currentIndex()
        _dir["execute3"] = self.execute3.currentIndex()
        _dir["execute4"] = self.execute4.currentIndex()
        _dir["execute5"] = self.execute5.currentIndex()
        _dir["execute6"] = self.execute6.currentIndex()
        _dir["execute7"] = self.execute7.currentIndex()
        _dir["execute8"] = self.execute8.currentIndex()
        _dir["execute9"] = self.execute9.currentIndex()

        _dir["time0"] = self.timer0.getTime().toString()
        _dir["time1"] = self.timer1.getTime().toString()
        _dir["time2"] = self.timer2.getTime().toString()
        _dir["time3"] = self.timer3.getTime().toString()
        _dir["time4"] = self.timer4.getTime().toString()
        _dir["time5"] = self.timer5.getTime().toString()
        _dir["time6"] = self.timer6.getTime().toString()
        _dir["time7"] = self.timer7.getTime().toString()
        _dir["time8"] = self.timer8.getTime().toString()
        _dir["time9"] = self.timer9.getTime().toString()

        _dir["text0"] = self.text0.currentText()
        _dir["text1"] = self.text1.currentText()
        _dir["text2"] = self.text2.currentText()
        _dir["text3"] = self.text3.currentText()
        _dir["text4"] = self.text4.currentText()
        _dir["text5"] = self.text5.currentText()
        _dir["text6"] = self.text6.currentText()
        _dir["text7"] = self.text7.currentText()
        _dir["text8"] = self.text8.currentText()
        _dir["text9"] = self.text9.currentText()

        _dir["awake0"] = self.awake0.isChecked()
        _dir["awake1"] = self.awake1.isChecked()
        _dir["awake2"] = self.awake2.isChecked()
        _dir["awake3"] = self.awake3.isChecked()
        _dir["awake4"] = self.awake4.isChecked()
        _dir["awake5"] = self.awake5.isChecked()
        _dir["awake6"] = self.awake6.isChecked()
        _dir["awake7"] = self.awake7.isChecked()
        _dir["awake8"] = self.awake8.isChecked()
        _dir["awake9"] = self.awake9.isChecked()
        return _dir

    def delete_overall_plan(self, config_index):
        self.text0.removeItem(config_index)
        self.text1.removeItem(config_index)
        self.text2.removeItem(config_index)
        self.text3.removeItem(config_index)
        self.text4.removeItem(config_index)
        self.text5.removeItem(config_index)
        self.text6.removeItem(config_index)
        self.text7.removeItem(config_index)
        self.text8.removeItem(config_index)
        self.text9.removeItem(config_index)

    def overall_add_item(self, name):
        self.text0.addItem(name)
        self.text1.addItem(name)
        self.text2.addItem(name)
        self.text3.addItem(name)
        self.text4.addItem(name)
        self.text5.addItem(name)
        self.text6.addItem(name)
        self.text7.addItem(name)
        self.text8.addItem(name)
        self.text9.addItem(name)

    def overall_rename_item(self, old_name, new_name):
        self.text0.rename(old_name, new_name)
        self.text1.rename(old_name, new_name)
        self.text2.rename(old_name, new_name)
        self.text3.rename(old_name, new_name)
        self.text4.rename(old_name, new_name)
        self.text5.rename(old_name, new_name)
        self.text6.rename(old_name, new_name)
        self.text7.rename(old_name, new_name)
        self.text8.rename(old_name, new_name)
        self.text9.rename(old_name, new_name)
