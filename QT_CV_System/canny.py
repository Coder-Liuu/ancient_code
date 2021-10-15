"""
步骤1：使用Canny 算法提取图像边缘
① 使用高斯滤波器滤波
② 计算图像的梯度图并获得梯度方向
③ 对梯度图进行非极大化抑制
④ 使用双阈值法获得最终的边缘图
"""

import numpy as np
from scipy import ndimage


class Canny:
    """ Canny算法的实现 """

    def gaussian_filiter(self,img ,sigma, kernel_size):
        """ 对图片进行一次高斯滤波
        Parameters:
            img: 原始图片
            sigma: 方差
            kernel_size: 卷积核大小
        """

        kernel_size = int(kernel_size) // 2
        x, y = np.mgrid[-kernel_size:kernel_size+1, -kernel_size:kernel_size+1]
        normal = 1 / (2.0 * np.pi * sigma ** 2)
        g = np.exp(-((x**2 + y ** 2)) / (2.0 * sigma ** 2)) * normal
        g = g / g.sum()
        img = ndimage.filters.convolve(img, g)
        return img

    def sobel_filiter(self, gaussian_img):
        """ 使用sobel算子对图片进行滤波
        Parameters:
            gaussian_img: 高斯过滤后的图片
        returns:
            g: 图片的梯度
            theta: 梯度的方向
        """
        # 水平sobel算子 垂直sobel算子
        kx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], np.float32)
        ky = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], np.float32)
        # 这个卷积不同与深度学习的卷积，这个卷积前需要反转180度
        gaussian_img = np.array(gaussian_img,np.float32)
        ix = ndimage.filters.convolve(gaussian_img, kx)
        iy = ndimage.filters.convolve(gaussian_img, ky)
        # 计算梯度大小
        g = np.hypot(ix, iy)
        g = (g - g.min()) / g.max() * 255
        g = np.array(g,dtype=np.int8)
        # 计算梯度方向 值域-pi到pi => 0 ~ 360
        theta = np.pi - np.arctan2(iy, ix)
        return (g, theta)

    def non_max_suppression(self, g, D):
        """ 对图片进行非极大化抑制
        Parameters:
            g: 梯度大小
            D: 图像梯度的方向
        returns:
            z: 抑制后的图片
        """
        m, n = g.shape
        z = np.zeros((m, n), dtype=np.int32)
        # 弧度(-pi ~ pi) 转 角度 (-180, 180)
        angle = D / np.pi * 180 - 180
        angle[angle < 0] += 180

        for i in range(1, m-1):
            for j in range(1, n-1):
                try:
                    q = 255
                    r = 255
                    # 和梯度方向垂直90度的直线进行对比
                    if (0 <= angle[i, j] < 22.5) or (157.5 <= angle[i, j] <= 180):
                        q = g[i, j+1]
                        r = g[i, j-1]
                    elif (22.5 <= angle[i, j] < 67.5):
                        q = g[i-1, j-1]
                        r = g[i+1, j+1]
                    elif (67.5 <= angle[i, j] < 112.5):
                        q = g[i+1, j]
                        r = g[i-1, j]
                    elif (112.5 <= angle[i, j] < 157.5):
                        q = g[i+1, j-1]
                        r = g[i-1, j+1]

                    if (g[i, j] >= q) and (g[i, j] >= r):
                        z[i, j] = g[i, j]
                    else:
                        z[i, j] = 0
                except IndexError as e:
                    pass
        return z

    def threshold(self, non_max_img, lowThreshold, highThreshold, weak_pixel):
        """ 使用双阈值法生成强弱边缘图
        Parameters:
            non_max_img: 非极大抑制的图像
            lowThreshold: 低阈值
            highThreshold: 高阈值
            weak_pixel: 介于高低阈值之间的值
        returns:
            res: 处理后的图片
            weak: 弱阈值像素
            strong: 强阈值像素
        """
        print("highThreshold:", highThreshold, "\nlowThreshold:", lowThreshold)
        m, n = non_max_img.shape
        res = np.zeros((m, n))

        weak = weak_pixel
        strong = 255

        strong_i, strong_j = np.where(non_max_img >= highThreshold)
        zeros_i, zeros_j = np.where(non_max_img < highThreshold)
        weak_i, weak_j = np.where((non_max_img <= highThreshold) & (non_max_img >= lowThreshold))

        res[strong_i, strong_j] = strong
        res[weak_i, weak_j] = weak
        return res, weak, strong

    def hysteresis(self, threshold_img, weak, strong):
        """ 弱元素转化为强元素
        Parameters:
            threshold_img: 经过双阈值处理后的图像
            weak: 弱元素的值
            strong: 强元素的值
        returns:
            threshold_img: 处理后的图像
        """
        m, n = threshold_img.shape
        for i in range(1, m-1):
            for j in range(1, n-1):
                if threshold_img[i, j] == weak:
                    try:
                        if strong in [threshold_img[i+ii, j+jj] for ii in range(-1, 2) for jj in range(-1, 2)]:
                            threshold_img[i, j] = strong
                        else:
                            threshold_img[i, j] = 0
                    except IndexError as e:
                        pass
        return threshold_img

    def detect(self,img, sigma, kernel_size, lowthreshold, highthreshold, weak_pixel = 100):
        """ 通过canny算法来进行边缘检测
        Parameters:
            img: 原始图片范围必须是0-1之间的
            sigma: 方差
            kernel_size: 卷积核大小
            lowthreshold: 低阈值
            highthreshold: 高阈值
            weak_pixel: 介于高低阈值之间的值
        returns:
            res: 边缘图片
        """
        img = self.gaussian_filiter(img, sigma, kernel_size)
        granient, theta = self.sobel_filiter(img)
        z = self.non_max_suppression(granient, theta)
        res, weak, strong = self.threshold( z, lowthreshold, highthreshold, weak_pixel)
        res = self.hysteresis(res, weak, 255)
        return res


def show(img):
    import matplotlib.pyplot as plt
    plt.imshow(img, "gray")
    plt.show()

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import cv2
    import skimage

    img = cv2.imread("../data/picture_0_1.jpg", 0)  # 0 ~ 255的图像
    canny = Canny()
    edge = canny.detect(img,sigma=1, kernel_size=3, lowthreshold=10, highthreshold=100)
    show(edge)
