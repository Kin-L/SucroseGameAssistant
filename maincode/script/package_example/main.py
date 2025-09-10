from maincode.tools.controller.main import ctler
# 可选：自行添加其他引入，需要填入绝对引入路径

# 脚本名称 必填，显示在连点器和DIY模块界面的下拉框里
script_name = "文件包示例脚本"

# 可选使用：脚本配置
_script_config = {

}

"""
必须包含__init__.py, main.py文件，py文件名和文件夹名必须为字母加下划线
其他资源文件需要放在resource文件夹或personal文件夹内
"""


# 脚本入口 必填
def script_run():
    ctler.send("示例：输出指示信息")
    ctler.wait(1)  # 等待一秒
    ctler.click((100, 100))  # 点击参考系坐标(x = 100, y = 100)
