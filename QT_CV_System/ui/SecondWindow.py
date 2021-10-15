import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import  Qt

class SecondWindow():
    def __init__(self):
        self.window = QWidget()

        self.window.setWindowTitle('参数选择窗口')

        vlayout = QFormLayout()
        self.list = [QLabel(),QSpinBox(),QSpinBox(),QLabel(),QSpinBox(),QSpinBox(),QSpinBox(),QSpinBox(),QSpinBox(),QSpinBox(),QSpinBox()]
        self.str_list = ["算法名称:","低阈值:","高阈值:","算法名称","空间步长:","最小半径:","最大半径:","阈值:","最小圆心距:","画笔宽度:","中心点大小:"]
        self.list[6].setMaximum(10000)
        self.list[0].setText("Canny算法")
        self.list[3].setText("Hough算法")
        self.param2()

        for i in range(len(self.list)):
            vlayout.addRow(self.str_list[i],self.list[i])
        self.btn_yes = QPushButton("确定")
        self.btn_param2 = QPushButton("推荐参数(小图片)")
        self.btn_param1 = QPushButton("推荐参数(大图片)")
        vlayout.addWidget(self.btn_param1)
        vlayout.addWidget(self.btn_param2)
        vlayout.addWidget(self.btn_yes)
        self.btn_param1.clicked.connect(self.param1)
        self.btn_param2.clicked.connect(self.param2)
        self.window.setLayout(vlayout)

    def param2(self):
        self.list[1].setValue(10)
        self.list[2].setValue(45)
        self.list[3].setText("Hough算法")
        self.list[4].setValue(3)
        self.list[5].setValue(5)
        self.list[6].setValue(500)
        self.list[7].setValue(15)
        self.list[8].setValue(50)
        self.list[9].setValue(1)
        self.list[10].setValue(1)

    def param1(self):
        self.list[1].setValue(20)
        self.list[2].setValue(50)
        self.list[3].setText("Hough算法")
        self.list[4].setValue(5)
        self.list[5].setValue(10)
        self.list[6].setValue(1000)
        self.list[7].setValue(50)
        self.list[8].setValue(500)
        self.list[9].setValue(10)
        self.list[10].setValue(10)


    def window_exit(self):
        self.message = ""
        for i in range(len(self.list)):
            if i != 0 and i != 3:
                self.message += self.str_list[i] + self.list[i].text() + "\n"
        self.window.close()

    def show(self):
        self.window.show()


if __name__ == "__main__":
    app = QApplication([])
    s = SecondWindow()
    s.show()
    app.exec_()

