import sys
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QCheckBox, QMainWindow, QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QImage, QPixmap

x_coordinate = 180
color_settings = "background-color: rgb(58, 111, 50);\n"

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.resize(720, 720)
window.setWindowTitle('Smart Hardware')

#COM端口设置
COM = QLabel(window)
COM.setText('COM端口')
COM.move(20, 25)
box = QtWidgets.QComboBox(window)
box.move(x_coordinate, 20)
box.addItems(['5', '6', '7', '8'])
# label = QtWidgets.QLineEdit(window)
# label.move(110,20)

#Baudurate设置
baud = QLabel(window)
baud.setText('Baudurate波特率')
baud.move(20, 70)
box1 = QtWidgets.QComboBox(window)
box1.move(x_coordinate, 65)
box1.addItems(['9600', '19200', '38400', '115200'])
# label1 = QtWidgets.QLineEdit(window)
# label1.move(110, 65)

#校验位设置
CRC = QLabel(window)
CRC.setText('CRC校验')
CRC.move(20, 115)
box2 = QtWidgets.QComboBox(window)
box2.move(x_coordinate, 110)
box2.addItems(['None', 'Odd', 'Even', 'Mark', 'Space'])
CheckBox = QtWidgets.QCheckBox(window)
CheckBox.move(x_coordinate + 100, 110)
label2 = QtWidgets.QLabel(window)
label2.move(305, 110)
label2.setText('周期发送')

#log显示
LOG = QLabel(window)
LOG.setText('LOG显示')
LOG.move(20, 160)
label3 = QtWidgets.QTextEdit(window)
label3.move(x_coordinate, 155)
label3.resize(250, 250)


#connect显示 灯
light_sts = QLabel(window)
light_sts.setText('Light_sts')
light_sts.move(20, 370)
light = QLabel(window)
light.move(x_coordinate-70, 350)
light.resize(50, 50)  #1.resize正方形 2.setstylesheet(border-radius为长宽的一半)
light.setStyleSheet("background-color: rgb(200, 200, 200);\n"
                    "border-radius: 25px;\n"
                    "border:3px groove gray;\n" #圆边设置
                    "border-style: outset;\n")
btn = QtWidgets.QPushButton(window)
btn.setText('Connect')
btn.pressed.connect(lambda:light.setStyleSheet("background-color: rgb(0, 255, 0);\n"
                                                "border-radius: 25px;\n"
                                                "border:3px groove gray;\n" #圆边设置
                                                "border-style: outset;\n"))

btn.move(x_coordinate,420)
btn1 = QtWidgets.QPushButton(window)
btn1.setText('Send')
btn1.move(320,420)


#图像显示
label_pic = QLabel(window)
label_pic.setPixmap(QPixmap("D:\\NIO.png")) #先Qpixmap加载图片，再setPixmap
label_pic.resize(202, 202)
label_pic.move(450, 200)
label_pic.setScaledContents(True)  




window.show()
sys.exit(app.exec_())

