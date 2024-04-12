#基本控件显示的包 包括QLabel, QComboX
import sys
import time
import serial
from PyQt5 import QtWidgets 
from serial.tools import list_ports
from PyQt5.QtWidgets import QWidget, QMessageBox, QHBoxLayout, QVBoxLayout, QFormLayout, QGroupBox, QLabel, QCheckBox, QComboBox, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtCore import QTimer, Qt, QThread, pyqtSignal

#界面整体布局
class basicsurf(QWidget):
    def __init__(self):
        super().__init__()
        #变量定义
        self.x_coordinate = 180
        self.TCPEND = True
        self.ser = serial.Serial()
        #右边四列的控件列表
        self.V1label = [ ]
        self.V2label = [ ]
        self.V3label = [ ]
        self.V4label = [ ]
        self.DataReceive = 0
        self.DataSended  = 0
        self.init_ui()
        self.SignalProcessing()
        self.ColorChange() #状态颜色示意

    def init_ui(self):    
        #window基本设置
        self.setWindowTitle('EfuseControl GUI')
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.resize(480, 350)
        Container = QHBoxLayout() #总体水平布局

        #串口基本设置
        MinusGroupbox   = QGroupBox('')
        MinusGroupbox_  = QGroupBox('') 
        MinusGroupbox__ = QGroupBox('')
        MinusLayout    = QFormLayout()
        MinusLayout_   = QHBoxLayout()
        MinusLayout__  = QVBoxLayout()
        MinusLayout___ = QVBoxLayout()
        _MinusLayout   = QHBoxLayout()
        __MinusLayout  = QHBoxLayout()
        ___MinusLayout = QVBoxLayout()
        self.COMInput  = QComboBox()
        self.Baudrate  = QComboBox()
        self.DataBits  = QComboBox()
        self.CheckBits = QComboBox()
        self.StopBits  = QComboBox()

        self.AutoDetect  = QPushButton("检测串口") #有布局的情况下,不需要在控件中继承self,因为布局已经完成了继承
        self.OpenButton  = QPushButton("打开串口")
        self.CloseButton = QPushButton("关闭串口")

        self.CheckSend   = QCheckBox()
        self.LabelSend   = QLabel("定时发送")
        self.PeriodSend  = QLabel("ms/次")
        self.LabelTX     = QLabel("TX")
        self.LabelRX     = QLabel("RX") 
        self.Number      = QLineEdit("1000")
        self.TXData      = QLineEdit()
        self.RXData      = QLineEdit()
        
        self.TXData.setText("0")
        self.RXData.setText("0")
        self.TXData.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.RXData.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.COMInput.addItems(['COM1', 'COM2', 'COM3', 'COM4', 'COM5'])
        self.Baudrate.addItems(['9600', '19200', '38400', '115200']) 
        self.DataBits.addItems(['8', '7', '6', '5'])
        self.CheckBits.addItems(['None', 'ODD', 'EVEN'])
        self.StopBits.addItems(['1', '2'])
        
        MinusLayout.addRow("COMInput", self.COMInput)
        MinusLayout.addRow("Baudrate", self.Baudrate)
        MinusLayout.addRow("DataBits", self.DataBits)
        MinusLayout.addRow("CheckBits", self.CheckBits)
        MinusLayout.addRow("StopBits", self.StopBits)
        MinusLayout_.addWidget(self.AutoDetect)
        MinusLayout_.addWidget(self.OpenButton)
        MinusLayout__.addWidget(self.CloseButton)
        _MinusLayout.addWidget(self.Number)
        _MinusLayout.addWidget(self.PeriodSend)
        _MinusLayout.addWidget(self.CheckSend)
        _MinusLayout.addWidget(self.LabelSend)
        __MinusLayout.addWidget(self.LabelTX)
        __MinusLayout.addWidget(self.TXData)
        __MinusLayout.addWidget(self.LabelRX)
        __MinusLayout.addWidget(self.RXData)

        MinusLayout___.addLayout(MinusLayout_)
        MinusLayout___.addLayout(MinusLayout__)
        ___MinusLayout.addLayout(_MinusLayout)
        ___MinusLayout.addLayout(__MinusLayout)
        MinusGroupbox.setLayout(MinusLayout)
        MinusGroupbox_.setLayout(MinusLayout___)
        MinusGroupbox__.setLayout(___MinusLayout)

        #第零列 串口发送/接收/LOG显示
        V0GroupBox   = QGroupBox('DataReceiveArea')
        V0GroupBox_  = QGroupBox('DataSendArea')
        V0GroupBox__ = QGroupBox('')
        V0Layout   = QVBoxLayout()
        V0Layout_  = QVBoxLayout()
        V0Layout__ = QHBoxLayout()
        self.receive_area = QTextEdit()
        self.send_area    = QTextEdit()
        self.send_button  = QPushButton("SEND")
        self.ClearButton  = QPushButton("CLEAR")
        self.receive_area.setFontPointSize(9)
        self.send_area.setFontPointSize(9)
        
        V0Layout.addWidget(self.receive_area)
        V0Layout_.addWidget(self.send_area)
        V0Layout__.addWidget(self.send_button)
        V0Layout__.addWidget(self.ClearButton)
        V0GroupBox.setLayout(V0Layout)
        V0GroupBox_.setLayout(V0Layout_)
        V0GroupBox__.setLayout(V0Layout__)

        #第一列  每列两个group,则两个QGroupBox和两个QVBoxLayout
        V1GroupBox  = QGroupBox('') #组布局
        V1GroupBox_ = QGroupBox('')
        V1Layout  = QVBoxLayout() #垂直组创建
        V1Layout_ = QVBoxLayout()

        IdLabel = QLabel("EfuseId") #EfuseID
        # IdLabel.setStyleSheet("background-color: rgb(220, 220, 220)")
        V1Layout_.addWidget(IdLabel)

        for i in range(1, 11):
            #exec()创建动态变量
            # exec(f'self.TextLabel{i}1 = QTextEdit(self)')
            # self.V1Layout.addWidget(getattr(self, f'TextLabel{i}1')) #getattr()获取动态创建的变量
            label = QLineEdit(self)
            # label.setObjectName(f'OneLabel{i}1')
            V1Layout.addWidget(label)
            self.V1label.append(label)

        V1GroupBox.setLayout(V1Layout)
        V1GroupBox_.setLayout(V1Layout_)
        
        #第二列
        V2GroupBox  = QGroupBox('')
        V2GroupBox_ = QGroupBox('') 
        V2Layout  = QVBoxLayout()
        V2Layout_ = QVBoxLayout()
        StatusLabel = QLabel("EfuseSTS") #EfuseStatus
        V2Layout_.addWidget(StatusLabel)
        
        for i in range(1, 11):
            light = QLineEdit(self)
            # light.setObjectName(f'LightLabel{i}1')
            light.setEnabled(False)
            light.setStyleSheet("background-color: rgb(255, 255, 0);\n"
                                "border-radius: 4px;\n"
                                "border:2px groove gray;\n" #圆边设置
                                "border-style: outset;\n")
            V2Layout.addWidget(light)
            self.V2label.append(light)
        
        V2GroupBox.setLayout(V2Layout)
        V2GroupBox_.setLayout(V2Layout_)

        #第三列
        V3GroupBox  = QGroupBox('')
        V3GroupBox_ = QGroupBox('') 
        V3Layout  = QVBoxLayout()
        V3Layout_ = QVBoxLayout()
        CurrentLabel = QLabel("Current") #Current
        V3Layout_.addWidget(CurrentLabel)

        for i in range(1, 11):
            label3 = QLineEdit(self)
            label3.setObjectName(f'ThreeLabel{i}3')
            V3Layout.addWidget(label3)
            self.V3label.append(label3)

        V3GroupBox.setLayout(V3Layout)
        V3GroupBox_.setLayout(V3Layout_)

        #第四列
        V4GroupBox  = QGroupBox('')
        V4GroupBox_ = QGroupBox('')
        V4Layout  = QVBoxLayout()
        V4Layout_ = QVBoxLayout()
        VoltageLabel = QLabel(self) #Voltage
        VoltageLabel.setText('Voltage')
        V4Layout_.addWidget(VoltageLabel)

        for i in range(1, 11):
            label4 = QLineEdit(self)
            label4.setObjectName(f'FourLabel{i}3')
            V4Layout.addWidget(label4)
            self.V4label.append(label4)

        V4GroupBox.setLayout(V4Layout)
        V4GroupBox_.setLayout(V4Layout_)
        
        #串口设置布局
        Container_minus = QVBoxLayout()
        Container_minus.addWidget(MinusGroupbox)
        Container_minus.addWidget(MinusGroupbox_)
        Container_minus.addWidget(MinusGroupbox__)
        #左侧垂直布局
        Container_zero = QVBoxLayout()
        Container_zero.addWidget(V0GroupBox, 2)
        Container_zero.addWidget(V0GroupBox_, 1)
        Container_zero.addWidget(V0GroupBox__)
        #第一列垂直布局
        Container_one = QVBoxLayout()
        Container_one.addWidget(V1GroupBox_, 1)
        Container_one.addWidget(V1GroupBox, 10)
        #第二列垂直布局
        Container_two = QVBoxLayout()
        Container_two.addWidget(V2GroupBox_, 1)
        Container_two.addWidget(V2GroupBox, 10)
        #第三列垂直布局
        Container_three = QVBoxLayout()
        Container_three.addWidget(V3GroupBox_, 1)
        Container_three.addWidget(V3GroupBox, 10)
        #第四列垂直布局
        Container_four = QVBoxLayout()
        Container_four.addWidget(V4GroupBox_, 1)
        Container_four.addWidget(V4GroupBox, 10)
        #总体布局设置
        Container.addLayout(Container_minus)
        Container.addLayout(Container_zero)
        Container.addLayout(Container_one)
        Container.addLayout(Container_two)
        Container.addLayout(Container_three)
        Container.addLayout(Container_four)
        
        self.setLayout(Container)
    
    #端口检测
    def AutoDetectOperation(self):
        port_list = list(list_ports.comports()) #port list转化为列表形式 port_list = [[com1, xxx], [com2, xxx]]
        self.COMInput.clear() #将原有box中的元素清空 为已连接的端口显示做准备
        if len(port_list) > 0: #if port
            for port in port_list:
                self.COMInput.addItems([port[0]]) #port[0]表示设备名(COM1,2,3)
    
        if len(port_list) <= 0:
            self.COMInput.addItems(['无串口'])
    
    #打开串口
    def OpenButtonOperation(self):
        self.ser.port     = self.COMInput.currentText() #获取当前串口号
        self.ser.baudrate = self.Baudrate.currentText() #波特率
        Databits = self.DataBits.currentText() #数据位
        if Databits   == 8:
            self.ser.bytesize = serial.EIGHTBITS
        elif Databits == 7:
            self.ser.bytesize = serial.SEVENBITS
        elif Databits == 6:
            self.ser.bytesize = serial.SIXBITS
        else:
            self.ser.bytesize = serial.FIVEBITS
        
        CheckBits = self.CheckBits.currentText() #校验位
        if CheckBits   == 'None':
            self.ser.parity = serial.PARITY_NONE
        elif CheckBits == "ODD":
            self.ser.parity = serial.PARITY_ODD
        elif CheckBits == "EVEN":
            self.ser.parity = serial.PARITY_EVEN
        
        StopBits = self.StopBits.currentText() #停止位
        if StopBits == "1":
            self.ser.stopbits = serial.STOPBITS_ONE
        else:
            self.ser.stopbits = serial.STOPBITS_TWO
        
        try:
            time.sleep(0.1) #等待10ms 打开串口
            self.ser.open() 
        except:
            QMessageBox.critical(self, "串口异常" , "不能被打开") #title, text
            return None
        
        if self.ser.is_open:
            self.OpenButton.setEnabled(False)
            self.receive_area.append('串口已打开')

        #串口一旦打开 就开始接收消息
        self.timer = QTimer()
        self.timer.setInterval(1) #定时1ms一次 
        self.timer.timeout.connect(self.DataReceiving)
        self.timer.start()

    #各种信号槽函数处理
    def SignalProcessing(self):
        self.AutoDetect.clicked.connect(self.AutoDetectOperation) #端口检测
        self.OpenButton.clicked.connect(self.OpenButtonOperation) #串口打开&&数据接收
        self.CloseButton.clicked.connect(self.PortClose) #串口关闭
        self.send_button.clicked.connect(self.DataSending) #数据发送
        self.ClearButton.clicked.connect(self.ClearReceive) #发送区清空        
        
        #定时发送
        self.TimerSend = QTimer()
        self.TimerSend.timeout.connect(self.DataSending) #定时器开始
        self.CheckSend.stateChanged.connect(self.DataTimerSend) #checkbox状态变化

    def DataTimerSend(self):
        try:
            if 1 <= int(self.Number.text()) <= 30000:
                if  self.CheckSend.isChecked():
                    self.TimerSend.setInterval(int(self.Number.text()))
                    self.TimerSend.start()
                    self.Number.setEnabled(False)
                
                else:
                    self.TimerSend.stop()
                    self.Number.setEnabled(True)
            else:
                QMessageBox.critical(self, "定时发送异常", "设置合理的定时时间")
        except:
            QMessageBox.critical(self, "定时发送异常", "需设置合理的数据类型")
    
    def DataSending(self):
        if self.ser.is_open:
            SendDATA = self.send_area.toPlainText() #获取发送的数据

            if SendDATA != "":
                SendDATA = SendDATA.encode('utf-8')
                self.ser.write(SendDATA)
                length = len(SendDATA)
                self.DataSended += length
                self.TXData.setText(str(self.DataSended))
            else:
                pass
        
        else:
            pass

    def DataReceiving(self):
        # try:
        BufferData = self.ser.in_waiting #缓冲区的数据
        if BufferData > 0:
            # time.sleep(0.1)
            # BufferData = self.ser.in_waiting #延时 消故障 再读一次buffer data
            # if BufferData > 0:
            RealData = self.ser.read(BufferData) #读取数据
            DataLength = len(RealData)
            self.receive_area.append(RealData.decode('ascii'))

            self.DataReceive += DataLength
            self.RXData.setText(str(self.DataReceive))
        else:
            pass
        # except:
        #     QMessageBox.critical(self, "串口异常", "串口数据接收异常,请重新连接设备")
        #     self.PortClose()
        #     return None

    #串口关闭
    def PortClose(self):
        try:
            if self.ser.is_open: #考虑到刚摁下AutoDetec就关闭端口触发except的bug 用if隔开
                self.timer.stop() #接收数据的定时器停止
                self.ser.close() #串口对象关闭
            
            self.TimerSend.stop()
            self.Number.setEnabled(True)
            self.DataReceive = 0 #接收数据计数清零
            self.RXData.setText(str("0"))
            self.DataSended  = 0 #发送数据计数清零
            self.TXData.setText(str("0"))
            #串口基本设置清零并初始化
            self.COMInput.clear()
            self.COMInput.addItems(['COM1', 'COM2', 'COM3', 'COM4', 'COM5'])
            self.Baudrate.clear()
            self.Baudrate.addItems(['9600', '19200', '38400', '115200']) 
            self.DataBits.clear()
            self.DataBits.addItems(['8', '7', '6', '5'])
            self.CheckBits.clear()
            self.CheckBits.addItems(['None', 'ODD', 'EVEN'])
            self.StopBits.clear()
            self.StopBits.addItems(['1', '2'])

        except:
            QMessageBox.critical(self, "串口异常", "串口关闭异常, 请重启程序")
            return None
        
        self.OpenButton.setEnabled(True)

    def ClearReceive(self):
        self.receive_area.clear() #发送区清空

    def ColorChange(self):
        for i in range(1, 11, 4):
            self.V2label[i-1].setStyleSheet("background-color: rgb(0, 255, 0)")
        for j in range(2, 11, 4):
            self.V2label[j-1].setStyleSheet("background-color: rgb(200, 200, 200)")
        for k in range(3, 11, 7):
            self.V2label[k-1].setStyleSheet("background-color: rgb(255, 255, 0)")
        for m in range(4, 11, 4):
            self.V2label[m-1].setStyleSheet("background-color: rgb(255, 0, 0)")

#接收线程
class receive_data(QThread):
    DataDisplay = pyqtSignal(str)

    def __init__(self,ser):
        super().__init__()
        self.ThreadSer = ser

    def run(self):
        while(True):
            # BufferData = self.ThreadSer.in_waiting #缓冲区的数据
            # if BufferData > 0:
                # time.sleep(0.1)
                # BufferData = self.ser.in_waiting #延时 消故障 再读一次buffer data
                # if BufferData > 0:
            RealData = self.ThreadSer.read() #读取数据
            DataLength = len(RealData)
                # self.bs.receive_area.append(RealData.decode('utf-8'))
            print(f"数据为:{RealData.decode('utf-8')}")
                # self.bs.DataReceive += DataLength
                # self.bs.RXData.setText(str(self.bs.DataReceive))
            # else:
                # pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    surface = basicsurf()#basicsurf()
    surface.show()
    sys.exit(app.exec_())