"""
步骤2：在边缘图上利用Hough变换计算圆心与半径
① 建立参数空间
② 依据`边缘点`的梯度方向对参数空间进行投票
③ 依据预设定的投票阈值筛选出初步结果
④ 对已筛选出的结果进行非极大化抑制，得到精确的参数（圆心和半径）
"""

import skimage
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import ndimage
from copy import deepcopy
import math


class HoughCircles():
    """ Hough圆检测算法的实现 """

    def __init__(self, img, edge_image, step, r_min, r_max, thoushld, minDist):
        """
        Parameters:
            img: 原始图片
            edge_image: 图像边缘信息
            step: Hough空间的步长
            r_max: 半径的最大值
            r_min: 半径的最大值
            thoushld: 阈值
            minDist: 两个圆心之间最小的距离
        """
        self.img = img
        self.edge_image = edge_image
        self.angle = self.sobel_filiter(img)
        self.step = step
        self.r_min = math.floor(r_min / step) * step
        self.r_max = r_max
        self.thoushld = thoushld
        self.minDist = minDist

    def sobel_filiter(self, img):
        """ 使用sobel算子对图片进行滤波 """
        b, g, r = img[:,:,0], img[:,:,1], img[:,:,2]
        img = 0.2989 * r + 0.5870 * g + 0.1140 * b
        kx = np.array([[-1,0,1],[-2,0,2],[-1,0,1]],np.float32)
        ky = np.array([[1,2,1],[0,0,0],[-1,-2,-1]],np.float32)
        ix = ndimage.filters.convolve(img, kx)
        iy = ndimage.filters.convolve(img, ky)
        theta = np.arctan2(iy,ix)
        return np.pi - theta

    def hough_soft_vote(self):
        """ Hough变换使用软投票法对参数空间进行投票 """
        def ceil(x):
            return math.ceil(x)
        def floor(x):
            return math.floor(x)

        h, w = self.edge_image.shape
        angle_sin = np.sin(self.angle)
        angle_cos = np.cos(self.angle)
        step = self.step
        r_max = self.r_max

        # 进行投票累加
        accumulator = np.zeros((ceil(h / step) + 1, ceil(w / step) + 1, ceil(r_max / step) + 1))
        for x in range(1, h - 1):
            for y in range(1, w - 1):
                if self.edge_image[x][y] != 0:
                    ii = x
                    jj = y
                    r = self.r_min
                    gs = angle_sin[x][y]
                    gc = angle_cos[x][y]
                    while ii >= 0 and jj >= 0 and ii < h and jj < w and r < r_max / step:
                        i_step,j_step,r_step = floor(ii / step), floor(jj / step), floor(r / step)
                        accumulator[i_step][j_step][r_step] += 0.7
                        accumulator[i_step - 1][j_step][r_step] += 0.05
                        accumulator[i_step][j_step - 1][r_step] += 0.05
                        accumulator[i_step][j_step][r_step - 1] += 0.05
                        accumulator[i_step + 1][j_step][r_step] += 0.05
                        accumulator[i_step][j_step + 1][r_step] += 0.05
                        accumulator[i_step][j_step][r_step + 1] += 0.05
                        ii += step * gs
                        jj += step * gc
                        r += step
                    ii = x - step * gs
                    jj = y - step * gc
                    r = self.r_min
                    while ii >= 0 and jj >= 0 and ii < h and jj < w and r < r_max / step:
                        i_step,j_step,r_step = floor(ii // step), floor(jj // step), floor(r // step)
                        accumulator[i_step][j_step][r_step] += 0.7
                        accumulator[i_step - 1][j_step][r_step] += 0.05
                        accumulator[i_step][j_step - 1][r_step] += 0.05
                        accumulator[i_step][j_step][r_step - 1] += 0.05
                        accumulator[i_step + 1][j_step][r_step] += 0.05
                        accumulator[i_step][j_step + 1][r_step] += 0.05
                        accumulator[i_step][j_step][r_step + 1] += 0.05
                        ii -= step * gs
                        jj -= step * gc
                        r += step
        print("参数空间中最大投票数为：",accumulator.max())
        mmax = accumulator.max()
        index = np.argwhere(accumulator >= self.thoushld)
        index = index * step + step / 2
        if len(index) == 0:
            print("[Waring] 没有圆")
        return index

    def non_max_suppression(self, index):
        """
        非极大抑制，抑制圆心向近的圆
        Parameters:
            index: 初步检测出来的结果
        """
        x, y, r = index[0]
        possible = []
        result = []
        for circle in index:
            if abs(circle[0] - x) <= self.minDist and abs(circle[1] - y) <= self.minDist:
                possible.append([circle[0],circle[1],circle[2]])
            else:
                mean_circle = np.array(possible).mean(axis=0)
                result.append([mean_circle[0], mean_circle[1], mean_circle[2]])
                possible.clear()
                x, y, r = circle
                possible.append([x, y, r])
        mean_circle = np.array(possible).mean(axis=0)
        result.append([mean_circle[0], mean_circle[1], mean_circle[2]])
        return result

    def detect(self):
        """ 执行Hough检测算法 """
        print("begin hough transform")
        result = self.hough_soft_vote()
        # result = self.non_max_suppression(result)
        return result

    def paint_circles(self, circles, wide, centre=10, Text = True):
        """ 在彩色图片中绘制圆 """
        color_img = deepcopy(self.img)
        s = []
        for i, circle in enumerate(circles):
            y = int(circle[0])
            x = int(circle[1])
            r = int(circle[2])
            s1 = f"圆{i+1}: 圆心坐标为(x:{x},y:{y}) 半径为:{r}"
            s.append(s1)
            color_img = cv2.circle(color_img, (x, y), r, (255, 0, 0), wide)
            color_img = cv2.circle(color_img, (x, y), centre, (255, 0, 0), -1)
            if Text:
                cv2.putText(color_img,f"x:{x},y:{y},r:{r}",(x - 300, y + 300),cv2.FONT_HERSHEY_PLAIN, 5.0, (0, 0, 255), 5)
        if Text:
            return color_img
        else:
            return color_img, s


if __name__ == "__main__":
    path = "picture"
    img = cv2.imread(f"../data/{path}.jpg", 0)
    color_img = cv2.imread(f"../data/{path}.jpg")

    edge = cv2.Canny(img, 100, 200)
    hough = HoughCircles(color_img, edge, step=5, r_min=10, r_max=1000, thoushld=50, minDist=200)
    circles = hough.detect()
    color_img = hough.paint_circles(circles,10)
    print("程序结束")

    cv2.namedWindow('input image', cv2.WINDOW_FREERATIO)
    cv2.imshow("input image", color_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
