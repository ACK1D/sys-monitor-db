#!/bin/bash

PLATFORM=$(uname)

python -m venv .venv
source .venv/bin/activate

sudo rm -rf build dist

mkdir -p dist/system-monitor-app/data
mkdir -p dist/system-monitor-app/logs
chmod -R 777 dist/system-monitor-app/data
chmod -R 777 dist/system-monitor-app/logs

if [ "$PLATFORM" = "Darwin" ]; then
    cat > build.spec << EOL
block_cipher = None

a = Analysis(
    ['src/__main__.py'],
    pathex=['src', '.'],
    binaries=[],
    datas=[],
    hiddenimports=['customtkinter', 'src.main', 'src.logger', 'src.config', 'src.database', 'src.translations'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='system-monitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
EOL
else
    # Linux spec
    cat > build.spec << EOL
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['src/__main__.py'],
    pathex=['src', '.'],
    binaries=[],
    datas=[],
    hiddenimports=['customtkinter', 'src.main', 'src.logger', 'src.config', 'src.database', 'src.translations'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='system-monitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
EOL
fi

pyinstaller build.spec --clean

mv dist/system-monitor dist/system-monitor-app/

cd dist
tar -czf system-monitor.tar.gz system-monitor-app/

echo "Build completed. The archive is located in dist/system-monitor.tar.gz" 