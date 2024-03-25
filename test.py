#基本控件显示的包 包括QLabel, QComboX
import sys
import serial
import socket
from PyQt5 import QtWidgets
from serial.tools import list_ports
from PyQt5.QtWidgets import QWidget, QLabel, QCheckBox, QComboBox, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QThread


#tcp_server线程
class tcp_server_thread(QThread):
    server_stop = pyqtSignal(str) 
    #自定义的信号只能放在类属性中，函数之外
    MsgOnReminder = pyqtSignal(str)
    MsgDisplay = pyqtSignal(str)
    MsgOffReminder = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.ipport = basicsurf()
        #获取IP PORT
        self.IP_PORT = [str(self.ipport.label4.text()), int(self.ipport.label5.text())]

    def run(self):
        #创建一个套接字
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #绑定IP和端口号
        server.bind(tuple(self.IP_PORT))
        #开始监听，绑定最大连接数
        server.listen(5)
        while(True):
            client_socket, client_addr = server.accept()
            MsgOn = '一个新的客户端到来%s' %str(client_addr)
            self.MsgOnReminder.emit(MsgOn) #新的Client接入提醒
            while(True):
                #接收client的数据 b
                data = client_socket.recv(1024).decode('utf-8')
                if data:
                    print('recevied: %s' %data)
                    self.MsgDisplay.emit(data) #发送信号
                else:
                    break
            MsgOff = "本次服务完毕\n等待新的客户端连接\n-------"
            self.MsgOffReminder.emit(MsgOff) #结束提示
            client_socket.close()
        server.close()

#tcp_client线程
class tcp_client_thread(QThread):
    client_stop = pyqtSignal(str) 

    def __init__(self):
        super().__init__()
        self.ipport = basicsurf()
        #获取IP PORT
        self.IP_PORT = [str(self.ipport.label4.text()), int(self.ipport.label5.text())]
        #创建一个套接字TCP
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #连接服务器
        self.client.connect(tuple(self.IP_PORT))
        
    def run(self):
        pass

#界面整体布局
class basicsurf(QWidget):

    def __init__(self):
        super().__init__()
        #变量定义
        self.x_coordinate = 180
        self.TCPEND = True
        #window基本设置
        self.setWindowTitle('Hardware Testing GUI')
        self.resize(820, 820)
        #调用控件基本设置的函数
        self.LabelOperation()
        self.ComboxOperation()
        self.CheckBoxOperation()
        self.QTextOperation()
        self.ButtonOperation()
        
    #标签、灯、图片
    def LabelOperation(self):
        #COM端口设置
        self.label1 = QLabel(self) #COM端口设置
        self.label1.setText('COM端口')
        self.label1.move(20, 25)

        #Baudurate设置
        self.baud = QLabel(self)
        self.baud.setText('Baudurate波特率')
        self.baud.move(20, 70)
        
        #校验位设置
        self.CRC = QLabel(self)
        self.CRC.setText('CRC校验')
        self.CRC.move(20, 115)
        self.label2 = QLabel(self)
        self.label2.move(305, 110)
        self.label2.setText('周期发送')

        #log显示
        self.LOG = QLabel(self)
        self.LOG.setText('LOG显示')
        self.LOG.move(20, 160)

        #light图标显示
        self.light_sts = QLabel(self)
        self.light_sts.setText('Light_sts')
        self.light_sts.move(20, 370)
        self.light = QLabel(self)
        self.light.move(self.x_coordinate-70, 350)
        self.light.resize(50, 50)  #1.resize正方形 2.setstylesheet(border-radius为长宽的一半)
        self.light.setStyleSheet("background-color: rgb(200, 200, 200);\n"
                            "border-radius: 25px;\n"
                            "border:3px groove gray;\n" #圆边设置
                            "border-style: outset;\n")

        #pic显示
        self.label_pic = QLabel(self)
        self.label_pic.setPixmap(QPixmap("D:\\NIO.png")) #先Qpixmap加载图片，再setPixmap
        self.label_pic.resize(202, 202)
        self.label_pic.move(450, 200)
        self.label_pic.setScaledContents(True)  #图片和label大小自适应

        #ip和port显示
        self.C_S = QLabel(self)
        self.C_S.setText('C/S')
        self.C_S.move(20, 480) 
        self.ip_address = QLabel(self)
        self.ip_address.setText('Ip_Address')
        self.ip_address.move(self.x_coordinate-20, 480)
        self.port = QLabel(self)
        self.port.setText('Port')
        self.port.move(self.x_coordinate-20, 520)

    #多选框
    def ComboxOperation(self):
        #COM端口 ----> 多选框  
        self.box = QComboBox(self) #多选框
        self.box.move(self.x_coordinate, 20)
        self.box.addItems(['COM5', 'COM6', 'COM7', 'COM8', 'NoPort'])

        #Baudurate ----> 多选框
        self.box1 = QComboBox(self)
        self.box1.move(self.x_coordinate, 65)
        self.box1.addItems(['9600', '19200', '38400', '115200'])

        #校验位 ----> 多选框
        self.box2 = QComboBox(self)
        self.box2.move(self.x_coordinate, 110)
        self.box2.addItems(['None', 'Odd', 'Even', 'Mark', 'Space'])

        #Clinet/Server多选框
        self.box3 = QComboBox(self)
        self.box3.move(40, 480)
        self.box3.addItems(['TCP_Client', 'TCP_Server'])

        #IP
    #方形小框    
    def CheckBoxOperation(self):
        #校验位 ----> 方形框
        self.CheckBox = QCheckBox(self)
        self.CheckBox.move(self.x_coordinate + 100, 110)
    
    #文本显示框
    def QTextOperation(self):
        #log显示 ----> 文本显示框
        self.label3 = QTextEdit(self)
        self.label3.move(self.x_coordinate, 155)
        self.label3.resize(250, 250)

        #ip/port显示框
        self.label4 = QLineEdit(self)
        self.label4.move(self.x_coordinate+40, 480)
        self.label4.setText('10.116.40.91')
        
        self.label5 = QLineEdit(self)
        self.label5.move(self.x_coordinate+40, 520)
        self.label5.setText('6789')

        #TCPServer通信显示框
        self.label6 = QTextEdit(self)
        self.label6.move(self.x_coordinate+210, 480)
        self.label6.resize(250, 150)
        #TCPClient
        self.label7 = QTextEdit(self)
        self.label7.move(40, 550)
        self.label7.resize(150, 100)

    #按钮显示
    def ButtonOperation(self):
        #Connect ----> 按钮显示 
        self.btn = QPushButton(self)
        self.btn.setText('Connect')
        self.btn.move(self.x_coordinate, 420)
        #Send ----> 按钮显示
        self.btn1 = QPushButton(self)
        self.btn1.setText('Send')
        self.btn1.move(320,420)
        #端口自动检测按钮
        self.btn2 = QPushButton(self)
        self.btn2.setText('自动检测')
        self.btn2.move(self.x_coordinate + 80, 16)
        #TcpClient/Server打开/清空按钮
        self.btn3 = QPushButton(self)
        self.btn3.setText('连接')
        self.btn3.move(40, 520)
        self.btn4 = QPushButton(self)
        self.btn4.setText('发送')
        self.btn4.move(40, 670)
        #Tcp接收清空
        self.btn5 = QPushButton(self)
        self.btn5.setText('清空')
        self.btn5.move(self.x_coordinate+210, 650)
        

#功能实现
class basicfun(basicsurf):
    my_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.click = True
        #初始化serial对象
        self.ser = serial.Serial()
        #检测串口
        self.AutoPortDetect()
        #Send灯点亮
        self.LightOn()
        #Server接收界面清空
        self.btn5.clicked.connect(lambda: self.label6.clear())
        #Server/Client选择
        self.btn3.clicked.connect(self.ChooseC_S)

    def ChooseC_S(self):
        self.btn3.setText('断开')
        if self.box3.currentText() == 'TCP_Client':
            #Tcp Client通信开始与结束
            self.my_signal.connect(self.slot_msg)#信息发送信号绑定
            self.ClientProcessThread()#Client线程开启
        if self.box3.currentText() == 'TCP_Server':
            #Tcp Server通信开始与结束
            self.msgthread = tcp_server_thread() #必须加上self因为不加---->结束程序的时候线程仍然继续运行会报错，加上则表示属于surface对象，surface结束即线程结束
            #绑定Server信号和槽函数
            self.msgthread.MsgOnReminder.connect(self.slot_ServerReminder)
            self.msgthread.MsgDisplay.connect(self.slot_MsgDis)
            self.msgthread.MsgOffReminder.connect(self.slot_ServerOff)
            self.msgthread.start()
            
    #端口检测
    def PortDetec(self):
        port_list = list(list_ports.comports()) #port list转化为列表形式 port_list = [[com1, xxx], [com2, xxx]]
        self.box.clear() #将原有box中的元素清空 为已连接的端口显示做准备
        if len(port_list) > 0: #if port
            for port in port_list:
                self.box.addItems([port[0]]) #port[0]表示设备名(COM1,2,3)
    
        if len(port_list) <= 0:
            self.box.addItems(['NoPort'])
    
    #TCP通信
    def TcpServerCom(self):
        self.btn3.clicked.connect(self.ServerProcessThread)
    
    #开始Server线程
    def ServerProcessThread(self):
        #---->结束程序的时候线程仍然继续运行会报错，加上则表示属于surface对象，surface结束即线程结束
        self.msgthread.start()


    #开始Client线程
    def ClientProcessThread(self):
        #连接server
        self.clientthread = tcp_client_thread()#连接Server
        self.btn4.clicked.connect(lambda: self.my_signal.emit('msg')) #msg发送

    
    #Client数据发送
    def slot_msg(self, msg):
        MSG = self.label7.toPlainText()
        self.clientthread.client.send(MSG.encode('utf-8'))#发送的数据为encode转换为二进制b
        #print(self.box3.currentText())
    
    #Client连接提示槽函数
    def slot_ServerReminder(self, msg):
        self.label6.append(msg)

    #Server显示的槽函数
    def slot_MsgDis(self, msg):
        #append自带切换行
        self.label6.append(msg)

    #Client断开提升槽函数
    def slot_ServerOff(self, msg):
        self.label6.append(msg)

    #灯亮
    def LightOn(self):
        self.btn.pressed.connect(lambda:self.light.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                                                 "border-radius: 25px;\n"
                                                                 "border:3px groove gray;\n" #圆边设置
                                                                 "border-style: outset;\n"))
    
    #端口自动检测
    def AutoPortDetect(self):
        self.btn2.clicked.connect(self.PortDetec)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    surface = basicfun()#basicsurf()

    surface.show()
    sys.exit(app.exec_())

