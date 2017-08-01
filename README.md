#serial-helper

qt5 串口助手 跨平台兼容

代码说明文档： https://damoyelang1992.github.io/serial-helper/doc/build/html/

## 兼容平台：

兼容 OSX(测试环境：macOS Sierra 10.12)

兼容raspberry pi 3(测试环境：ubuntu Mate)

Windows 未测试。

代码环境： python3.5 PyQt5 以及其他依赖（requirements.txt）

打包出来的 app 文件太大(200M+), 所以需要删减。

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

## 或者编译 app 

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
