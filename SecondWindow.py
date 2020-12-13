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
            self.list = [QLabel(),QSpinBox(),QLineEdit()]
            self.str_list = ["算法名称:","聚类簇个数:","最大迭代次数:"]
            self.list[0].setText("Kmeans算法")
            self.list[1].setValue(3)
            self.list[2].setText(str(100))
        elif algorithm == "BIRCH":
            self.list = [QLabel(),QSpinBox(),QLineEdit()]
            self.str_list = ["算法名称:","聚类簇个数:","阈值:"]
            self.list[0].setText("BIRCH算法")
            self.list[1].setValue(3)
            self.list[2].setText(str(0.5))
        elif algorithm == "DBSCAN":
            self.list = [QLabel(),QDoubleSpinBox(),QLineEdit()]
            self.str_list = ["算法名称:","距离阈值:","样本数阈值:"]
            self.list[0].setText("DBSCAN算法")
            self.list[1].setValue(2)
            self.list[2].setText(str(2))
        elif algorithm == "GMM":
            self.list = [QLabel(),QSpinBox(),QLineEdit()]
            self.str_list = ["算法名称:","聚类簇个数:","最大迭代次数:"]
            self.list[0].setText("GMM算法")
            self.list[1].setValue(3)
            self.list[2].setText(str(100))
        elif algorithm == "OPTICS":
            self.list = [QLabel(),QDoubleSpinBox(),QLineEdit()]
            self.str_list = ["算法名称:","最小样本数:","最大密度:"]
            self.list[0].setText("OPTICS算法")
            self.list[1].setValue(2)
            self.list[2].setText(str(2))
        elif algorithm == "MeanShift":
            self.list = [QLabel(),QSpinBox(),QLineEdit()]
            self.str_list = ["算法名称:","随机种子::","最大迭代次数:"]
            self.list[0].setText("MeanShift算法")
            self.list[1].setValue(2)
            self.list[2].setText(str(2))
        elif algorithm == "CLIQUE":
            self.list = [QLabel(),QSpinBox(),QLineEdit()]
            self.str_list = ["算法名称:","网格步长:","密度阈值:"]
            self.list[0].setText("CLIQUE算法")
            self.list[1].setValue(5)
            self.list[2].setText(str(0))

        for i in range(len(self.list)):
            vlayout.addRow(self.str_list[i],self.list[i])
        self.btn_yes = QPushButton("确定")
        vlayout.addWidget(self.btn_yes)
        self.window.setLayout(vlayout)


    def window_exit(self):
        self.message = ""
        for i in range(len(self.list)):
            self.message += self.str_list[i] + self.list[i].text() + "\n"
        self.window.close()

    def show(self):
        self.window.show()


if __name__ == "__main__":
    app = QApplication([])
    s = SecondWindow("KMeans")
    s.show()
    app.exec_()
