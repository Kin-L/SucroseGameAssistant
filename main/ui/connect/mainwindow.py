from main.ui.mainwindows import main_windows as mw
from main.tools.environment import env


def show_statement():
    notify = "使用须知:\n" \
             "1、该项目（以下称SGA）免费、开源。" \
             "如果您付费购买了该工具，请申请退款并举报售卖方，每一次倒卖都会使开源更加困难。\n" \
             "2、所有用于游戏的第三方工具都不保证没有封号风险。\n" \
             "3、点击停止按钮或快捷键“ctrl+/”中止当前任务。\n" \
             "4、SGA文件夹中有使用说明文件，" \
             "鼠标悬停部分按钮上会有提示信息，或参考B站账号:绘星痕 的SGA介绍视频。\n" \
             "------------------------------"
    mw.box_info.append(notify)
    
    
# 切换页面
def change_interface():
    if env.setting:
        mw.stack_setting.setCurrentIndex(0)
        env.setting = 0
    else:
        mw.stack_setting.setCurrentIndex(1)
        env.setting = 1


# 设置锁定模式
def change_lock():
    if env.lock:
        mw.button_config_lock.hide()
        mw.button_config_unlock.show()
        env.lock = False
    else:
        mw.button_config_unlock.hide()
        mw.button_config_lock.show()
        env.lock = True


