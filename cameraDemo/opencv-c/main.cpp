/*
 * @Description: opencv打开摄像头
 * @Version: 1.0
 * @Autor: lhgcs
 * @Date: 2019-08-19 14:50:33
 * @LastEditors: lhgcs
 * @LastEditTime: 2019-09-06 11:35:36
 */


#include <sys/time.h>
#include <unistd.h>
#include <chrono>
#include <iostream>
#include <stdio.h>
#include "opencv2/opencv.hpp"

using namespace cv;


/**
 * @description: 获取图像RGB通道的平均值
 * @param {type} 
 * @return: 
 */
unsigned char get_avg(Mat &img) {
	unsigned long num = 0;
	int row = img.rows;
	int col = img.cols;
	int channel = img.channels();
	
	channel = (channel > 3 ? 3:channel);
	int cols = col * channel;
	
	for(int i=0; i<row; i++) {
		unsigned char *p = img.ptr<unsigned char>(i);
		for(int j=0; j< cols; j++) {
			num +=p[j];
		}
	}
	return num/(row*cols);
}


/**
 * @description: 获取图像指定位置RGB通道的平均值
 * @param {type} 
 * @return: 
 */
unsigned char get_part_avg(Mat &img, int x1, int y1, int x2, int y2) {
	unsigned long num = 0;
	int row = img.rows;
	int col = img.cols;
	int channel = img.channels();
	channel = (channel > 3 ? 3:channel);
	int cols = col * channel;
	
	x1 = x1 < 0 ? 0 : x1;
	y1 = y1 < 0 ? 0 : y1;
	x2 = x2 > col ? col: x2;
	y2 = y2 < row ? row : y2;
	x1 *=channel;
	x2 *=channel;
	
	for(int i=y1; i<y2; i++) {
		unsigned char *p = img.ptr<unsigned char>(i);
		for(int j=x1; j<x2; j++) {
			num +=p[j];
		}
	}
	return num/((x2-x1)*(y2-y1));
}


/**
 * @description: 获取时间戳
 * @param {type} 
 * @return: 
 */
unsigned long get_timestamp() {
	struct timeval tv;
	gettimeofday(&tv, NULL);
	return (tv.tv_sec*1000 + tv.tv_usec/1000);
}


/**
 * @description: 调节曝光值
 * @param {type} 
 * @return: 
 */
void auto_exposure(VideoCapture &cap, Mat &img) {
	unsigned char currentAvgValue = 0;   // 当前图像的灰度平均值
    unsigned char targetValue = 128;     // 图像的灰度平均值
    unsigned char radius = 35;           // 偏值
    
	static unsigned long lastTime = 0;
    unsigned long currentTime = get_timestamp();
    if (currentTime - lastTime < 1200) {
		return;
	}
    
    float isAuto = cap.get(CV_CAP_PROP_AUTO_EXPOSURE);
    printf("isAuto:%f\n", isAuto);
    if(0.75 == isAuto) {
		return;
	}
    
    // currentAvgValue = get_avg(img);
    currentAvgValue = get_part_avg(img, 0, 0, 200,200);
    printf("%d\n", currentAvgValue);
    
    if (currentAvgValue < targetValue - radius) {
		unsigned int temp = (targetValue - currentAvgValue)/radius;
		temp *=temp;
		float value = cap.get(CV_CAP_PROP_EXPOSURE) + temp* 0.0025 + 0.0001;
		value = value > 1 ? 1 : value;
		
		int result = cap.set(CV_CAP_PROP_EXPOSURE, value);
		printf("%f\n", value);
		printf("%d\n", result);
	} else if (currentAvgValue > targetValue + radius) {
		unsigned int temp = (currentAvgValue - targetValue)/radius;
		temp *=temp;
		
		float value = cap.get(CV_CAP_PROP_EXPOSURE) - temp* 0.0025 + 0.0001;
		value = value < 0 ? 0 : value;
		
		int result = cap.set(CV_CAP_PROP_EXPOSURE, value);
		printf("%f\n", value);
		printf("%d\n", result);
	}
	
	lastTime = currentTime;
}


int main() {
	
	VideoCapture cap(8);
	if(!cap.isOpened()) {
		printf("open camera fail\n");
		return -1;
	}

	// 设置参数
	cap.set(CV_CAP_PROP_FRAME_WIDTH, 1920);
	cap.set(CV_CAP_PROP_FRAME_HEIGHT, 1080);
	cap.set(CV_CAP_PROP_FPS, 10);
	cap.set(CV_CAP_PROP_AUTO_EXPOSURE, 0.25);
	cap.set(CAP_PROP_AUTO_WB, 0);
	cap.set(CV_CAP_PROP_EXPOSURE, 0.22);
	cap.set(CAP_PROP_FOURCC, CV_FOURCC('M','J','P','G'));
	
	// 获取参数
	printf("%f\n",cap.get(CV_CAP_PROP_FRAME_WIDTH));
	printf("%f\n",cap.get(CV_CAP_PROP_FRAME_HEIGHT));
	printf("%f\n",cap.get(CV_CAP_PROP_FPS));
	printf("%f\n",cap.get(CV_CAP_PROP_EXPOSURE));
	printf("%f\n",cap.get(CV_CAP_PROP_GAIN));
	
	int cnt=0;
	int num = 0;
	float value = 0.26;
	
	while(true) {
		
		++cnt;
		auto start = std::chrono::system_clock::now();
		
		Mat frame;
		cap >> frame;

		auto_exposure(cap, frame);
		imshow("img", frame);
		
		auto end = std::chrono::system_clock::now();
		num += std::chrono::duration_cast<std::chrono::milliseconds>(end-start).count();
		
		if(num>=10000) {
			printf("fps:%d   %d  %f\n", cnt, num, value);
			cnt = 0;
			num = 0;
			value -=0.01;
		}
		
		if(waitKey(100) == 27) {
			break;
		}

	}
}

