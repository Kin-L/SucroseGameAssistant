from maincode.tools.main import CmdRun
from maincode.main.maingroup import sg
import json


def subtract_minute(time_list):
    hour, minute = time_list
    if minute == 0:
        return f"{hour - 1:02d}:{59:02d}" if hour > 0 else [23, 59]
    else:
        return f"{hour:02d}:{minute - 1:02d}"


def timer_delete():
    CmdRun("schtasks.exe /DELETE /tn SGA-auto /f")
    CmdRun("schtasks.exe /DELETE /tn SGA-awake /f")


def ApplyTimer():
    with open("personal/schtasks.json", 'r', encoding='utf-8') as x:
        xml_dir = json.load(x)
    autos, awakes = [], []
    timerconfig = sg.mainconfig.TimerConfig.model_dump()
    l1, l2, l3, l4 = timerconfig['Execute'], timerconfig['Time'], timerconfig['ConfigKeys'], timerconfig['Awake']
    for daily, time, filekey, awake in list(zip(l1, l2, l3, l4)):
        if daily and filekey:
            if daily == 1:
                _item = xml_dir["daily"]
            else:
                _item = xml_dir["weekly"]
                week = \
                    ["", "", "Monday", "Tuesday", "Wednesday", "Thursday",
                     "Friday", "Saturday", "Sunday"][daily]
                _item[5] = "          <" + week + " />\n"
            wake_time = subtract_minute(time)
            _item[1] = f"      <StartBoundary>2023-09-20T{wake_time}</StartBoundary>\n"
            if awake:
                awakes += _item
            else:
                autos += _item
    if autos or awakes:
        if autos:
            _p2 = xml_dir["part2"]
            _p2[22] = f"<WakeToRun>false</WakeToRun>"
            autos = xml_dir["part1"] + autos + _p2
            xml_path = r"cache/SGA-auto.xml"
            f = open(xml_path, 'w', encoding='utf-16')
            f.writelines(autos)
            f.close()
            CmdRun("schtasks.exe /create /tn SGA-auto /xml \"%s\" /f" % xml_path)
        else:
            CmdRun("schtasks.exe /DELETE /tn SGA-auto /f")
        if awakes:
            _p2 = xml_dir["part2"]
            _p2[22] = f"<WakeToRun>true</WakeToRun>"
            awakes = xml_dir["part1"] + awakes + _p2
            xml_path = r"cache/SGA-awake.xml"
            f = open(xml_path, 'w', encoding='utf-16')
            f.writelines(awakes)
            f.close()
            CmdRun("schtasks.exe /create /tn SGA-awake /xml \"%s\" /f" % xml_path)
        else:
            CmdRun("schtasks.exe /DELETE /tn SGA-awake /f")
        return True
    else:
        timer_delete()
        return False
