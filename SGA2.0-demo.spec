# -*- mode: python ; coding: utf-8 -*-
from os import path
# pyinstaller SGA2.0-demo.spec

a = Analysis(
    ['SGA2.0-demo.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
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
    name='SGA2.0-demo',
)
