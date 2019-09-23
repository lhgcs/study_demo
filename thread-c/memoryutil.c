/*
 * @Description: 内存
 * @Version: 1.0
 * @Autor: lhgcs
 * @Date: 2019-08-08 10:29:24
 * @LastEditors: lhgcs
 * @LastEditTime: 2019-09-02 16:28:45
 */


#include <stdio.h>
#include <string.h>
#include <malloc.h>
#include "memoryutil.h"


/**
 * @description: 分配内存
 * @param {type} 
 * @return: 
 */
char *create_memory(char **str, unsigned long int size) {
    char *p = *str;
    // 分配内存
    p = (char *)malloc(size * sizeof(char));
    if (NULL != p) {
        // 初始化
        memset(p, 0, sizeof(p));
    }
    return p;
}


/**
 * @description: 分配多个内存块（一般是为数组分配）
 * @param {type} 
 * @return: 
 */
char *create_memory_array(char **str, unsigned long int cnt, unsigned long int size) {
    char *p = *str;
    // 已经初始化
    p = (char *)calloc(cnt, size);
    if (NULL != p) {  

    }
    return p;
}


/**
 * @description: 重新分配内存（扩大或缩小）
 * @param {type} 
 * @return: 
 */
char *resize_memory(char **str, unsigned long int size) {
    char *p = *str;
    // 内存的内容不变（缩小内存时可能丢失数据），可能不是原来那一块内存
    p = (char *) realloc(p, size);
    return p;
}


/**
 * @description: 释放内存
 * @param {type} 
 * @return: 
 */
char *release_memory(char *str) {
    if (NULL != str) {
        free(str);
        str = NULL;
    }
}


/**
 * @description: 测试
 * @param {type} 
 * @return: 
 */
void test_memory() {
	char *p = NULL;
	int i=0;
	while(1) {
        create_memory(&p, 1);
        create_memory_array(&p, 1024, 1024*1024);
        printf("%d\n", ++i);
    }
}
