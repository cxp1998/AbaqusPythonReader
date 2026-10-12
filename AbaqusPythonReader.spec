# -*- mode: python ; coding: utf-8 -*-

# Unused PySide6 and standard library modules to exclude
excluded_modules = [
    'PySide6.QtNetwork',
    'PySide6.QtQml',
    'PySide6.QtQuick',
    'PySide6.Qt3D',
    'PySide6.Qt3DCore',
    'PySide6.Qt3DRender',
    'PySide6.QtMultimedia',
    'PySide6.QtMultimediaWidgets',
    'PySide6.QtSensors',
    'PySide6.QtPositioning',
    'PySide6.QtLocation',
    'PySide6.QtBluetooth',
    'PySide6.QtSql',
    'PySide6.QtTest',
    'PySide6.QtPdf',
    'PySide6.QtPdfWidgets',
    'PySide6.QtCharts',
    'PySide6.QtGraphs',
    'PySide6.QtDataVisualization',
    'PySide6.QtVirtualKeyboard',
    'tkinter',
    'unittest',
    'pydoc',
    'email',
    'html',
    'http',
    'xmlrpc',
    'bz2',
    'lzma',
]

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('abaqus_python_reader/resources', 'abaqus_python_reader/resources'),
        ('abaqus_python_reader/app.ico', 'abaqus_python_reader'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excluded_modules,
    noarchive=False,
    optimize=2,
)

# Strip out bulky, unused binaries and Qt plugins (e.g. opengl32sw, network, unused image formats)
excluded_bin_keywords = [
    'opengl32sw',
    'qt6network',
    'qtnetwork',
    'qopensslbackend',
    'qcertonlybackend',
    'qschannelbackend',
    'qnetworklistmanager',
    'qtvirtualkeyboardplugin',
    'qdirect2d',
    'qminimal',
    'qoffscreen',
    'qtuiotouchplugin',
    'qpdf',
    'qwebp',
    'qtga',
    'qgif',
    'qwbmp',
    'qicns',
    'qtiff',
    'd3dcompiler',
]

a.binaries = [
    b for b in a.binaries
    if not any(k in b[0].lower() for k in excluded_bin_keywords)
]

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AbaqusPythonReader',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['abaqus_python_reader/app.ico'],
)
