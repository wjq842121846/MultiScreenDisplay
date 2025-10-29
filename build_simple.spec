# -*- mode: python ; coding: utf-8 -*-

# 简化的PyInstaller配置文件，专注于稳定性

import sys
import os

# 获取项目路径
project_path = os.path.dirname(os.path.abspath(SPEC))

# 分析主程序
a = Analysis(
    ['simple_launcher.py'],  # 简化启动器作为入口文件
    pathex=[project_path],  # 项目路径
    binaries=[],  # 二进制文件
    datas=[
        # 包含基本文件
        ('ui_styles_complete.py', '.'),
        ('opencv_video_player.py', '.'),
        ('embedded_video_player.py', '.'),
        # 包含资源目录（如果存在）
        ('assets', 'assets') if os.path.exists(os.path.join(project_path, 'assets')) else None,
    ],
    hiddenimports=[
        # 基本PyQt5模块
        'PyQt5.QtCore',
        'PyQt5.QtGui', 
        'PyQt5.QtWidgets',
        'PyQt5.QtWebEngineWidgets',
        'PyQt5.QtMultimedia',
        'PyQt5.QtMultimediaWidgets',
        # OpenCV相关
        'cv2',
        'numpy',
        # 系统模块
        'psutil',
        'json',
        # 项目模块
        'screen_manager',
        'threaded_content_window', 
        'view_config_manager',
        'settings_dialog',
        'ui_styles_complete',
        'splash_screen',
        'opencv_video_player',
        'embedded_video_player',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # 排除不必要的大型模块
        'tkinter', 'matplotlib', 'PIL', 'scipy', 'pandas',
        'jupyter', 'notebook', 'IPython',
        'test', 'tests', '_test', 'testing',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# 过滤掉None值
a.datas = [item for item in a.datas if item is not None]

# 生成PYZ文件
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# 生成可执行文件
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='多屏幕内容管理器_简化版',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # 不显示控制台
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)