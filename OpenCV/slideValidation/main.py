#################################
# Date: 2021/05/10
# Author: Miles Xu
# Email: kanonxmm@163.com
# Desc.: 滑块验证码识别接口，返回识别到的缺口坐标
#################################
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from utils import img2b64, b64Tndarray


class SVHelper:
    """
        滑块验证码，识别接口
        input:
            front: 滑块图片数据流 base64
            bg:    缺口图片数据流 base64
        output:
            (x, y): 缺口坐标
    """
    def __init__(self, front, bg):
        self.front = b64Tndarray(front)
        self.bg = b64Tndarray(bg)
        self.bg2 = self.bg
        self.coordinates = None

    def preprocess_front(self):
        """
            滑块预处理：
                1.灰度化滑块图片
                2.处理一下滑块图中滑块的外圈
                3.使用inRange二值化滑块图
                4.使用开运算去除白色噪点
        """
        # 灰度处理
        self.front = cv2.cvtColor(self.front, cv2.COLOR_BGR2GRAY)

        # 处理边缘黑色部分，只保留中间待匹配图形
        width, height = self.front.shape
        for h in range(height):
            for w in range(width):
                if self.front[w, h] == 0:
                    self.front[w, h] = 96

        # 使用inRange 二值化滑块图
        self.front = cv2.inRange(self.front, 96, 96)

        # 开运算去除白色噪点
        kernel = np.ones((8, 8), np.uint8)  # 去滑块的前景噪声内核
        self.front = cv2.morphologyEx(self.front, cv2.MORPH_OPEN, kernel)  # 开运算去除白色噪点

    def preprocess_bg(self):
        """
            处理带缺口背景图片：
                1.先来个高斯滤波去噪
                2.灰度化带缺口图
                3.使用阈值二值化该图
        """
        self.bg = cv2.GaussianBlur(self.bg, (3, 3), 0)  # 目标图高斯滤波
        self.bg = cv2.cvtColor(self.bg, cv2.COLOR_BGR2GRAY)
        ret, target = cv2.threshold(self.bg, 127, 255, cv2.THRESH_BINARY)  # 目标图二值化


    def process(self):
        """
            识别
        """
        self.preprocess_front()
        self.preprocess_bg()
        # 使用cv2 的图像匹配算法
        result = cv2.matchTemplate(
            self.bg, self.front, cv2.TM_CCOEFF_NORMED)#match匹配,Template模板;精度高，速度慢的方法
        index_max = np.argmax(result)#返回的是一维的位置，最大值索引

        x, y = np.unravel_index(index_max, result.shape)
        print("二维中坐标的位置：", x, y)
        print("使用selenium拖动时，xoffset={}".format(y))


        cv2.imshow("front", self.front)
        self.get_pos(self.bg2)
        cv2.imshow("bg", self.bg)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def get_pos(self, image):
        """[summary]

        Args:
            image ([type]): [description]

        Returns:
            [type]: [description]

        Desc.:
            轮廓检测识别缺口
                基于轮廓检测缺口的思路简单很多，加上合理的条件识别率在95%以上，实现过程如下：

                1.带缺口图高斯模糊去噪
                2.用(200,400)的阈值做Canny边缘检测
                3.寻找轮廓
                4.对已有的轮廓做约束，比如轮廓的面积范围，轮廓的周长范围
        """
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        canny = cv2.Canny(blurred, 200, 400)
        contours, hierarchy = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for i, contour in enumerate(contours):
            M = cv2.moments(contour)
            if M['m00'] == 0:
                cx = cy = 0
            else:
                cx, cy = M['m10'] / M['m00'], M['m01'] / M['m00']
            if 6000 < cv2.contourArea(contour) < 8000 and 370 < cv2.arcLength(contour, True) < 390:
                if cx < 400:
                    continue
                x, y, w, h = cv2.boundingRect(contour)  # 外接矩形
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.imshow('image', image)
                return x
        return 0



if __name__ == "__main__":
    front = img2b64("./resources/s1/front.png")
    bg = img2b64("./resources/s1/bg.png")
    SVHelper(front, bg).process()
