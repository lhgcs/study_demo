#!/bin/bash

### 
# @Description: v4l2-ctl获取摄像头图片
 # @Version: 1.0
 # @Autor: lhgcs
 # @Date: 2019-07-19 11:05:25
 # @LastEditors: lhgcs
 # @LastEditTime: 2019-10-15 11:24:53
 ###


# 图片保存路径
JPG_SAVE_PATH="/home/ubuntu/Desktop/tmp"
mkdir -p ${JPG_SAVE_PATH}

# 图片保存路径
CAMERA="/dev/video0"


###
 # @description: 设置曝光值(范围0-5000)
 # @param {type} 
 # @return: 
###
set_exposure() {
    v4l2-ctl -d ${CAMERA} -c exposure_absolute=$1
    sleep 1
    v4l2-ctl -d ${CAMERA} -C exposure_absolute
}

###
 # @description: 设置白平衡值
 # @param {type} 
 # @return: 
###
set_white_balance() {
    v4l2-ctl -d ${CAMERA} -c white_balance_temperature=$1
    sleep 1
}

###
 # @description: 输出一帧图像
 # @param {type} 
 # @return: 
###
save_image() {
    DATE=$(date "+%Y-%m-%d_%H:%M:%S")
    v4l2-ctl -d ${CAMERA} --set-fmt-video=width=1920,height=1080 #,pixelformat=3
    v4l2-ctl -d ${CAMERA} --stream-mmap=3 --stream-count=1 --stream-to=${JPG_SAVE_PATH}/${DATE}.jpg
} 

###
 # @description: 输出视频
 # @param {type} 
 # @return: 
###
save_video() {
    DATE=$(date "+%Y-%m-%d_%H:%M:%S")
    v4l2-ctl --set-fmt-video=width=1920,height=1088,pixelformat=NV12
    v4l2-ctl --stream-mmap=3 --stream-count=1000 --stream-to=${JPG_SAVE_PATH}/${DATE}.264
}


###
 # @description: 初始化
 # @param {type} 
 # @return: 
###
init() {
    # 关闭自动曝光
    v4l2-ctl -c exposure_auto=1
    # 当前自动曝光是否开启
    v4l2-ctl -d ${CAMERA} -C exposure_auto

    # 关闭自动白平衡
    # v4l2-ctl -d ${CAMERA} -c white_balance_temperature_auto=0
    # 开启自动白平衡
    # v4l2-ctl -d ${CAMERA} -c white_balance_temperature_auto=0
    # 当前白平衡是否开启
    v4l2-ctl -d ${CAMERA} -C white_balance_temperature_auto
    # 当前白平衡的值
    v4l2-ctl -d ${CAMERA} -C white_balance_temperature
}


# 初始化
init

i=0
while [ $i -le 3 ]
do
    sum=$[100 + i*500]
    let i++

    # 设置曝光值
    set_exposure ${sum}
    # 保存图像
    save_image
  
done

exit 0