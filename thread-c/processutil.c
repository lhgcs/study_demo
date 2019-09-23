/*
 * @Description: 进程
 * @Version: 1.0
 * @Autor: lhgcs
 * @Date: 2019-08-08 16:36:45
 * @LastEditors: lhgcs
 * @LastEditTime: 2019-09-02 16:29:29
 */


#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include "processutil.h"


/**
 * @description: 创建进程
 * @param {type} 
 * @return: 
 */
int create_process() {

    pid_t pid;

    if((pid=fork()) < 0) {
        printf("fork error!\n");
        exit(1);
    } else if(pid==0) {
        while(1) {
            printf("Child process PID: %d  Parent process PID: %d\n", getpid(), getppid());
            create_process();
        }
    } else {
        while(1) {
            printf("Parent process PID: %d.\n", getpid());
            create_process();
        }
    }

    printf("stop\n");
    return 0;
}


/**
 * @description: 
 * @param {type} 
 * @return: 
 */
void exec_comman() {
    // 当进程调用 exec 族函数时，该进程的用户空间代码和数据完全被新程序替换，从新程序的起始处开始执行。调用 exec 族函数并不创建新进程，所以调用 exec 族函数前后该进程的 PID 并不改变。
    char *argv[ ]={"ls", "-al", "/home", NULL};  
    char *envp[ ]={"PATH=/bin", NULL};
    if(execve("/bin/ls", argv, envp) < 0)
    {
        printf("subprocess error");
        exit(1);
    }
    // 子进程要么从 ls 命令中退出，要么从上面的 exit(1) 语句退出
    // 所以代码的执行路径永远也走不到这里，下面的 printf 语句不会被执行
    printf("You should never see this message.");
}
