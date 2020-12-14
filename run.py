import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox,QWidget,QPlainTextEdit,QLabel,QBoxLayout
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
from DataHelper import DataHelper
from SecondWindow import SecondWindow
from ClusterHelper import ClusterHelper
import pandas as pd
import matplotlib.pyplot as plt
from qtpandas.compat import QtGui
from qtpandas.models.DataFrameModel import DataFrameModel
from qtpandas.views.DataTableView import DataTableWidget


class Main:
    def __init__(self):
        """ 初始化主界面 """
        self.ui = loadUi("UI/main.ui")
        self.DataHelper = None
        self.ui.btn_choose_data.clicked.connect(self.choose_path)
        self.ui.btn_set_parameter.clicked.connect(self.set_parameter)

        self.ui.btn_spin.addItems(["KMeans","BIRCH","DBSCAN","OPTICS","MeanShift","CLIQUE"])
        self.ui.btn_run.clicked.connect(self.run)
        self.cluster = ClusterHelper()
        self.ui.btn_show_image.clicked.connect(self.show_image)

    def show_image(self):
        """ 展示聚类结果 """
        try:
            self.cluster.imshow()
        except:
            QMessageBox.about(self.ui,"展示失败","请先训练你的聚类器")

    def choose_path(self):
        """ 选择数据集 """
        file_name = QtWidgets.QFileDialog.getOpenFileName(self.ui,"请选择你要打开数据的名字","./data/","Csv files(*.csv)") 
        file_name = file_name[0]
        self.DataHelper = DataHelper(file_name)

        name = file_name.split("/")[-1]
        self.ui.ldata_name.setText(name)
        self.show_information()
        self.show_data()

    def show_information(self):
        """ 显示数据集的基本信息 """
        self.ui.ldata_shape.setText(str(self.DataHelper.shape))
        self.ui.ldata_class.setText(str(self.DataHelper.class_))

    def set_parameter(self):
        """ 设置分类器 """
        currentText = self.ui.btn_spin.currentText()
        self.newWindow = SecondWindow(algorithm=currentText)
        self.newWindow.btn_yes.clicked.connect(self.get_parameter)
        self.newWindow.show()

    def get_parameter(self):
        """ 获得参数信息 """
        self.newWindow.window_exit()

        self.ui.tmessage_show.setText(self.newWindow.message)
        currentText = self.ui.btn_spin.currentText()
        param_dict = [eval(line.split(":")[1]) for line in self.newWindow.message.split("\n")[1:-1]]
        self.cluster.set_Cluster(currentText,param_dict)


    def show_data(self):
        """
        展示读取进来的数据
        """
        self.widget = DataTableWidget(self.ui)
        model = DataFrameModel()
        model.setDataFrame(self.DataHelper.data)
        self.widget.setViewModel(model)
        self.widget.move(30,200)
        self.widget.resize(350,350)
        self.widget.show()

    def run(self):
        """ 运行聚类算法 """
        if(self.DataHelper == None):
            QMessageBox.about(self.ui,"运行失败","请选择你的数据集")
        elif(self.cluster.cluster == None ):
            QMessageBox.about(self.ui,"运行失败","请初始化你的聚类器")
        else:
            self.cluster.fit(self.DataHelper.data)
            score = self.cluster.get_score()
            text = ""
            for item in score.items():
                text += item[0] + str(item[1]) + "\n"
            self.ui.t_ans.setText(text)


app = QApplication([])
main = Main()
main.ui.show()
app.exec_()
