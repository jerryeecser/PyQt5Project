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
        self.resize(810, 810)
        self.FirstRow()
        # self.QLabelOperation2()
        self.QtextOperation()
        

        #总体布局设置
        self.ContainerOperation()

    def FirstRow(self):
        self.Container = QVBoxLayout() #总体垂直布局
        
        self.HGroupBox = QGroupBox('LABEL') #组布局
        self.HLayout = QHBoxLayout() #水平组创建
        
        self.IdLabel = QLabel(self) #EfuseID
        self.IdLabel.setText('EfuseId')

        self.StatusLabel = QLabel(self) #EfuseStatus
        self.StatusLabel.setText('EfuseStatus')
        
        self.CurrentLabel = QLabel(self) #Current
        self.CurrentLabel.setText('Current')
        
        self.VoltageLabel = QLabel(self) #Voltage
        self.VoltageLabel.setText('Voltage')
        
        self.HLayout.addWidget(self.IdLabel)
        self.HLayout.addWidget(self.StatusLabel)
        self.HLayout.addWidget(self.CurrentLabel)
        self.HLayout.addWidget(self.VoltageLabel)
        #添加到水平布局
        self.HGroupBox.setLayout(self.HLayout)
        

    def QtextOperation(self):
        #第一列的组
        self.V1GroupBox = QGroupBox('') 
        self.V1Layout = QVBoxLayout()

        for i in range(1, 11):
            #exec()创建动态变量
            # exec(f'self.TextLabel{i}1 = QTextEdit(self)')
            # self.V1Layout.addWidget(getattr(self, f'TextLabel{i}1')) #getattr()获取动态创建的变量
            label = QTextEdit(self)
            label.setObjectName(f'TextLabel{i}1')
            label.resize(5, 5)
            self.V1Layout.addWidget(label)

        self.V1GroupBox.setLayout(self.V1Layout)
    
    # def QLabelOperation2(self):
    #     #第二列的组
    #     self.V2GroupBox = QGroupBox('')
    #     self.V2Layout = QVBoxLayout()

    #     for j in range(1, 11):
    #         exec(f'TextLabel{j}1 = QLabel(self)')
    #         self.V2Layout.addWidget(getattr(self, f'TextLabel{j}1'))
        
    #     self.V2GroupBox.setLayout(self.V2Layout)

    def ContainerOperation(self):
        self.Container.addWidget(self.HGroupBox)
        self.Container.addWidget(self.V1GroupBox)
        # self.Container.addWidget(self.V2GroupBox)
        self.setLayout(self.Container)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    surface = basicsurf()#basicsurf()

    surface.show()
    sys.exit(app.exec_())