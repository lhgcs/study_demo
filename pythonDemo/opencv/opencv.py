#!/usr/bin/python3

'''
@Description: opencv demo
@Version: 1.0
@Autor: lhgcs
@Date: 2019-09-06 11:35:47
@LastEditors: lhgcs
@LastEditTime: 2019-09-06 11:36:06
'''

import cv2
import numpy as np


'''
@description: 保存图片
@param {type} 图片名称，图片数据，图片质量
@return: 
'''
def save_jpg(fileName, img):
    cv2.imwrite(fileName, img, [cv2.IMWRITE_JPEG_QUALITY, 50])


'''
@description: 获取灰度图像
@param {type} 
@return: 
'''
def get_gray(img):
    # 方法1：颜色空间转换
    dst= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 单通道，只有宽高
    print(dst.shape)

    h = img.shape[0]
    w = img.shape[1]
    dst = np.zeros((h, w), np.uint8)

    # 方法2：通过计算b,g,r的均值，在把均值赋给b,g,r
    # 速度太慢了
    for i in range(h):
        for j in range(w):
            (b,g,r) = img[i,j]
            # 使用int防止数据溢出
            # (b+g+r)/3
            dst[i,j] = np.uint8((int(b)+int(g)+int(r))/3)
    print(dst.shape)
    cv2.imshow("dst", dst)

    dst2 = np.zeros((h, w), np.uint8)
    # 方法3：r*0.299+g*0.587+b*0.114
    # 比上一个还慢
    for i in range(h):
        for j in range(w):
            (b,g,r) = img[i,j]
            # 使用int防止数据溢出
            dst2[i,j] = np.uint8(r*0.299 + g*0.587 + b*0.114)
    print(dst2.shape)
    cv2.imshow("dst2", dst2)


'''
@description: 几何图像
@param {type} 
@return: 
'''
def draw(img):
    # 线条
    # 起点 终点 线条颜色 线宽 线条类型
    cv2.line(img,(0,0),(200,200),(0,0,255), 10, cv2.LINE_AA)

    # 矩形
    # 左上角 右下角 线条颜色 是否填充（线条宽度)
    cv2.rectangle(img, (100,100), (200,200), (0,255,0), -1)

    # 椭圆
    # 圆心 轴长 偏转角度 起始角度 终止角度 是否填充（线条宽度) 线条类型（防锯齿）
    cv2.ellipse(img,(300,300),(100,50), 0, 0, 360, (255,255,255), -1, cv2.LINE_AA)
    
    # 圆形
    # 圆心 半径 线条颜色 是否填充（线条宽度) 线条类型（防锯齿）
    cv2.circle(img, (300,300), (50), (255,0,0), 2, cv2.LINE_AA)

    # 多边形
    # 坐标点(int32类型)
    point = np.array([[0,100],[200,200],[300,300],[300,400]],np.int32)
    # 维度转换
    point = point.reshape((-1,1,2))
    print(point.shape)
    cv2.polylines(img, [point], True, (0,255,255))

    # 字体
    font = cv2.FONT_HERSHEY_SIMPLEX
    # 文字 左下角坐标 字体 字体大小 颜色 线条大小 线条类型
    cv2.putText(img, "hello world", (100,100), font, 1, (255,0,0), 2, cv2.LINE_AA)
    
    cv2.imshow("img", img)


'''
@description: 改变图片大小
@param {type} 
@return: 
'''
def changeSize(img):
    # 方法1：resize
    h = img.shape[0]
    w = img.shape[1]
    dst = cv2.resize(img, (int(h/2), int(w/2)))
    cv2.imshow("dst", dst)

    # 方法2：最近邻域插值（通过缩放比例算出对应的坐标，再取在原图中最近的点）
    dst = np.zeros((int(h/2), int(w/2), img.shape[2]), np.uint8)
    dstH = int(h/2)
    dstW = int(w/2)
    scaleX = h*1.0/dstH
    scaleY = w*1.0/dstW

    for i in range(0, dstH):
        for j in range(0, dstW):
            dst[i,j] = img[int(i*scaleX), int(j*scaleY)]
    cv2.imshow("dst", dst)


'''
@description: 位移(部分图像显示不全)
@param {type} 
@return: 
'''
def move(img, moveX, moveY):
    # [x,y] * [[1,0,100],[0,1,200] = [x*1+y*0+100,x*0+y*1+200]
    matfloat = np.float32([[1,0,moveX], [0,1,moveY]])

    # 移位矩阵  图片info
    dst = cv2.warpAffine(img, matfloat, (img.shape[0], img.shape[1]))
    cv2.imshow("dst", dst)

    h = img.shape[0]
    w = img.shape[1]
    dst = np.zeros((h+moveY, w+moveX, 3), np.uint8)
    for i in range(h):
        for j in range(w):
            dst[i+moveY, j+moveX] = img[i,j]
    cv2.imshow("dst", dst)


'''
@description: 镜像
@param {type} 
@return: 
'''
def mirror_x(img):
    h = img.shape[0]
    w = img.shape[1]
    deep = img.shape[2]

    dst = np.zeros((h*2,w,deep), np.uint8)
    for i in range(0, h):
        for j in range(0, w):
            dst[i,j] = img[i,j]
            dst[h*2-i-1,j] = img[i,j]
    cv2.imshow("dst", dst)


'''
@description: 镜像
@param {type} 
@return: 
'''
def mirror_y(img):
    h = img.shape[0]
    w = img.shape[1]
    deep = img.shape[2]
    dst = np.zeros((h, w*2, deep), np.uint8)
    for i in range(0, h):
        for j in range(0, w):
            dst[i,j] = img[i,j]
            dst[i,w*2-j-1] = img[i,j]
    cv2.imshow("dst", dst)


'''
@description: 仿射变换
@param {type} 
@return: 
'''
def mapping(img):
    h = img.shape[0]
    w = img.shape[1]
    # 三个点映射到新位置，左上，左下，右上
    matsrc = np.float32([[0,0],[0,h-1],[w-1,0]])
    matdst = np.float32([[50,50],[0,h-1],[w-1,0]])
    # 组合
    # 仿色变换矩阵
    matAffine = cv2.getAffineTransform(matsrc,matdst)
    dst = cv2.warpAffine(img,matAffine,(w,h))
    cv2.imshow("dst", dst)


'''
@description: 旋转矩阵
@param {type} 
@return: 
'''
def rotate(img, value):
    h = img.shape[0]
    w = img.shape[1]
    # 中心点， 角度，缩放系数
    matrotate = cv2.getRotationMatrix2D((h/2,w/2), value, 0.5)
    # 仿射方法
    dst = cv2.warpAffine(img,matrotate,(w,h))
    cv2.imshow("dst", dst)


'''
@description: 图像叠加
@param {type} 
@return: 
'''
def add(img1, value1, img2, value2):
    # 图像1 图像1权重 图像2 图像2权重 透明度（1-a)
    dst = cv2.addWeighted(img1, value1, img2, value2, 0)
    cv2.imshow("dst", dst)


'''
@description: 边缘检测
@param {type} 
@return: 
'''
def canny(img):
    # 转为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 高斯滤波（去掉噪声）
    cv2.GaussianBlur(gray,(3,3),0)
    # canny边缘检测，大于这个值，视为边缘点
    dst = cv2.Canny(img,50,50)
    cv2.imshow("dst", dst)

import math
'''
@description: 边缘检测(速度超慢)
@param {type} 
@return: 
'''
def outline(img):
    # 转为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h = gray.shape[0]
    w = gray.shape[1]
    dst = np.zeros((h,w,1), np.uint8)

    for i in range(1, h-3):
        for j in range(1, w-3):
            # 图片卷积(对应元素相乘)
            x = gray[i,j] + (gray[i,j+1]<<1) + gray[i,j+2] - gray[i+2,j] - (gray[i+2,j+1]<<1) - gray[i+2,j+2]
            y = gray[i,j] - gray[i,j+2] + (gray[i+1,j]<<1) - (gray[i+1,j+2]<<1) + gray[i+2,j] - gray[i+2,j+2]
            
            # 阈值判决(大于阈值则为边缘)
            grad = math.sqrt(x*x+y*y)
            dst[i,j] = 255 if grad > 50 else grad
    cv2.imshow("dst", dst)


'''
@description: 浮雕(相邻像素值之差+固定值)
@param {type} 
@return: 
'''
def relief(img):
    # 转为灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    h = gray.shape[0]
    w = gray.shape[1]
    dst = np.zeros((h,w,1), np.uint8)

    for i in range(0,h-1):
        for j in range(0,w):
            pix = int(gray[i+1,j]) - gray[i,j] + 150
            dst[i,j] = 255 if pix > 255 else pix
    cv2.imshow("dst", dst)


'''
@description: 滤波(模板越大越模糊)
@param {type} 
@return: 
'''
def filter(img):
    # 双边滤波
    dst = cv2.bilateralFilter(img, 15, 35, 35)
    cv2.imshow("dst1", dst)

    # 高斯滤波
    dst = cv2.GaussianBlur(img, (3,3), 1.5)
    cv2.imshow("dst2", dst)

    h = img.shape[0]
    w = img.shape[1]

    # 均值滤波(3x3)
    dst = np.zeros((h,w,3), np.uint8)
    for i in range(1, h-1):
        for j in range(1, w-1):
            sumb = int(0)
            sumg = int(0)
            sumr = int(0)
            for m in range(-1,2):
                for n in range(-1,2):
                    b,g,r = img[i+m,j+n]
                    sumb += int(b)
                    sumg += int(g)
                    sumr += int(r)
            b = np.uint8(sumb/9)
            g = np.uint8(sumg/9)
            r = np.uint8(sumr/9)
            dst[i,j] = (b,g,r)
    cv2.imshow("dst3", dst)

    # 中值滤波
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    for i in range(1, h-1):
        for j in range(1, w-1):
            # 取出9个元素
            temp = []
            for m in range(-1,2):
                for n in range(-1,2):
                    temp.append(img[i+m,j+n])
            # 排序
            temp.sort()
            dst[i,j] = temp[4]
    cv2.imshow("dst4", dst)


'''
@description: 计算直方图
@param {type} 
@return: 
'''
def imageHist(img):
    # 计算直方图
    # 图片数组 直方图通道 蒙版 直方图分成多少分 像素从0-255
    hist = cv2.calcHist([img], [0], None, [256], [0.0,255])
    print(type(hist))
    # numpy 元素是下标对应灰度级的个数
    # 最小值，最大值 及对应下标
    minv, maxv, minL, maxL = cv2.minMaxLoc(hist)
    print(minv,maxv,minL,maxL)
    # 画布
    histImg = np.zeros([256,256,3], np.uint8)
    for h in range(256):
        # 归一化到 0-256
        inteNormal = int(hist[h] * 256 / maxv)
        cv2.line(histImg, (h, 256), (h, 256-inteNormal), (255,0,0))
    cv2.imshow("B", histImg)
    return histImg


'''
@description: 灰度图直方图均衡化
@param {type} 
@return: 
'''
def equal(img):
    # 转灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 均衡化
    dst = cv2.equalizeHist(gray)
    cv2.imshow("dst", dst)
    cv2.waitKey(3000)


'''
@description: 彩色图直方图均衡化
@param {type} 
@return: 
'''
def equal3(img):
    # bgr转yuv
    # imgYuv = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    # imgYuv = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)
    
    # 分解单通道
    b, g, r = cv2.split(img)
    # 均衡化
    bb = cv2.equalizeHist(b)
    gg = cv2.equalizeHist(g)
    rr = cv2.equalizeHist(r)
    # 合成
    dst = cv2.merge((bb, gg, rr))
    cv2.imshow("dst", dst)
    cv2.waitKey(3000)


'''
@description: 灰度图直方图均衡化
@param {type} 
@return: 
'''
def equal_img(img):
    h = img.shape[0]
    w = img.shape[1]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray", gray)

    count = np.zeros(256, np.float)
    for i in range(0, h):
        for j in range(0,w):
            pix = gray[i,j]
            index = int(pix)
            count[index] = count[index] + 1
    # 每个像素等级的概率
    for i in range(0, 256):
        count[i] = count[i]*1.0 / (w*h)

    # 累积概率
    sum1 = float(0)
    for i in range(0,256):
        sum1 = sum1 + count[i]
        count[i] = sum1
        print(count[i])

    # 计算映射表
    map1 = np.zeros(256, np.uint16)
    for i in range(0, 256):
        map1[i]= np.uint16(count[i] * 255)

    for i in range(0, h):
        for j in range(0,w):
            index = int(gray[i,j])
            gray[i,j] = map1[pix]

    cv2.imshow("eequal", gray)


'''
@description: 滤波
@param {type} 
@return: 
'''
def blgr(img):

    # 锐化
    # 自定义核
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], np.float32)
    # 对图像和自定义核做卷积
    img = cv2.filter2D(img, -1, kernel=kernel)


    # 均值滤波
    img_mean = cv2.blur(img, (3,3))

    # 高斯滤波
    img_Guassian = cv2.GaussianBlur(img, (3,3), 0)

    # 中值滤波
    img_median = cv2.medianBlur(img, 3)

    # 双边滤波
    img_bilater = cv2.bilateralFilter(img, 9, 75, 75)

    # 二值化
    ret,b = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)


if __name__ == "__main__":
    # 读取图片
    img = cv2.imread("/home/ubuntu/Desktop/1.jpg", 1) # 0 灰度图，1 原图

    # # 获取灰度图像
    # get_gray(img)

    # # 几何图像
    # draw(img)

    # # 改变图像大小
    # changeSize(img)

    # # 移动
    # move(img, 100, 200)

    # # 镜像
    # mirror_x(img)
    # mirror_y(img)

    # # 映射
    # mapping(img)

    # # 旋转
    # rotate(img,180)

    # # 叠加
    # add(img,0.1,img,0.2)

    # 边缘检测
    # canny(img)
    # outline(img)

    # # 浮雕
    # relief(img)

    # # 滤波
    # filter(img)

    # 直方图
    # imageHist(img)
    # equal(img)
    # equal3(img)
    equal_img(img)


    cv2.waitKey(30000)