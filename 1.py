import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# class Worker(QThread):
#     my_signal = pyqtSignal(str)

#     def __init__(self):
#         super().__init__()
#         #设置工作状态与初始num数值
#         self.num = 0

#     def run(self):
#         while True:
#             #获取文本
#             file_str = 'File index'
#             self.num += 1
#             # 发射信号
#             self.my_signal.emit(file_str)
#             # 线程休眠2秒
#             self.sleep(1)

class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        #设置标题
        self.setWindowTitle('QThread多线程例子')

        #实例化多线程对象
        # self.thread1 = Worker()

        #实例化列表控件与按钮控件
        self.listFile = QListWidget()
        self.btnStart = QPushButton('开始')

        self.label7 = QTextEdit(self)
        self.label7.move(40, 550)
        self.label7.resize(150, 100)
        self.label7.setText('hello nio')
        print(self.label7.toPlainText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = MainWidget()
    demo.show()
    
    sys.exit(app.exec_())
