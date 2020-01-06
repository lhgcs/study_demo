/*
 * @Description: usb摄像头
 * @Author: your name
 * @Date: 2019-07-20 10:53:25
 * @LastEditTime: 2019-07-24 09:32:53
 * @LastEditors: Please set LastEditors
 */

#include "play_video.h"

#include <stdio.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <errno.h>
#include <getopt.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/select.h>
#include <sys/time.h>		// for timestamp incomplete error in kernel 2.6.21
#include <linux/version.h>
#include <sys/utsname.h>
#include <pthread.h>

#include <linux/videodev2.h>
#include <time.h>

// https:// my.oschina.net/yuyang/blog/176049


/**
 * @description: 获取时间字符串
 * @param {type} 
 * @return: 
 */
void get_current_time(char *str) {
    time_t t;   
    struct tm *p;
    char temp[48];
    memset(temp, 0, sizeof(temp));

    time(&t);   
    p = localtime(&t);
    sprintf(temp, "%d%d%d_%d%d%d_%ld\n", (1900 + p->tm_year), (1 + p->tm_mon), p->tm_mday,(p->tm_hour + 12), p->tm_min, p->tm_sec, t); 
    strcat(str, temp);
   // printf("%s\n", asctime(p));
}


/**
 * @description: 录制视频
 * @param {type} 
 * @return: 
 */
void play_video() {

    // 打开摄像头
    int cam_fd = open("/dev/video0", O_RDWR);
    if (cam_fd < 0) {
        return;
    }


    // 查询设备属性
    struct v4l2_capability cap;
    ioctl(cam_fd, VIDIOC_QUERYCAP, &cap);
    printf("Driver Name:%s\nCard Name:%s\nBus info:%s\nDriver Version:%u.%u.%u\n",
    cap.driver,
    cap.card,
    cap.bus_info,
    (cap.version>>16)&0XFF,
    (cap.version>>8)&0XFF,
    cap.version&0XFF);


    struct v4l2_format *fmt = calloc(1, sizeof(*fmt));
    fmt->type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    
    // 获取摄像头当前的采集格式
    ioctl(cam_fd, VIDIOC_G_FMT,fmt);
    printf("%d\n", fmt->fmt.pix.width);
    printf("%d\n", fmt->fmt.pix.height);

    // 设置摄像头的采集格式JPEG
    bzero(fmt, sizeof(*fmt));
    fmt->type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    fmt->fmt.pix.width = 1024;
    fmt->fmt.pix.height = 768;
    fmt->fmt.pix.pixelformat = V4L2_PIX_FMT_JPEG;// 格式
    fmt->fmt.pix.field = V4L2_FIELD_INTERLACED; // 采样区域,交错方式捕获
    ioctl(cam_fd, VIDIOC_S_FMT, fmt);
    // // 尝试设置
    // ioctl(cam_fd, VIDIOC_TRY_FMT, fmt);

    //释放
    free(fmt);
    

    // 设置摄像头缓存的个数
    int nbuf = 3;

    // 向内核申请缓存（内核）
    struct v4l2_requestbuffers reqbuf;
    bzero(&reqbuf, sizeof(reqbuf));
    reqbuf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    reqbuf.memory = V4L2_MEMORY_MMAP;
    reqbuf.count = nbuf;
    ioctl(cam_fd, VIDIOC_REQBUFS, &reqbuf);

    // 定义struct v4l2_buffer，每个v4l2_buffer对应内核驱动中的一个缓存
    struct v4l2_buffer buffer[nbuf];
    int length[nbuf];
    unsigned char * start[nbuf];

    for(int i=0; i<nbuf; i++) {
        bzero(&buffer[i], sizeof(buffer[i]));
        buffer[i].type = V4L2_BUF_TYPE_VIDEO_CAPTURE; // 缓冲帧数据格式
        buffer[i].memory = V4L2_MEMORY_MMAP;          // 内存映射方式
        buffer[i].index = i;
        // 取内核的buffer的数据，获取缓冲帧的地址，长度
        ioctl(cam_fd, VIDIOC_QUERYBUF, &buffer[i]);

        length[i] = buffer[i].length;
        // 内核缓冲区通过mmap映射到用户空间的内存，我们在用户层获取摄像头数据
        start[i] = mmap(NULL, buffer[i].length, PROT_READ | PROT_WRITE, MAP_SHARED, cam_fd, buffer[i].m.offset);
        // 入队，准备放入数据
        ioctl(cam_fd, VIDIOC_QBUF, &buffer[i]);
    }


	// 采集数据
	enum v4l2_buf_type vtype = V4L2_BUF_TYPE_VIDEO_CAPTURE;
    // 开启IO流
	ioctl(cam_fd, VIDIOC_STREAMON, &vtype);

	struct v4l2_buffer v4lbuf;
	bzero(&v4lbuf, sizeof(v4lbuf));
	v4lbuf.type = V4L2_BUF_TYPE_VIDEO_CAPTURE;
	v4lbuf.memory = V4L2_MEMORY_MMAP;

    char filename[64];
    memset(filename, 0, sizeof(filename));

	// 循环读取摄像头
	int i=0;
	while(1) {
	    // 从队列中取出数据填满缓存
		v4lbuf.index = i%nbuf;
        // VIDIOC_DQBUF出队，摄像头没数据时阻塞
		ioctl(cam_fd, VIDIOC_DQBUF, &v4lbuf);

        // 保持图片路径
        strcpy(filename, "./jpg/");
        get_current_time(filename);
        strcat(filename, ".jpg");
        // 保存
        FILE *file = fopen(filename, "wb");
        if (file != NULL) {
            fwrite(start[v4lbuf.index], v4lbuf.bytesused, 1, file);
            fclose(file);
        }

		// 将已经读到数据的缓存块重新置入队列中
		v4lbuf.index=i%nbuf;
		ioctl(cam_fd, VIDIOC_QBUF, &v4lbuf);

		i++;
	}


    // 关闭IO流（丢掉缓冲区数据）
    ioctl(cam_fd, VIDIOC_STREAMOFF, &vtype);
    // 关闭摄像头
    close(cam_fd);
}
