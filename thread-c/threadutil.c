/*
 * @Description: 线程
 * @Version: 1.0
 * @Autor: lhgcs
 * @Date: 2019-08-08 10:32:06
 * @LastEditors: lhgcs
 * @LastEditTime: 2019-09-02 16:30:08
 */


#include <stdio.h>
#include <pthread.h>
#include <semaphore.h>
#include <unistd.h>
#include "threadutil.h"


/**
 * @description: 创建线程
 * @param {type} 
 * @return: 
 */
unsigned long int create_thread(FUN fun, char *args) {
    pthread_t thid;
    // 线程ID,线程属性,线程函数,传递给线程函数的参数
    pthread_create(&thid,NULL,(void*)fun, (void *)args);
    return thid;
}


/**
 * @description: 等待线程结束函数
 * @param {type} 
 * @return: 
 */
void get_result(unsigned long int id, void **res) {
    // 要等待结束的线程的ID,结束线程的返回值的地址
    pthread_join(id, res);
}


/**
 * @description: 将线程设置为分离属性(分离属性的线程一旦结束，直接回收资源)
 * @param {type} 
 * @return: 
 */
void set_detach(unsigned long int id) {
    // 当线程设置为分离属性后将无法再等待线程结束和获取线程的返回值，pthread_join无效
    pthread_detach(id);
}


//由于多线程之间是共享进程资源的，所以多线程编程时需要对共享资源的访问进行保护
unsigned long int num = 0;


//互斥锁
pthread_mutex_t lock;


/**
 * @description: 初始化互斥锁
 * @param {type} 
 * @return: 
 */
void init_lock() {
    pthread_mutex_init(&lock,0);
}


/**
 * @description: 删除互斥锁
 * @param {type} 
 * @return: 
 */
void destroy_lock() {
    pthread_mutex_destroy(&lock);
}


/**
 * @description: 线程方法(互斥锁)
 * @param {type} 
 * @return: 
 */
void* task_lock(void* arg){
    char *str = (char *)arg;
    for(unsigned int i=1; i>0; i++) {
        printf("%ld  %s\n", num, str);
        usleep(1000000);//1秒

        pthread_mutex_lock(&lock);  // 加锁
        num++;                      // 访问共享资源
        pthread_mutex_unlock(&lock);// 解锁
    }
    printf("thread exit\n");
    pthread_exit(0);
}


// 信号量
sem_t sem;

/**
 * @description: 初始化信号量
 * @param {type} 
 * @return: 
 */
void init_sem() {
    // 信号量初始值10
    sem_init(&sem,0,10);
}


/**
 * @description: 释放信号量
 * @param {type} 
 * @return: 
 */
void destroy_sem() {
    // 如果还有线程在等待它，返回EBUSY
    sem_destroy(&sem);
}


/**
 * @description: 线程方法（信号量）
 * @param {type} 
 * @return: 
 */
void* task_sem(void* arg){
    char *str = (char *)arg;
    for(unsigned int i=1; i>0; i++) {
        printf("%ld  %s\n", num, str);
        usleep(1000000);//1秒

        sem_wait(&sem);// P操作(计数-1)(阻塞当前线程直到信号量大于0，然后 才-1)
        //sem_trywait是一个立即返回函数
        num++;         // 访问共享资源
        sem_post(&sem);// V操作(计数+1)
    }
    printf("thread exit\n");
    pthread_exit(0);    
}


/**
 * @description: 测试
 * @param {type} 
 * @return: 
 */
void test_thread() {
    init_lock();
    init_sem();

    while (1)
    {
        create_thread(task_lock, "zhangsan");
        create_thread(task_sem, "lisi");
    }
    

    destroy_lock();
    destroy_sem();
}
