/*
 * @Description: 内存
 * @Version: 1.0
 * @Autor: lhgcs
 * @Date: 2019-08-08 10:29:24
 * @LastEditors: lhgcs
 * @LastEditTime: 2019-09-02 16:29:14
 */


#ifndef __MEMORYUTIL__
#define __MEMORYUTIL__


#include <stdio.h>
#include <string.h>
#include <malloc.h>


/**
 * @description: 分配内存
 * @param {type} 
 * @return: 
 */
char *create_memory(char **str, unsigned long int size);


/**
 * @description: 分配多个内存块（一般是为数组分配）
 * @param {type} 
 * @return: 
 */
char *create_memory_array(char **str, unsigned long int cnt, unsigned long int size);


/**
 * @description: 重新分配内存（扩大或缩小）
 * @param {type} 
 * @return: 
 */
char *resize_memory(char **str, unsigned long int size);


/**
 * @description: 释放内存
 * @param {type} 
 * @return: 
 */
char *release_memory(char *str);


/**
 * @description: 测试
 * @param {type} 
 * @return: 
 */
void test_memory();

#endif