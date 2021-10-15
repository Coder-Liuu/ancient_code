import cv2
import numpy as np
import matplotlib.pyplot as plt
from canny import Canny
from hough import HoughCircles
from utils import show, save

# 要检测图片的名称，运行程序后结果会保存到当前文件目录下。
path = "picture"

img = cv2.imread(f"data/{path}.jpg", 0)
color_img = cv2.imread(f"data/{path}.jpg")

canny = Canny()
edge = canny.detect(img, sigma=1, kernel_size=5, lowthreshold=20, highthreshold=50)
print("边缘检测完毕")
save(edge,"result-edge")

hough = HoughCircles(color_img, edge, step=5, r_min=10, r_max=1000, thoushld=50, minDist=500)
circles = hough.detect()
color_img,_ = hough.paint_circles(circles,10,Text=False)
print(f"一共有圆{len(circles)}个")
save(color_img,"result")
