from main.mainwindows import smw
from main.mainenvironment import sme


# def check_update():
#     smw.overall.button_check.setEnabled(False)
#     smw.sendbox(mode=1)
#     smw.sendbox("检查更新中...", mode=2)
#
#
# def load_update():
#     smw.overall.button_update.setEnabled(False)
#     smw.sendbox(mode=1)
#     smw.sendbox("开始更新中", mode=2)


def update_check_change():
    sme.update = smw.overall.auto_update.isChecked()


def open_update_history():
    from os import startfile
    startfile(sme.workdir + "/update.txt")
    smw.sendbox(mode=1)
    smw.sendbox("打开更新日志")
    smw.sendbox(mode=3)


def ocr_dir_change():
    smw.sendbox(mode=1)
    from main.tools.ocr.main import ocr
    ocr.exe_path = smw.overall.ocr_path_line.text()
    if not ocr.check():
        _str = (f"指定的OCR路径无效。可参考从以下链接从\"PaddleOCR\"和\"RapidOCR\""
                f"中选择\"{sme.ocr.exe_name}\"进行下载"
                f"并将其解压到\"ocr_json\"文件夹下，并重启SGA完成安装。\n"
                f"或重新指定\"{sme.ocr.exe_name}\"的绝对路径。\n"
                f"例如： E:\\OCR-json\\{sme.ocr.exe_name}")
        smw.sendbox(_str)
    else:
        sme.ocrdir = ocr.exe_path
        smw.sendbox("成功检测到指定的OCR组件，OCR已就绪")
    smw.sendbox(mode=3)
