import sys
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import  Qt

class SecondWindow():
    def __init__(self,algorithm):
        self.window = QWidget()

        self.window.setWindowTitle('参数选择窗口')

        vlayout = QFormLayout()

        if algorithm == "KMeans":
            self.l1 = QLabel("Kmeans算法")
            self.l2 = QSpinBox()
            self.l3 = QLineEdit()
            self.btn_yes = QPushButton("确定")

            self.l2.setValue(3)
            self.l3.setText(str(100))

            vlayout.addRow("算法名称:",self.l1)
            vlayout.addRow("聚类簇个数:",self.l2)
            vlayout.addRow("最大迭代次数:",self.l3)
            vlayout.addWidget(self.btn_yes)

        elif algorithm == "BIRCH":
            self.l1 = QLabel("BIRCH算法")

        self.window.setLayout(vlayout)


    def window_exit(self):
        self.message = "算法名称:"+self.l1.text() + "\n聚类簇个数" + self.l2.text() + "\n最大迭代次数" + self.l3.text()
        self.window.close()

    def show(self):
        self.window.show()


if __name__ == "__main__":
    app = QApplication([])
    s = SecondWindow("KMeans")
    s.show()
    app.exec_()
