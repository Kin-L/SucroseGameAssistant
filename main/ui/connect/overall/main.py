def check_timer(self):
    now_time = localtime()
    for num in range(self.overall.timer.time_item):
        execute = eval("self.overall.timer.execute%s" % num).currentIndex()
        time_str = eval("self.overall.timer.timer%s" % num).getTime().toString()
        timetuple = datetime.strptime(time_str, "%H:%M:%S").timetuple()
        if execute in [now_time[6] + 2, 1]:
            if now_time[3:5] == timetuple[3:5]:
                _text = eval("self.overall.timer.text%s" % num).currentText()
                if _text != "<未选择>":
                    return _text
    return None

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
                cmd_run("schtasks.exe /create /tn SGA-awake /xml \"%s\" /f" % xml_path)
            else:
                cmd_run("schtasks.exe /DELETE /tn SGA-awake /f")
            self.indicate("应用定时成功", 3)
        else:
            cmd_run("schtasks.exe /DELETE /tn SGA-auto /f")
            cmd_run("schtasks.exe /DELETE /tn SGA-awake /f")
            self.indicate("清除定时", 3)
    except Exception as e:
        logger.error("应用定时异常:\n%s\n" % format_exc())
        self.indicate(f"应用定时异常：{e}", 3, log=False)

def timer_delete(self):
    self.indicate("", 1)
    cmd_run("schtasks.exe /DELETE /tn SGA-auto /f")
    cmd_run("schtasks.exe /DELETE /tn SGA-awake /f")
    self.indicate("清除定时", 3)

def check_update(self, mode=0):
    self.overall.button_check.setEnabled(False)
    self.indicate("检查更新中...")
    self.update.mode = mode
    self.update.start()

def load_update(self):
    self.overall.button_update.setEnabled(False)
    self.update.mode = 1
    self.update.start()