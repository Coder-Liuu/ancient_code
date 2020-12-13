import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox,QWidget,QPlainTextEdit,QLabel,QBoxLayout
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from DataHelper import DataHelper
from SecondWindow import SecondWindow
from ClusterHelper import ClusterHelper




class Main:
    def __init__(self):
        self.ui = loadUi("UI/main.ui")
        self.DataHelper = None
        self.ui.btn_choose_data.clicked.connect(self.choose_path)
        self.ui.btn_set_parameter.clicked.connect(self.set_parameter)

        self.ui.btn_spin.addItems(["KMeans","DBSCAN"])
        self.ui.btn_run.clicked.connect(self.run)
        self.cluster = ClusterHelper()

    def choose_path(self):
        """ 选择数据集 """
        file_name = QtWidgets.QFileDialog.getOpenFileName(self.ui,"请选择你要打开数据的名字","./data/","Csv files(*.csv)") 
        file_name = file_name[0]
        self.DataHelper = DataHelper(file_name)

        name = file_name.split("/")[-1]
        self.ui.ldata_name.setText(name)
        self.show_information()

    def show_information(self):
        """ 显示数据集的基本信息 """
        self.ui.ldata_shape.setText(str(self.DataHelper.shape))
        self.ui.ldata_class.setText(str(self.DataHelper.class_))

    def set_parameter(self):
        """ 设置分类器 """
        currentText = self.ui.btn_spin.currentText()
        if(currentText == "KMeans"):
            self.cluster.set_Cluster("KMeans")
            print("----------------")
            # 必须设置为全局变量
            self.newWindow = SecondWindow(algorithm=currentText)
            self.newWindow.show()
        else:
            print("+++++++++++")
        self.show_parameter()

    def show_parameter(self):
        pass

    def run(self):
        """ 运行聚类算法 """

        self.cluster.fit(self.DataHelper.data)
        if(self.DataHelper == None):
            QMessageBox.about(self.ui,"运行失败","请选择你的数据集")
        score = self.cluster.get_score()
        text = ""
        for item in score.items():
            text += item[0] + str(item[1]) + "\n"
        self.ui.t_ans.setText(text)

app = QApplication([])
main = Main()
main.ui.show()
app.exec_()

