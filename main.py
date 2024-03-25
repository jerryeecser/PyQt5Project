import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, \
                            QGridLayout, QLabel, QMessageBox, QComboBox, \
                            QCheckBox
import serial
import time
import serial.tools.list_ports


class CO2UI(QWidget):
 
    def __init__(self):
        super(CO2UI, self).__init__()
        self.initUI()
        global flag_open     #标志位，判断串口是否打开
        self.flag_open = 0
    def initUI(self):
        grid = QGridLayout()
 
        self.portname = QLabel("端口号")
        self.datanumber = QLabel("发送数据位数：")
        self.datasender = QLabel("发送数据：")
        self.datareview = QLabel("接收数据：")
        self.button = QPushButton("发送")
        self.open_button = QPushButton("打开")
        self.portnameEdit = QLineEdit()
        self.datanumberEdit = QLineEdit()
        self.datasenderEdit = QLineEdit()
        self.datareviewEdit = QLineEdit()
 
        grid.addWidget(self.portname, 1, 0)
        grid.addWidget(self.portnameEdit, 1, 1)
        grid.addWidget(self.datanumber, 2, 0)
        grid.addWidget(self.datanumberEdit, 2, 1)
        grid.addWidget(self.datasender, 3, 0,)
        grid.addWidget(self.datasenderEdit, 3, 1, 1, 6)
        grid.addWidget(self.datareview, 4, 0)
        grid.addWidget(self.datareviewEdit, 4, 1, 1, 6)
        grid.addWidget(self.button, 5, 3)
        grid.addWidget(self.open_button, 5, 1)
        self.setLayout(grid)
 
        self.button.clicked.connect(self.Cosender)
        self.open_button.clicked.connect(self.Check_serial)
        self.setGeometry(300,300,200,200)
        self.setWindowTitle("C02上位机")
    def messageUI(self):
        '''提示信息'''
        QMessageBox.critical(self, " ", "串口打开失败，请选择正确的串口")
    def Check_serial(self):
        '''检测串口是否被打开'''
        try:
            self.t = serial.Serial('com4', 9600)   #打开串口COM4
            port = self.t.portstr     #返回但端口号
            self.portnameEdit.setText(port)   #显示在界面上
            self.flag_open=1
        except serial.serialutil.SerialException:   #打开失败，输出提示信息
            self.messageUI()      #提示信息
 
    def Cosender(self):
        if self.flag_open==1:
            if self.flag_open == 1:  # 串口被打开
                self.str_input = self.datasenderEdit.text()  # 返回上面的发送文字
                n = self.t.write((self.str_input + '\n').encode())
                self.datanumberEdit.setText(str(n - 1))  # 写入数据位数框
                self.datasenderEdit.setText(str(self.str_input))  # 写入发送框
                time.sleep(1)  # sleep() 与 inWaiting() 最好配对使用
                num = self.t.inWaiting()  # 获取接收到的数据长度
                if num:
                    self.receivemessage = self.t.read(num)  # 读取接收数据
                    print(self.receivemessage)
                    self.datareviewEdit.setText(str(self.receivemessage)[2:-3])  # 写入接收框
        else:
            self.messageUI()
 
 
if __name__ == "__main__":
    app = QApplication(sys.argv)
    test = CO2UI()
    test.show()
    sys.exit(app.exec_())