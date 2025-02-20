from main.mainwindows import main_windows as mw
from main.tools.environment import env
from os import startfile

    
# 切换页面
def change_interface():
    # print(env.setting, )
    if env.setting:
        mw.main.stack_setting.setCurrentIndex(0)
        env.setting = 0
    else:
        mw.main.stack_setting.setCurrentIndex(1)
        env.setting = 1


def open_log_dir():
    startfile(env.workdir + "/personal/logs")
    mw.sendbox(mode=1)
    mw.sendbox("打开日志文件夹", mode=2)
    mw.sendbox(mode=3)
