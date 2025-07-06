# -*- mode: python ; coding: utf-8 -*-
from os import path
# pyinstaller SGAv3.spec

a = Analysis(
    ['SGAv3.py'],
    pathex=[],
    binaries=[],
    datas=[
            ("venv\Lib\site-packages\win32comext\shell\shellcon.py", "win32com\shell"),
            ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
b = Analysis(
    ['SGAv3-c.py'],
    pathex=[],
    binaries=[],
    datas=[
            ("venv\Lib\site-packages\win32comext\shell\shellcon.py", "win32com\shell"),
            ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
private_module = []
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
pyza = PYZ(a.pure)

temp = b.pure.copy(); b.pure.clear()
for name, src, type in temp:
    condition = [name.startswith(m) for m in private_module]
    if condition and any(condition):
        b.pure.append((name, src, type))    # 把需要保留打包的 py 文件重新添加回 a.pure
    else:
        name = name.replace('.', os.sep)
        init = path.join(name, '__init__.py')
        pos = src.find(init) if init in src else src.find(name)
        dst = src[pos:]
#        dst = path.join('libs', dst)
        b.datas.append((dst, src, 'DATA'))
pyzb = PYZ(b.pure)

exea = EXE(
    pyza,
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
    icon=["resources/main/SGA/icon.ico"],
)
exeb = EXE(
    pyzb,
    b.scripts,
    [],
    exclude_binaries=True,
    name='SGA-c',
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
    icon=["resources/main/SGA/icon.ico"],
)
coll = COLLECT(
    exea,
    exeb,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SGAv3',
)
