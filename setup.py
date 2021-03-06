"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['main.py']
DATA_FILES = ['app.icns']

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app.icns',
    # 加了下面一段 app 秒退
    # 'plist': {
    #     'CFBundleName': "泡面串口助手",
    #     'CFBundleDisplayName': "泡面串口助手",
    #     'CFBundleGetInfoString': "跨平台通用串口助手",
    #     'CFBundleIdentifier': "com.noodles.osx.qinfei",
    #     'CFBundleVersion': "0.1.0",
    #     'CFBundleShortVersionString': "0.1.0",
    #     'NSHumanReadableCopyright': u"Copyright © 2017, qinfei Nantong, All Rights Reserved"
    # }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

