import serial
from serial import *
import threading
from serial.tools import hexlify_codec
import codecs
from serial import serialposix
import queue

# modify CMSPAR to support darwin (OS X)
serialposix.CMSPAR = 1
codecs.register(lambda c: hexlify_codec.getregentry() if c == 'hexlify' else None)
q = queue.Queue()


class Nserial():
    '''
    serial 类，包含串口操作的一切方法
    '''
    def __init__(self):
        '''
        初始化串口类各种信息
        '''
        self.port = None
        self.baudrate = 9600
        self.bytesize = None
        self.parity = None
        self.stopbits = None
        self.thread = None
        self.alive = False
        self.raw = False
        self.rx_decoder = None
        self.tx_encoder = None
        self.input_encoding = 'UTF-8'
        self.output_encoding = 'UTF-8'
        self.receive_data = b''
        self.nserial = None

    def open_serial_port(self, port, baudrate, bytesize, parity, stopbits):
        '''
        打开串口函数，并开启接收线程

        :param port: 要打开的串口号
        :param baudrate: 串口波特率
        :param bytesize: 串口数据位位数
        :param parity: 串口校验位位数
        :param stopbits: 串口停止位位数
        :return: 没有返回值
        '''
        bytesize = self.trans_databits(bytesize)
        parity = self.trans_parity(parity)
        stopbits = self.trans_stopbits(stopbits)
        self.nserial = serial.Serial(port=port, baudrate=baudrate, bytesize=bytesize, parity=parity, stopbits=stopbits)
        self.StartThread()

    def close_serial_port(self):
        '''
        关闭串口， 取消串口读取，关闭串口并销毁 nserial 对象

        :return: 不返回值
        '''
        self.StopThread()
        if hasattr(self.nserial, 'cancel_read'):
            self.nserial.cancel_read()
        try:
            self.nserial.close()
            self.nserial = None
        except OSError:
            pass

    def StartThread(self):
        '''
        开始接收数据线程

        :return: 不返回值
        '''
        self.thread = threading.Thread(target=self.read, args=())
        self.thread.setDaemon(True)
        self.alive = True
        self.thread.start()

    def StopThread(self):
        '''
        停止接收数据线程，并等待线程结束，然后销毁线程对象

        :return: 不返回值
        '''
        if self.thread is not None:
            self.alive = False
            self.thread.join(0.1)  # wait until thread has finished
            self.thread = None

    def read(self):
        '''
        循环读取串口内容， 这里跟 miniterm，minicom 等都不一样，这些串口助手会把数据截断，这里修复了这个问题

        :return: 不返回数据，串口读取的数据写入到了 Queue 对象里面，在 mainwindow 中被读取并处理
        '''
        while self.alive:
            try:
                while self.nserial.inWaiting() > 0:
                    self.receive_data += self.nserial.read(1)
                    time.sleep(0.001)
            except OSError:
                pass
            if self.receive_data != b'':
                q.put(self.receive_data)
                self.receive_data = b''

    def write(self, data):
        '''
        向串口写入数据

        :param data: 等待写入的数据（str）

        :return: 不返回值
        '''
        try:
            self.nserial.write(self.tx_encoder.encode(data))
        except:
            self.close_serial_port()
            raise

    def get_alive_status(self):
        '''
        获取读取串口数据的线程存活状态

        :return: bool 值，存活状态
        '''
        return self.alive

    @staticmethod
    def trans_parity(parity):
        '''
        校验位数据界面数值和宏定义数值的转换，利用字典进行转换

        :param parity: 校验位字符串，界面combobox 选中的选项数值，即下面字典的键

        :return: 返回预定义的校验位格式
        '''
        pa = {"无校验": PARITY_NONE, "奇校验": PARITY_ODD, "偶校验": PARITY_EVEN, "1 校验": PARITY_MARK, "0 校验": PARITY_SPACE}
        return pa[parity]

    @staticmethod
    def trans_databits(bytesize):
        '''
        数据位界面数值和宏定义数值的转换，，利用字典进行转换

        :param bytesize: 数据位位字符串，界面combobox 选中的选项数值，即下面字典的键

        :return: 返回预定义的数据位格式
        '''
        bs = {'5': FIVEBITS, '6': SIXBITS, '7': SEVENBITS, '8': EIGHTBITS}
        return bs[str(bytesize)]

    @staticmethod
    def trans_stopbits(stopbits):
        '''
        停止位界面数值和宏定义数值的转换，，利用字典进行转换

        :param bytesize: 停止位位字符串，界面combobox 选中的选项数值，即下面字典的键

        :return: 返回预定义的停止位格式
        '''
        sb = {'1': STOPBITS_ONE, '1.5': STOPBITS_ONE_POINT_FIVE, '2': STOPBITS_TWO}
        return sb[str(stopbits)]

# Nserial 实例化对象，因为串口为硬件，开多个线程或出现问题，所以单线程来操作硬件
noodles_serial = Nserial()
