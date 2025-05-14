# runtime_hook.py
import sys
import os
import shutil


def copy_resources():
    if getattr(sys, 'frozen', False):
        # 需要复制到外部的资源列表
        resources = [
            ("assets", "assets"),
            ("README.md", "README.md"),
            ("update_history.txt", "update_history.txt"),
            ("3rd_package", "3rd_package"),
            ("Instructions.docx", "Instructions.docx"),
            ("SGA快速上手.docx", "SGA快速上手.docx")
        ]

        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)

        for src, dst in resources:
            dst_path = os.path.join(os.path.dirname(sys.executable), dst)
            src_path = os.path.join(base_path, src)
            if os.path.exists(dst_path) or not os.path.exists(src_path):
                continue
            if os.path.isdir(src_path):
                shutil.move(src_path, dst_path)
            else:
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.move(src_path, dst_path)


copy_resources()