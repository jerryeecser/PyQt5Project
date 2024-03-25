#基本控件显示的包 包括QLabel, QComboX
import sys
import serial
import socket
from PyQt5 import QtWidgets 
from serial.tools import list_ports
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QGroupBox, QLabel, QCheckBox, QComboBox, QLineEdit, QTextEdit, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QThread


#界面整体布局
class basicsurf(QWidget):
    def __init__(self):
        super().__init__()
        #变量定义
        self.x_coordinate = 180
        self.TCPEND = True
        self.init_ui()

    def init_ui(self):    
        #window基本设置
        self.setWindowTitle('EfuseControl GUI')
        self.resize(360, 360)
        self.FirstRow()
        self.SecondRow()
        self.ThirdRow()
        self.FourthRow()

        #总体布局设置
        self.ContainerOperation()

    def FirstRow(self):
        self.Container = QHBoxLayout() #总体垂直布局
        
        self.V1GroupBox = QGroupBox('') #组布局
        self.V1Layout = QVBoxLayout() #垂直组创建
        
        self.IdLabel = QLabel(self) #EfuseID
        self.IdLabel.setText('EfuseId')
        self.V1Layout.addWidget(self.IdLabel)

        for i in range(1, 11):
            #exec()创建动态变量
            # exec(f'self.TextLabel{i}1 = QTextEdit(self)')
            # self.V1Layout.addWidget(getattr(self, f'TextLabel{i}1')) #getattr()获取动态创建的变量
            label = QLineEdit(self)
            label.setObjectName(f'TextLabel{i}1')
            self.V1Layout.addWidget(label)

        self.V1GroupBox.setLayout(self.V1Layout)        

    def SecondRow(self):
        #第二列的组
        self.V2GroupBox = QGroupBox('') 
        self.V2Layout = QVBoxLayout()

        self.StatusLabel = QLabel(self) #EfuseStatus
        self.StatusLabel.setText('EfuseStatus')
        self.V2Layout.addWidget(self.StatusLabel)
        
        for i in range(1, 11):
            light = QLabel(self)
            light.setObjectName(f'LightLabel{i}1')
            light.resize(50, 50)
            light.setStyleSheet("background-color: rgb(200, 200, 200);\n"
                                "border-radius: 25px;\n"
                                "border:3px groove gray;\n" #圆边设置
                                "border-style: outset;\n")
            self.V2Layout.addWidget(light)
        
        self.V2GroupBox.setLayout(self.V2Layout)

    
    def ThirdRow(self):
        self.V3GroupBox = QGroupBox('') 
        self.V3Layout = QVBoxLayout()

        self.CurrentLabel = QLabel(self) #Current
        self.CurrentLabel.setText('Current')
        self.V3Layout.addWidget(self.CurrentLabel)

        for i in range(1, 11):
            label3 = QLineEdit(self)
            label3.setObjectName(f'TextLabel{i}3')
            label3.resize(5, 5)
            self.V3Layout.addWidget(label3)

        self.V3GroupBox.setLayout(self.V3Layout)

    
    def FourthRow(self):
        self.V4GroupBox = QGroupBox('') 
        self.V4Layout = QVBoxLayout()

        self.VoltageLabel = QLabel(self) #Voltage
        self.VoltageLabel.setText('Voltage')
        self.V4Layout.addWidget(self.VoltageLabel)

        for i in range(1, 11):
            label4 = QLineEdit(self)
            label4.setObjectName(f'TextLabel{i}3')
            label4.resize(5, 5)
            self.V4Layout.addWidget(label4)

        self.V4GroupBox.setLayout(self.V4Layout)

        self.V5GroupBox = QGroupBox('') 
        self.V5Layout = QHBoxLayout()
        self.edit = QLineEdit(self)
        self.V5Layout.addWidget(self.edit)
        self.V5GroupBox.setLayout(self.V5Layout)
        
    # def QLabelOperation2(self):
    #     #第二列的组
    #     self.V2GroupBox = QGroupBox('')
    #     self.V2Layout = QVBoxLayout()

    #     for j in range(1, 11):
    #         exec(f'TextLabel{j}1 = QLabel(self)')
    #         self.V2Layout.addWidget(getattr(self, f'TextLabel{j}1'))
        
    #     self.V2GroupBox.setLayout(self.V2Layout)

    def ContainerOperation(self):
        self.Container.addWidget(self.V1GroupBox)
        self.Container.addWidget(self.V2GroupBox)
        self.Container.addWidget(self.V3GroupBox)
        self.Container.addWidget(self.V4GroupBox)
        self.Container.addWidget(self.V5GroupBox)
        self.setLayout(self.Container)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    surface = basicsurf()#basicsurf()

    surface.show()
    sys.exit(app.exec_())