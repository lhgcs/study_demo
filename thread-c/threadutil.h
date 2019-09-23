/*
 * @Description: 线程
 * @Version: 1.0
 * @Autor: lhgcs
 * @Date: 2019-08-08 10:32:06
 * @LastEditors: lhgcs
 * @LastEditTime: 2019-09-02 16:30:39
 */


#ifndef __THREADUTIL__
#define __THREADUTIL__


#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>


typedef void *(*FUN)(void *);


/**
 * @description: 创建线程
 * @param {type} 
 * @return: 
 */
unsigned long int create_thread(FUN fun, char *args);


/**
 * @description: 等待线程结束函数
 * @param {type} 
 * @return: 
 */
void get_result(unsigned long int id, void **res);


/**
 * @description: 将线程设置为分离属性(分离属性的线程一旦结束，直接回收资源)
 * @param {type} 
 * @return: 
 */
void set_detach(unsigned long int id);


/**
 * @description: 初始化互斥锁
 * @param {type} 
 * @return: 
 */
void init_lock();


/**
 * @description: 删除互斥锁
 * @param {type} 
 * @return: 
 */
void destroy_lock();


/**
 * @description: 线程方法(互斥锁)
 * @param {type} 
 * @return: 
 */
void* task_lock(void* arg);


/**
 * @description: 初始化信号量
 * @param {type} 
 * @return: 
 */
void init_sem();


/**
 * @description: 释放信号量
 * @param {type} 
 * @return: 
 */
void destroy_sem();


/**
 * @description: 线程方法（信号量）
 * @param {type} 
 * @return: 
 */
void* task_sem(void* arg);


/**
 * @description: 测试
 * @param {type} 
 * @return: 
 */
void test_thread();

#endif