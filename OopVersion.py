#当一个控件里有多子控件需要管理的时候，可使用面向对象的思想简化程序设计
#pyqt5中常用的思想
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel
import sys

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
        label3 = QLabel(self)
        label3.setText('oop sucess')
        label3.move(240, 240)

if __name__ == "__main__":
    #1.创建应用程序对象
    app = QtWidgets.QApplication(sys.argv)

    window = Window()

    # window = QtWidgets.QWidget()
    # window.resize(480, 480)
    # label1 = QtWidgets.QLabel(window)
    # label1.setText('hello nio')
    # label1.move(200, 300)
    # label2 = QtWidgets.QLabel(window)
    # label2.setText('hello again')
    # label2.move(60, 80)

    window.show()
    sys.exit(app.exec_())