from maincode.tools.system.other import CmdRun
from maincode.config.configctrl import scc
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


def create_task(xml_content, task_name, wake_to_run):
    xml_dir = xml_content
    part2 = xml_dir["part2"].copy()
    part2[22] = f"<WakeToRun>{str(wake_to_run).lower()}</WakeToRun>"
    full_xml = xml_dir["part1"] + xml_content + part2
    xml_path = rf"cache/{task_name}.xml"
    try:
        with open(xml_path, 'w', encoding='utf-16') as f:
            f.writelines(full_xml)
        CmdRun(f'schtasks.exe /create /tn {task_name} /xml "{xml_path}" /f')
    except Exception as e:
        print(f"Failed to create task {task_name}: {e}")


def ApplyTimer():
    try:
        with open("personal/schtasks.json", 'r', encoding='utf-8') as x:
            xml_dir = json.load(x)
    except Exception as e:
        print("Failed to load schtasks.json:", e)
        return False

    autos, awakes = [], []
    timerconfig = scc.mc.TimerConfig.model_dump()
    l1, l2, l3, l4 = timerconfig['Execute'], timerconfig['Time'], timerconfig['ConfigKeys'], timerconfig['Awake']

    for daily, time, filekey, awake in zip(l1, l2, l3, l4):
        if not (daily and filekey):
            continue
        if daily == 1:
            _item = xml_dir["daily"]
        else:
            _item = xml_dir["weekly"]
            week = ["", "", "Monday", "Tuesday", "Wednesday", "Thursday",
                    "Friday", "Saturday", "Sunday"][daily]
            _item[5] = f"          <{week} />\n"
        try:
            wake_time = subtract_minute(time)
        except ValueError as ve:
            print("Invalid time format:", ve)
            continue
        _item[1] = f"      <StartBoundary>2023-09-20T{wake_time}</StartBoundary>\n"
        if awake:
            awakes += _item
        else:
            autos += _item

    if not autos and not awakes:
        timer_delete()
        return False

    if autos:
        create_task(autos, "SGA-auto", False)
    else:
        CmdRun("schtasks.exe /DELETE /tn SGA-auto /f")

    if awakes:
        create_task(awakes, "SGA-awake", True)
    else:
        CmdRun("schtasks.exe /DELETE /tn SGA-awake /f")

    return True
