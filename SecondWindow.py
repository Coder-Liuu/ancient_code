import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import  Qt

class SecondWindow():
    def __init__(self,algorithm):
        self.window = QWidget()

        # self.window.resize(300, 500)
        self.window.setWindowTitle('参数选择窗口')

        vlayout = QFormLayout()

        if algorithm == "KMeans":
            self.l1 = QLabel("Kmeans算法")
            self.l2 = QSpinBox()
            self.l3 = QLineEdit()
            self.btn_yes = QPushButton("确定")
            vlayout.addRow("算法名称:",self.l1)
            vlayout.addRow("聚类簇个数:",self.l2)
            vlayout.addRow("最大迭代次数:",self.l3)
            vlayout.addWidget(self.btn_yes)
        elif algorithm == "BIRCH":
            self.l1 = QLabel("BIRCH算法")

        self.window.setLayout(vlayout)

    def show(self):
        self.window.show()

app = QApplication([])
s = SecondWindow("KMeans")
s.show()
app.exec_()
