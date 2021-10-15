from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
from skimage import io
from ui.SecondWindow import SecondWindow
from canny import Canny
from hough import HoughCircles


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.ui = loadUi('ui/main.ui', self)
        self.setParam()
        self.ui.setParam_bt.clicked.connect(self.setParam_windows)

        self.ui.load_image.clicked.connect(self.load_image_func)
        self.ui.gaussian_filiter_bt.clicked.connect(self.gaussian_filiter)
        self.ui.sobel_filiter_bt.clicked.connect(self.sobel_filiter)
        self.ui.non_max_suppression_bt.clicked.connect(
            self.non_max_suppression)
        self.ui.threshold_bt.clicked.connect(self.threshold)
        self.ui.canny_bt.clicked.connect(self.canny_detect)

        self.ui.soft_vote_bt.clicked.connect(self.soft_vote)
        self.ui.non_max_suppression_bt2.clicked.connect(
            self.non_max_suppression_2)
        self.ui.hough_bt.clicked.connect(self.hough_detect)

        self.ui.execute_bt.clicked.connect(self.execute)
        self.ui.enlarge_bt.clicked.connect(self.enlarge)

        self.handle_image = None
        self.show_image("ui/bg.png")

    def setParam_windows(self):
        self.newWindow = SecondWindow()
        self.newWindow.btn_yes.clicked.connect(self.get_parameter)
        self.newWindow.show()

    def get_parameter(self):
        self.newWindow.window_exit()
        param_dict = [eval(line.split(":")[1])
                      for line in self.newWindow.message.split("\n")[:-1]]
        print("参数:",param_dict)
        self.lowthreshold = param_dict[0]
        self.highthreshold = param_dict[1]
        self.step = param_dict[2]
        self.r_min = param_dict[3]
        self.r_max = param_dict[4]
        self.thoushld = param_dict[5]
        self.minDist = param_dict[6]
        self.paint_wide = param_dict[7]
        self.paint_centre = param_dict[8]


    def setParam(self):
        self.lowthreshold = 10
        self.highthreshold = 45
        self.step = 3
        self.r_min = 5
        self.r_max = 500
        self.thoushld = 15
        self.minDist = 50
        self.paint_wide = 1
        self.paint_centre = 1

    def enlarge(self):
        path = ".cache/handle_image.jpg"
        img = cv2.imread(path)
        cv2.namedWindow('image', cv2.WINDOW_FREERATIO)
        cv2.imshow("image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def execute(self):
        self.canny_detect()
        self.hough_detect()

    def hough_detect(self):
        self.hough = HoughCircles(self.color_image, self.handle_image, step=self.step, r_min=self.r_min, r_max=self.r_max, thoushld=self.thoushld, minDist=self.minDist)
        self.index = self.hough.hough_soft_vote()
        result = self.hough.non_max_suppression(self.index)
        tmp, s = self.hough.paint_circles(result, self.paint_wide, centre=self.paint_centre, Text=False)
        path = ".cache/handle_image.jpg"
        cv2.imwrite(path, tmp)
        self.show_image(path)
        self.ui.resut_text.setText("\n".join(s))

    def non_max_suppression_2(self):
        result = self.hough.non_max_suppression(self.index)
        tmp, s = self.hough.paint_circles(
            result, self.paint_wide, centre=self.paint_centre, Text=False)
        path = ".cache/handle_image.jpg"
        cv2.imwrite(path, tmp)
        self.show_image(path)
        self.ui.resut_text.setText("\n".join(s))

    def soft_vote(self):
        self.hough = HoughCircles(self.color_image, self.handle_image, step=self.step,
                                  r_min=self.r_min, r_max=self.r_max, thoushld=self.thoushld, minDist=self.minDist)
        self.index = self.hough.hough_soft_vote()
        tmp, s = self.hough.paint_circles(
            self.index, self.paint_wide, centre=self.paint_centre, Text=False)
        path = ".cache/handle_image.jpg"
        cv2.imwrite(path, tmp)
        self.show_image(path)
        self.ui.resut_text.setText("\n".join(s))

    def canny_detect(self):
        self.handle_image = self.canny.gaussian_filiter(self.handle_image, 1, 3)
        self.handle_image, self.theta = self.canny.sobel_filiter(self.handle_image)
        self.handle_image = self.canny.non_max_suppression(self.handle_image, self.theta)
        self.handle_image, weak, strong = self.canny.threshold(self.handle_image, self.lowthreshold, self.highthreshold, 100)
        self.handle_image = self.canny.hysteresis(self.handle_image, weak, 255)
        path = ".cache/handle_image.jpg"
        cv2.imwrite(path, self.handle_image)
        self.show_image(path)

    def threshold(self):
        self.handle_image, weak, strong = self.canny.threshold(self.handle_image, self.lowthreshold, self.highthreshold, 100)
        self.handle_image = self.canny.hysteresis(self.handle_image, weak, 255)
        path = ".cache/handle_image.jpg"
        cv2.imwrite(path, self.handle_image)
        self.show_image(path)

    def non_max_suppression(self):
        self.handle_image = self.canny.non_max_suppression(self.handle_image, self.theta)
        path = ".cache/handle_image.jpg"
        cv2.imwrite(path, self.handle_image)
        self.show_image(path)

    def sobel_filiter(self):
        self.handle_image, self.theta = self.canny.sobel_filiter(self.handle_image)
        path = ".cache/handle_image.jpg"
        cv2.imwrite(path, self.handle_image)
        self.show_image(path)

    def gaussian_filiter(self):
        self.handle_image = self.canny.gaussian_filiter(self.handle_image, 1, 3)
        path = ".cache/handle_image.jpg"
        cv2.imwrite(path, self.handle_image)
        self.show_image(path)

    def gray(self):
        path = ".cache/handle_image.jpg"
        cv2.imwrite(path, self.handle_image)
        self.show_image(path)

    def show_image(self, image_path):
        lbl = self.ui.image_label
        pixmap = QPixmap(image_path)
        lbl.setPixmap(pixmap)
        lbl.setScaledContents(True)

    def load_image_func(self):
        self.canny = Canny()
        file_name = QtWidgets.QFileDialog.getOpenFileName(
            self.ui, "请选择你要打开图片的名字", "data/", "Image files(*.jpg)")[0]
        image_path = file_name[file_name.find("data"):]
        self.ui.image_path.setText(image_path)
        self.show_image(image_path)
        self.handle_image = cv2.imread(image_path, 0)
        self.color_image = cv2.imread(image_path)

app = QApplication([])
windows = MainWindow()
windows.setWindowTitle('钱币定位系统')
windows.show()
app.exec_()
