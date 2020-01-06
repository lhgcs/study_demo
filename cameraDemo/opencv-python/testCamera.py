#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
@Description: opencv 打开摄像头
@Version: 1.0
@Autor: lhgcs
@Date: 2019-08-02 16:27:52
@LastEditors: lhgcs
@LastEditTime: 2019-09-06 11:13:27
'''


import cv2
import numpy as np
import time


'''
@description: 调节色度
@param {type} 
@return: 
'''
def adjust_hue(imgSrc):
    # 复制
    imgRGB = imgSrc.copy()

    # 求原始图像的RGB分量的均值
    B = cv2.mean(cv2.split(imgSrc)[0])[0]
    G = cv2.mean(cv2.split(imgSrc)[1])[0]
    R = cv2.mean(cv2.split(imgSrc)[2])[0]
 
    # 需要调整的RGB分量的增益
    total = R + G + B
    R = 1 if R ==0 else R
    G = 1 if G ==0 else G
    B = 1 if B ==0 else B

    # 计算三个通道的增益系数
    KB = total / (3 * B)
    KG = total / (3 * G)
    KR = total / (3 * R)
 
    # 调整RGB三个通道各自的值
    imgRGB[0] = imgRGB[0] * KB
    imgRGB[1] = imgRGB[1] * KG
    imgRGB[2] = imgRGB[2] * KR
 
	# RGB三通道图像合并
    # img = cv2.merge(imgRGB, img)
    cv2.imshow("白平衡调整后", imgRGB)
    cv2.waitKey(3)


'''
@description: 获取摄像头参数
@param {type} 
@return: 
'''
def get_camera_info(capture):
    print("################ camera info ########################")
    print("视频编码器格式:", capture.get(cv2.CAP_PROP_FOURCC))
    print("宽:",      capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    print("高:",      capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print("帧率:",     capture.get(cv2.CAP_PROP_FPS))
    print("亮度:",     capture.get(cv2.CAP_PROP_BRIGHTNESS))
    print("对比度:",   capture.get(cv2.CAP_PROP_CONTRAST))
    print("饱和度:",   capture.get(cv2.CAP_PROP_SATURATION))
    print("色度:",     capture.get(cv2.CAP_PROP_HUE))
    print("曝光:",     capture.get(cv2.CAP_PROP_EXPOSURE))
    print("增益:",     capture.get(cv2.CAP_PROP_GAIN))
    print("白平衡:",   capture.get(cv2.CAP_PROP_WHITE_BALANCE))
    print("自动曝光:", capture.get(cv2.CAP_PROP_AUTO_EXPOSURE))
    print("WB:",      capture.get(cv2.CAP_PROP_AUTO_WB))


def show_info(capture):
    print("################### info #####################")
    print("亮度:", capture.get(cv2.CAP_PROP_BRIGHTNESS))
    print("帧率:", capture.get(cv2.CAP_PROP_FPS))
    print("色度:", capture.get(cv2.CAP_PROP_HUE))
    print("曝光:", capture.get(cv2.CAP_PROP_EXPOSURE))
    print("自动曝光:", capture.get(cv2.CAP_PROP_AUTO_EXPOSURE))


'''
@description: BGR三个通道的平均值
@param {type} 
@return: 
'''
def get_bgr_avg(frame):
    num = frame.size / frame.ndim
    avgB = np.sum(frame[:, :, 0]) / num
    avgG = np.sum(frame[:, :, 1]) / num
    avgR = np.sum(frame[:, :, 2]) / num
    return (avgB, avgG, avgR)


'''
@description: 开启或关闭自动白平衡
@param {type} 
@return: 
'''
def auto_wb(capture, isAuto):
    ret = capture.get(cv2.CAP_PROP_AUTO_WB)

    if isAuto:
        # 当前关闭了自动白平衡，则开启
        if ret == 0:
            capture.set(cv2.CAP_PROP_AUTO_WB, 1)
    else:
        # 当前开启了自动白平衡，则关闭，设置白平衡值为当前值
        if ret == 1:
            capture.set(cv2.CAP_PROP_AUTO_WB, 0)
            capture.set(cv2.CAP_PROP_WB_TEMPERATURE, capture.get(cv2.CAP_PROP_WB_TEMPERATURE))


'''
@description: 调整曝光
@param {type} 
@return: 
'''
def auto_exposure(capture, value, isAuto):
    if 0 == isAuto:
        return

    minValue = 115  # 下限
    maxValue = 140  # 上限

    ret = capture.get(cv2.CAP_PROP_AUTO_EXPOSURE)
    # ARM
    if ret == 0.25:
        exposure = capture.get(cv2.CAP_PROP_EXPOSURE)
        if value < minValue:
            exposure += 0.001
            exposure = 1 if exposure > 1 else exposure
            capture.set(cv2.CAP_PROP_EXPOSURE, exposure)
        elif value > maxValue:
            exposure -= 0.001
            exposure = 0 if exposure < 0 else exposure
            capture.set(cv2.CAP_PROP_EXPOSURE, exposure)
    # PC
    elif ret == 1:
        exposure = capture.get(cv2.CAP_PROP_EXPOSURE)
        if value < minValue or value > maxValue:
            exposure += (128 - value) / 40
            if exposure < 0:
                exposure = 0
            elif exposure > 255:
                exposure = 255
            capture.set(cv2.CAP_PROP_EXPOSURE, exposure)


'''
@description: 是否有人
@param {type} 
@return: 
'''
def is_anyone(capture):
    ret = capture.get(cv2.CAP_PROP_GAIN)
    print(ret)


'''
@description: 校正
@param {type} 
@return: 
'''
def adjust(capture, frame):
    avgB, avgG, avgR = get_bgr_avg(frame)
    # 灰度平均值
    value = (avgB + avgG + avgR) / 3
    auto_exposure(capture, value, 1)
    #print(int(avgB), int(avgG), int(avgR), int(avgB + avgG + avgR))


'''
@description: 打开摄像头
@param {type} 
@return: 
'''
def open_camera():

    i = 0
    t1 = time.time()
    
    while True:
        capture = cv2.VideoCapture(8)
        if(capture != None):
            break
        if(i > 10):
            return

    get_camera_info(capture)

    # 设置摄像头参数
    # 只有2种模式：1（手动）和 3（自动）s
    # capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1); # 开启手动曝光
    # capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3); # 开启自动曝光
    # 另一个摄像头
    # capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25); # 开启手动曝光
    capture.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.75); # 开启自动曝光
    
    capture.set(cv2.CAP_PROP_AUTO_WB, 1)         # 关闭自动白平衡
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1600); # 宽度 
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200);# 高度
    capture.set(cv2.CAP_PROP_FPS, 10);           # 帧率
    capture.set(cv2.CAP_PROP_CONTRAST,50);       # 对比度 50
    capture.set(cv2.CAP_PROP_SATURATION, 50);    # 饱和度 50
    capture.set(cv2.CAP_PROP_HUE, 0);            # 色调 50
    capture.set(cv2.CAP_PROP_EXPOSURE, 50);      # 曝光 50
    capture.set(cv2.CAP_PROP_BRIGHTNESS, 1);     # 亮度 1
    capture.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter.fourcc('M','J','P','G')) # 编码格式
    get_camera_info(capture)

    # 读摄像头
    cv2.namedWindow("video")
    while (capture.isOpened()):
        ret,frame = capture.read()
        if ret == True:
            cv2.imshow("video",frame)
            adjust(capture, frame)
            
            show_info(capture)
            is_anyone(capture)

        if (cv2.waitKey(100) == 27): # Esc键退出
            break

        if time.time() - t1 > 10:
            t1 = time.time()
            
    # 释放摄像头
    capture.release()
    # 删除全部窗口
    cv2.destroyAllWindows()
    

open_camera()
