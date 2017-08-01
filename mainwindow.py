from serial.tools import list_ports
from mainwindow_ui import Ui_MainWindow
from PyQt5.QtWidgets import QMainWindow, QFileDialog
import nserial
import time
import threading
import codecs


class MainWindow(QMainWindow, Ui_MainWindow):
    '''
    界面文件的各种操作方法实现，此类继承了 mainwindiw_ui，并对其进行操作，防止界面修改之后再次转化成 .py 代码丢失的问题
    '''
    def __init__(self, parent=None):
        '''
        类中各种变量初始化

        :param parent:
        '''
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.init_ports_combobox()
        self.port_name = None
        self.parity = None
        self.databit = None
        self.stopbit = None
        self.auto_send_thread = None
        self.open_serial_button_status = False
        self.stop_show_data_flag = False
        self.open_serial_button.clicked.connect(self.do_open_serial_port)
        self.send_data_button.clicked.connect(self.send_data)
        self.baudrate_combox.currentTextChanged.connect(self.init_ports_combobox)
        self.refresh_serial_info.clicked.connect(self.init_ports_combobox)
        self.clear_send_edit_btn.clicked.connect(self.send_edit.clear)
        self.clear_recv_data.clicked.connect(self.recv_data_browser.clear)
        self.stop_show_data.clicked.connect(self.stop_show)
        self.save_to_file_button.clicked.connect(self.save_to_file)
        self.auto_send_checkbox.stateChanged.connect(self.auto_send_check_event)
        self.send_edit_tab.setFocus()
        self.do_append_recv_data()
        self.stop_show_data.setDisabled(True)
        # self.open_serial_button.clicked.connect(lambda: nserial.noodles_serial.open_serial_port(
        #     port=self.port_name, baudrate=115200, bytesize=self.databit,
        #     parity=self.parity, stopbits=self.stopbit))

    def init_ports_combobox(self):
        '''
        初始化串口 combobox 串口号信息， 把程序扫描得到的串口添加到 combobox 的选项中

        :return: 不返回数据
        '''
        serial_ports = list_ports.comports()
        self.serialport_combox.clear()
        for serial_port in serial_ports:
            self.serialport_combox.addItem(str(serial_port.device))

    def do_open_serial_port(self):
        '''
        打开串口并改变相应界面操作

        :return: 不返回数据
        '''
        self.port_name = self.serialport_combox.currentText()
        self.parity = self.parity_combox.currentText()
        self.databit = self.databit_combox.currentText()
        self.stopbit = self.stopbit_combox.currentText()
        self.statusbar.clearMessage()
        if not self.open_serial_button_status:
            nserial.noodles_serial.open_serial_port(port=self.port_name, baudrate=115200, bytesize=self.databit,
                                                    parity=self.parity, stopbits=self.stopbit)
            self.serialport_combox.setDisabled(True)
            self.refresh_serial_info.setDisabled(True)
            self.open_serial_button_status = True
            self.stop_show_data.setDisabled(False)
            self.save_to_file_button.setDisabled(True)
            self.open_serial_button.setText("关闭串口")
        else:
            self.do_close_serial_port()
            self.serialport_combox.setDisabled(False)
            self.refresh_serial_info.setDisabled(False)
            self.open_serial_button_status = False
            self.stop_show_data.setDisabled(True)
            self.save_to_file_button.setDisabled(False)
            self.open_serial_button.setText("打开串口")

    def do_close_serial_port(self):
        '''
        关闭串口并进行相应界面操作

        :return:
        '''
        self.init_ports_combobox()
        nserial.noodles_serial.close_serial_port()

    def append_recv_data(self):
        '''
        把接收到的数据从 nserial 中的 Queue 队列中取出来并 append 到界面接收区

        :return:
        '''
        while True:
            if nserial.q.not_empty and not self.stop_show_data_flag:
                data = nserial.q.get()
                if self.recv_hex_checkbox.isChecked():
                    data = codecs.encode(data, 'hex')
                self.recv_data_browser.append(data.decode())
            time.sleep(0.001)

    def do_append_recv_data(self):
        recv_to_ui_thread = threading.Thread(target=self.append_recv_data, args=())
        recv_to_ui_thread.setDaemon(True)
        recv_to_ui_thread.start()

    def send_data(self):
        '''
        从界面发送方去获取数据并发送到串口

        :return:
        '''
        try:
            data = self.send_edit.toPlainText().encode()
            if not data:
                self.statusbar.showMessage("数据发送区为空，发送失败！")
            else:
                if self.send_hex_checkbox.isChecked():
                    data = codecs.encode(data, 'hex')
                nserial.noodles_serial.write(data.decode())
        except AttributeError:
            self.statusbar.showMessage("请先打开串口！")
        if self.clear_after_send_checkbox.isChecked():
            self.send_edit.clear()

    def stop_show(self):
        '''
        停止显示接收到的数据，为了防止数据丢失，不显示的时候就不读取 queue，此时数据暂存在 queue中，在下面显示的时候可以读取出来。

        :return:
        '''
        if not self.stop_show_data_flag:
            self.stop_show_data_flag = True
            self.save_to_file_button.setDisabled(False)
            self.stop_show_data.setText("开始显示")
        else:
            self.stop_show_data_flag = False
            self.save_to_file_button.setDisabled(True)
            self.stop_show_data.setText("停止显示")

    def save_to_file(self):
        '''
        保存接收区的数据到文件

        :return:
        '''
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "Text Files (*.txt)", options=options)
        if fileName:
            with open(fileName + ".txt", 'a') as f:
                f.write(self.recv_data_browser.toPlainText())

    def auto_send(self):
        '''
        根据设定的时间自动发送发送去的数据

        :return:
        '''
        while self.auto_send_checkbox.isChecked():
            self.send_data()
            time.sleep(float(self.auto_send_time.text())/1000)

    def auto_send_check_event(self, state):
        '''
        自动发送数据 checkbox 选中与取消选中的事件处理

        :param state: checkbox 事件传递的信号，2位选中，0为取消选中
        :return:
        '''
        if state == 2:
            self.clear_after_send_checkbox.setChecked(False)
            self.auto_send_thread = threading.Thread(target=self.auto_send, args=())
            self.auto_send_thread.start()
        else:
            self.auto_send_thread.join()
            self.auto_send_thread = None


