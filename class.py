import sys
import serial
import matplotlib.pyplot as plt
from serial.tools import list_ports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QCheckBox, QComboBox, QTextEdit
from PyQt5.QtGui import QImage, QPixmap

class Window(QWidget):
    #调用Window时候先运行下面的__init__,so加上super().__init__()从而调用
    def __init__(self):
        #从子类中调用父类的方法
        super().__init__()
        #window基础设置
        self.setWindowTitle('OOP lianxi')
        self.resize(480, 480)
        #各个控件的操作函数    
        self.LableOperation()

    def LableOperation(self):
        self.label3 = QLabel(self)
        self.label3.setText('oop sucess')
        self.label3.move(240, 240)


class window(Window):
    #Python类学习---->类属性-->属于类，实例对象属于对象，def之外，class之内的变量  用于不同对象之间共享
    x = 10

    def __init__(self):
        super().__init__()
        self.func()
        self.hh()
        self.xx()
        self.fileoperation()
        self.test(1, 2, 3, 234, 'sdad', 24, 25, name = 'jerry', github = 'http://www.github.com.cn')

    def func(self):
        print("output: \n")
        print(self.label3)

    #Python类学习---->静态方法调用  属于类
    #实例方法(self)、类方法(cls)、静态方法()在内存中都属于类,实例方法为对象所调用x = window(); x.func();
                                                     #后两者为类所调用 window.func()
    @staticmethod
    def hh():
        print('静态方法调用')

    #with关键词学习 
    @staticmethod
    def fileoperation():
        #with将open方法的返回值给f，再执行f.write()方法 
        with open('D:\\QT_test\\test.py', 'r') as f: #可避免文件遇到异常不关断的情况
            pass
            #f.write('with关键词学习')

    #类方法调用  属于类
    @classmethod
    def xx(cls):
        print(f'类方法调用 {cls.x}')

    #不定长参数测试 
    def test(a, b, c, *args, d = 25, **kwargs): #d = 25---->缺省参数  **kwargs必须在在最后面
        print('不定长参数 *args/**kwargs',type(a), type(b), type(c), type(args), type(d), type(kwargs))

app = QtWidgets.QApplication(sys.argv)
y = window()
y.show()
sys.exit(app.exec_())