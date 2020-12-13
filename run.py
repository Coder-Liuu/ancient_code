import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QMessageBox,QWidget,QPlainTextEdit,QLabel,QBoxLayout
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtWidgets
from DataHelper import DataHelper


class Main:
    def __init__(self):
        self.ui = loadUi("UI/main.ui")
        self.DataHelper = None
        self.ui.btn_choose_data.clicked.connect(self.choose_path)
        self.ui.btn_set_parameter.clicked.connect(self.set_parameter)

        self.ui.btn_spin.addItems(["KMeans","DBSCAN"])
        self.ui.btn_run.clicked.connect(self.run)

    def run(self):
        if(self.DataHelper == None):
            QMessageBox.about(self.ui,"运行失败","请选择你的数据集")
        self.ui.t_ans.setText("运行成功!")

    def choose_path(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self.ui,"请选择你要打开数据的名字","./data/","Csv files(*.csv)") 
        file_name = file_name[0]
        self.DataHelper = DataHelper(file_name)

        name = file_name.split("/")[-1]
        self.ui.ldata_name.setText(name)
        self.show_img()

    def show_img(self):
        self.ui.ldata_shape.setText(str(self.DataHelper.shape))
        self.ui.ldata_class.setText(str(self.DataHelper.class_))

    def set_parameter(self):
        currentText = self.ui.btn_spin.currentText()
        if(currentText == "KMeans"):
            print("----------------")
            # 必须设置为全局变量
            self.newWindow = SecondWindow(algorithm=currentText)
            self.newWindow.show()
        else:
            print("+++++++++++")
        self.show_parameter()

    def show_parameter(self):
        pass


app = QApplication([])
main = Main()
main.ui.show()
app.exec_()

