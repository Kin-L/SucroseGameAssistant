# -*- mode: python ; coding: utf-8 -*-
from ossu import path
# pyinstaller SGAv2.spec

a = Analysis(
    ['SGAv2.py'],
    pathex=[],
    binaries=[],
    datas=[("assets", "assets"),
            ("README.md", "."),
            ("update_history.txt", "."),
            ("3rd_package", "3rd_package"),
            ("Instructions.docx", "."),
            ("SGA快速上手.docx", "."),
            ("venv\Lib\site-packages\win32comext\shell\shellcon.py", "win32com\shell"),
            ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=["runtime_hook.py"],
    excludes=[],
    noarchive=False,
)
private_module = []                         # hello.exe 不保留任何依赖
temp = a.pure.copy(); a.pure.clear()
for name, src, type in temp:
    condition = [name.startswith(m) for m in private_module]
    if condition and any(condition):
        a.pure.append((name, src, type))    # 把需要保留打包的 py 文件重新添加回 a.pure
    else:
        name = name.replace('.', os.sep)
        init = path.join(name, '__init__.py')
        pos = src.find(init) if init in src else src.find(name)
        dst = src[pos:]
#        dst = path.join('libs', dst)
        a.datas.append((dst, src, 'DATA'))
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='SGA',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=["assets/main_window/ui/ico/SGA.ico"],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SGAv2',
)
