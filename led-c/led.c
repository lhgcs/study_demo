/*
 * @Description: led控制
 * @Author: your name
 * @Date: 2019-07-17 10:49:33
 * @LastEditTime: 2019-09-06 11:34:32
 * @LastEditors: lhgcs
 */

#include "led.h"
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

/**
 * @description: 写入led
 * @param {type} 
 * @return: 
 */
int led_ctrl(char *device, char *level) {
    int res = -1;
    int fd = -1;

    if(NULL == device || NULL == level) {
        return res;
    }

    fd = open(device, O_WRONLY);
    if(fd > 0) {
        printf("open %s\n", device);
        res = write(fd, level, strlen(level));
        close(fd);
    } else {
        printf("can not open %s\n", device);
    }
    
    return res;
}

/**
 * @description: 控制led亮灭
 * @param {type} 
 * @return: 
 */
int led_on_or_off(int led, int level) {
    printf("%d\n", led);
    int res = -1;
    char str[2] = {0};
    char device[48] = "/sys/class/leds/led-";
    switch(led) {
        //case LED_POWER: break;
        case LED_WIFI: strcat(device, "wifi"); break;
        case LED_USE1: strcat(device, "usr1"); break;
        case LED_USE2: strcat(device, "usr2"); break;
        default: return res;
    }
    printf("%s\n", device);
    sprintf(str, "%d", level);
    res = led_ctrl(device, str);
    return res;
}
