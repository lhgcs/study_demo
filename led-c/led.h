#ifndef LED_H
#define LED_H

#define LED_POWER 1  //电源指示灯
#define LED_WIFI  2  //wifi指示灯
#define LED_USE1  3  //指示灯
#define LED_USE2  4  //指示灯

#define LED_ON    1  //指示灯亮
#define LED_OFF   0  //指示灯灭

/**
 * @description: 控制led亮灭
 * @param {type} 
 * @return: 
 */
int led_on_or_off(int led, int level) ;

#endif