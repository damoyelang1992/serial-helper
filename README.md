https://git.oschina.net/damoyelang1992/serial-helper  下面粘贴说明
#serial-helper

qt5 串口助手 跨平台兼容

下载地址：http://qinfei-blog.oss-cn-hangzhou.aliyuncs.com/uploads/serial-helper.dmg

代码说明文档： https://damoyelang1992.github.io/serial-helper/doc/build/html/

## 兼容平台：

兼容 OSX(测试环境：macOS Sierra 10.12)

兼容raspberry pi 3(测试环境：ubuntu Mate)

Windows 未测试。

代码环境： python3.5 PyQt5 以及其他依赖（requirements.txt）

打包出来的 app 文件太大(200M+), 所以需要删减, 具体删减结果见文章最后清单。

## 建议直接编译使用 

编译方法：

```
pip3 install virtualenv

mkdir myproject

cd myproject/

virtualenv --no-site-packages venv

source venv/bin/activate

git clone https://github.com/damoyelang1992/serial-helper.git

cd serial-helper

pip install -r requirements.txt

python main.py

```

## 或者编译 app （MAC 用户）

教程（下面部分为引用此文章）： http://www.jianshu.com/p/afb6b2b97ce9

安装 py2app:

```bash
pip install -U git+https://github.com/metachris/py2app.git@master
```

创建 setup.py 文件：

```bash
py2applet --make-setup main.py
```

查看文件内容，并修改相应信息(OPTIONS 添加了图标，下面不要忘记把文件添加进来哦)：
 
```python
from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app.icns',
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

```

添加图标文件等——修改：

```python
DATA_FILES = ['testdata.json', 'picture.png']
```
创建开发版和测试版的应用：

```bash
python setup.py py2app -A
```

这并不是一个独立的应用，并且通过别名模式构建的应用不适用于其他机器。

别名模式下构建的应用直接引用了源码文件，所以任何对 main.py 文件作的修改在应用下次启动时会立刻生效。

构建发布版应用：

```bash
python setup.py py2app
```

打包成 dmg： 

```bash
hdiutil create ptimer.dmg -srcfolder dist/ptimer.app
```

更高级设置：
```python
# -*- coding: utf-8 -*-
from setuptools import setup

APP = ['Sandwich.py']
APP_NAME = "SuperSandwich"
DATA_FILES = []

OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app.icns',
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "Making Sandwiches",
        'CFBundleIdentifier': "com.metachris.osx.sandwich",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': u"Copyright © 2015, Chris Hager, All Rights Reserved"
    }
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

## 比较重要的部分：
 
我手动重写了 serial.serialposix.CMSPAR 的值，如果没有重写 OSX 不支持 1校验 和 0校验，在 serial 库说明中提示在不支持的平台上需要重写这个值

```python
from serial import serialposix

# modify CMSPAR to support darwin (OS X)
serialposix.CMSPAR = 1
```

另外注意串口接收部分与 miniterm minicom 都不一样，他们的接收会导致数据断开几部分。

##### Windows 用户请使用 py2exe 自行打包

##### Linux 用户建议直接运行源代码

MAC app 删减最终目录 tree：

```
.
└── Contents
    ├── Frameworks
    │   └── Python.framework
    │       ├── Python -> Versions/Current/Python
    │       ├── Resources -> Versions/Current/Resources
    │       └── Versions
    │           ├── 3.6
    │           │   ├── Python
    │           │   ├── Resources
    │           │   │   └── Info.plist
    │           │   ├── include
    │           │   │   └── python3.6m
    │           │   │       └── pyconfig.h
    │           │   └── lib
    │           │       └── python3.6
    │           │           └── config-3.6m-darwin
    │           │               └── Makefile
    │           └── Current -> 3.6
    ├── Info.plist
    ├── MacOS
    │   ├── main
    │   └── python
    ├── PkgInfo
    └── Resources
        ├── __boot__.py
        ├── __error__.sh
        ├── app.icns
        ├── include
        │   └── python3.6m
        │       └── pyconfig.h
        ├── lib
        │   ├── python3.6
        │   │   ├── PyQt5
        │   │   │   ├── Qt
        │   │   │   │   ├── lib
        │   │   │   │   │   ├── QtCore.framework
        │   │   │   │   │   │   └── Versions
        │   │   │   │   │   │       └── 5
        │   │   │   │   │   │           └── QtCore
        │   │   │   │   │   ├── QtGui.framework
        │   │   │   │   │   │   └── Versions
        │   │   │   │   │   │       └── 5
        │   │   │   │   │   │           └── QtGui
        │   │   │   │   │   ├── QtHelp.framework
        │   │   │   │   │   │   └── Versions
        │   │   │   │   │   │       └── 5
        │   │   │   │   │   │           └── QtHelp
        │   │   │   │   │   ├── QtMacExtras.framework
        │   │   │   │   │   │   └── Versions
        │   │   │   │   │   │       └── 5
        │   │   │   │   │   │           └── QtMacExtras
        │   │   │   │   │   ├── QtPrintSupport.framework
        │   │   │   │   │   │   └── Versions
        │   │   │   │   │   │       └── 5
        │   │   │   │   │   │           └── QtPrintSupport
        │   │   │   │   │   └── QtWidgets.framework
        │   │   │   │   │       └── Versions
        │   │   │   │   │           └── 5
        │   │   │   │   │               └── QtWidgets
        │   │   │   │   ├── plugins
        │   │   │   │   │   ├── PyQt5
        │   │   │   │   │   │   └── libpyqt5qmlplugin.dylib
        │   │   │   │   │   ├── iconengines
        │   │   │   │   │   │   └── libqsvgicon.dylib
        │   │   │   │   │   ├── imageformats
        │   │   │   │   │   │   ├── libqgif.dylib
        │   │   │   │   │   │   ├── libqicns.dylib
        │   │   │   │   │   │   ├── libqico.dylib
        │   │   │   │   │   │   ├── libqjpeg.dylib
        │   │   │   │   │   │   ├── libqmacjp2.dylib
        │   │   │   │   │   │   ├── libqsvg.dylib
        │   │   │   │   │   │   ├── libqtga.dylib
        │   │   │   │   │   │   ├── libqtiff.dylib
        │   │   │   │   │   │   ├── libqwbmp.dylib
        │   │   │   │   │   │   └── libqwebp.dylib
        │   │   │   │   │   ├── platforms
        │   │   │   │   │   │   ├── libqcocoa.dylib
        │   │   │   │   │   │   ├── libqminimal.dylib
        │   │   │   │   │   │   └── libqoffscreen.dylib
        │   │   │   │   │   └── printsupport
        │   │   │   │   │       └── libcocoaprintersupport.dylib
        │   │   │   │   └── translations
        │   │   │   │       └── qt_en.qm
        │   │   │   ├── Qt.so
        │   │   │   ├── QtCore.so
        │   │   │   ├── QtGui.so
        │   │   │   ├── QtMacExtras.so
        │   │   │   ├── QtPrintSupport.so
        │   │   │   ├── QtWidgets.so
        │   │   │   ├── __init__.py
        │   │   │   ├── pyrcc.so
        │   │   │   ├── pyrcc_main.py
        │   │   │   └── uic
        │   │   │       ├── Compiler
        │   │   │       │   ├── __init__.py
        │   │   │       │   ├── compiler.py
        │   │   │       │   ├── indenter.py
        │   │   │       │   ├── misc.py
        │   │   │       │   ├── proxy_metaclass.py
        │   │   │       │   ├── qobjectcreator.py
        │   │   │       │   └── qtproxies.py
        │   │   │       ├── Loader
        │   │   │       │   ├── __init__.py
        │   │   │       │   ├── __pycache__
        │   │   │       │   │   ├── __init__.cpython-36.pyc
        │   │   │       │   │   ├── loader.cpython-36.pyc
        │   │   │       │   │   └── qobjectcreator.cpython-36.pyc
        │   │   │       │   ├── loader.py
        │   │   │       │   └── qobjectcreator.py
        │   │   │       ├── __init__.py
        │   │   │       ├── driver.py
        │   │   │       ├── exceptions.py
        │   │   │       ├── icon_cache.py
        │   │   │       ├── objcreator.py
        │   │   │       ├── port_v2
        │   │   │       │   ├── __init__.py
        │   │   │       │   ├── __pycache__
        │   │   │       │   │   ├── __init__.cpython-36.pyc
        │   │   │       │   │   ├── as_string.cpython-36.pyc
        │   │   │       │   │   ├── ascii_upper.cpython-36.pyc
        │   │   │       │   │   ├── proxy_base.cpython-36.pyc
        │   │   │       │   │   └── string_io.cpython-36.pyc
        │   │   │       │   ├── as_string.py
        │   │   │       │   ├── ascii_upper.py
        │   │   │       │   ├── proxy_base.py
        │   │   │       │   └── string_io.py
        │   │   │       ├── port_v3
        │   │   │       │   ├── __init__.py
        │   │   │       │   ├── __pycache__
        │   │   │       │   │   ├── __init__.cpython-36.pyc
        │   │   │       │   │   ├── as_string.cpython-36.pyc
        │   │   │       │   │   ├── ascii_upper.cpython-36.pyc
        │   │   │       │   │   ├── proxy_base.cpython-36.pyc
        │   │   │       │   │   └── string_io.cpython-36.pyc
        │   │   │       │   ├── as_string.py
        │   │   │       │   ├── ascii_upper.py
        │   │   │       │   ├── proxy_base.py
        │   │   │       │   └── string_io.py
        │   │   │       ├── properties.py
        │   │   │       ├── pyuic.py
        │   │   │       ├── uiparser.py
        │   │   │       └── widget-plugins
        │   │   │           ├── __pycache__
        │   │   │           │   ├── qaxcontainer.cpython-36.pyc
        │   │   │           │   ├── qscintilla.cpython-36.pyc
        │   │   │           │   ├── qtcharts.cpython-36.pyc
        │   │   │           │   ├── qtprintsupport.cpython-36.pyc
        │   │   │           │   ├── qtquickwidgets.cpython-36.pyc
        │   │   │           │   ├── qtwebenginewidgets.cpython-36.pyc
        │   │   │           │   └── qtwebkit.cpython-36.pyc
        │   │   │           ├── qaxcontainer.py
        │   │   │           ├── qscintilla.py
        │   │   │           ├── qtcharts.py
        │   │   │           ├── qtprintsupport.py
        │   │   │           ├── qtquickwidgets.py
        │   │   │           ├── qtwebenginewidgets.py
        │   │   │           └── qtwebkit.py
        │   │   ├── config-3.6m-darwin
        │   │   ├── lib-dynload
        │   │   │   ├── _bisect.so
        │   │   │   ├── _blake2.so
        │   │   │   ├── _bz2.so
        │   │   │   ├── _codecs_cn.so
        │   │   │   ├── _codecs_hk.so
        │   │   │   ├── _codecs_iso2022.so
        │   │   │   ├── _codecs_jp.so
        │   │   │   ├── _codecs_kr.so
        │   │   │   ├── _codecs_tw.so
        │   │   │   ├── _ctypes.so
        │   │   │   ├── _datetime.so
        │   │   │   ├── _decimal.so
        │   │   │   ├── _elementtree.so
        │   │   │   ├── _hashlib.so
        │   │   │   ├── _heapq.so
        │   │   │   ├── _lzma.so
        │   │   │   ├── _md5.so
        │   │   │   ├── _multibytecodec.so
        │   │   │   ├── _multiprocessing.so
        │   │   │   ├── _opcode.so
        │   │   │   ├── _pickle.so
        │   │   │   ├── _posixsubprocess.so
        │   │   │   ├── _random.so
        │   │   │   ├── _sha1.so
        │   │   │   ├── _sha256.so
        │   │   │   ├── _sha3.so
        │   │   │   ├── _sha512.so
        │   │   │   ├── _socket.so
        │   │   │   ├── _ssl.so
        │   │   │   ├── _struct.so
        │   │   │   ├── array.so
        │   │   │   ├── binascii.so
        │   │   │   ├── fcntl.so
        │   │   │   ├── grp.so
        │   │   │   ├── math.so
        │   │   │   ├── mmap.so
        │   │   │   ├── pyexpat.so
        │   │   │   ├── resource.so
        │   │   │   ├── select.so
        │   │   │   ├── sip.so
        │   │   │   ├── termios.so
        │   │   │   ├── unicodedata.so
        │   │   │   └── zlib.so
        │   │   └── site.pyc -> ../../site.pyc
        │   └── python36.zip
        ├── main.py
        ├── site.pyc
        └── zlib.cpython-36m-darwin.so


```
