#!/usr/bin/env python

'''
@Description: pyA20控制GPIO
@Version: 1.0
@Autor: lhgcs
@Date: 2019-09-06 11:36:50
@LastEditors: lhgcs
@LastEditTime: 2019-09-16 18:11:05
'''

'''
安装：pip install pyA20
'''

import os
import sys
import time
from pyA20.gpio import gpio
from pyA20.gpio import port
#print dir(port)


# 初始化
gpio.init()


'''
@description: 输出电平
@param {type} 
@return: 
'''
def gpio_input(pin, level):
    gpio.setcfg(pin, gpio.OUTPUT)
    gpio.output(pin, level)


'''
@description: 读电平
@param {type} 
@return: 
'''
def gpio_input(pin):
    gpio.setcfg(pin, gpio.INPUT)
    return gpio.input(pin)


'''
@description: 控制风扇降温
@param {type} 
@return: 
'''
def fan_control():
    #  GPIO初始化输出
    args = sys.argv
    # 引脚
    Pin = int(args[1])  # Pin = 2
    # 电平
    Act = int(args[2])

    # 设置
    gpio.setcfg(Pin, gpio.OUTPUT)
    # 输出电平
    gpio.output(Pin, 1 if Act == 1 else 0)

    while True:
        # output = os.popen('cat /sys/devices/virtual/hwmon/hwmon1/temp1_input')
        output = os.popen('cat /sys/devices/virtual/thermal/thermal_zone0/temp')
        wd = output.read()
        temp = int(wd)
        print("cpu温度: ", temp)

        if temp > 50000:
            gpio.output(Pin, 1)
        else:
            gpio.output(Pin, 0)
        time.sleep(1)

if __name__ == "__main__":
    fan_control()
