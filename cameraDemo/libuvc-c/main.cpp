#include <stdio.h>
#include <unistd.h>
#include <string.h>

#include "libuvc/libuvc.h"

#include "opencv2/opencv.hpp"
#include "opencv2/core.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/imgproc.hpp"

using namespace cv;

/**
 * @description: 用opencv显示图像
 * @param {type} 
 * @return: 
 */
void show_bgr_image(uvc_frame_t *frame) {
    // 创建图像，此构造函数不创建图像数据所内存，而是直接使用 data 所指内存，图像的行步长由 step 指定；
    cv::Mat mat(cv::Size(frame->width, frame->height), CV_8UC3, (unsigned char *)(frame->data));
    cv::namedWindow("test", cv::WINDOW_AUTOSIZE);
    cv::imshow("test", mat);
    waitKey(100);
}

/**
 * @description: YUV 转 BGR
 * @param {type} 
 * @return: 
 */
int yuyv2rgb(uvc_frame_t *frame, uvc_frame_t *bgr) {
    uvc_error_t res;

    // 分配内存
    bgr = uvc_allocate_frame(frame->width * frame->height * 3);
    if (NULL == bgr) {
        printf("unable to allocate bgr frame!");
        return -1;
    }
    // 转换
    res = uvc_any2bgr(frame, bgr);
    if (res < 0) {
        uvc_perror(res, "uvc_any2bgr");
        uvc_free_frame(bgr);
        return -1;
    }
    show_bgr_image(bgr);
    uvc_free_frame(bgr);
    return 0;
}

/**
 * @description: JPEG 转 BGR
 * @param {type} 
 * @return: 
 */
int mjpeg2rgb(uvc_frame_t *frame, uvc_frame_t *bgr) {
    uvc_error_t res;

    // 分配内存
    bgr = uvc_allocate_frame(frame->width * frame->height * 3);
    if (NULL == bgr) {
        printf("unable to allocate bgr frame!");
        return -1;
    }
    // 转换
    res = uvc_mjpeg2bgr(frame, bgr);
    if (res < 0) {
        uvc_perror(res, "uvc_mjpeg2bgr");
        uvc_free_frame(bgr);
        return -1;
    }
    show_bgr_image(bgr);
    uvc_free_frame(bgr);
    return 0;
}

/**
 * @description: 设备描述
 * @param {type} 
 * @return: 
 */
void get_camera_descript(uvc_device_t *dev) {
    uvc_device_descriptor_t *desc;
    uvc_error_t res = uvc_get_device_descriptor(dev, &desc);
    if (res ==  UVC_SUCCESS) {
        printf("vid=%d pid=%d", desc->idVendor, desc->idProduct);
        uvc_free_device_descriptor(desc);
    }
}

/**
 * @description: 设置摄像头参数
 * @param {type} 
 * @return: 
 */
void set_camera_params(uvc_device_handle_t *devh) {
    // 优先保证帧率固定
    uvc_set_ae_priority(devh, 0);
    // 设置曝光模式，1: manual mode; 2: auto mode; 
    uvc_set_ae_mode(devh, 1);
    // 设置曝光时间 10ms
    uvc_set_exposure_abs(devh, 100);
    // 关闭自动白平衡
    uvc_set_contrast_auto(devh, 0);
}

/**
 * @description: 设置帧，只能设置10帧，分辨率不能过高
 * @param {type} 
 * @return: 
 */
int set_frame_params(uvc_device_handle_t *devh, uvc_stream_ctrl_t *ctrl, const char *format, int width, int height, int fps) {
    enum uvc_frame_format form = UVC_FRAME_FORMAT_ANY; // Any supported format
    if (0 == strcmp(format, "yuyv")) {
        form = UVC_FRAME_FORMAT_YUYV;
    } else if (0 == strcmp(format, "rgb")) {
        form = UVC_FRAME_FORMAT_RGB;
    } else if (0 == strcmp(format, "bgr")) {
        form = UVC_FRAME_FORMAT_BGR;
    } else if (0 == strcmp(format, "mjpeg")) {
        form = UVC_FRAME_FORMAT_MJPEG;
    }
    
    uvc_error_t res = uvc_get_stream_ctrl_format_size(devh, ctrl, form, width, height, fps);
    if (res < 0) {
        uvc_perror(res, "get_mode"); // 错误代码,自定义信息
    } 
    return res < 0 ? -1 : 0;
}

/**
 * @description: 获取增益
 * @param {type} 
 * @return: 
 */
int get_gain(uvc_device_handle_t *devh) {
    uint16_t value = 0;
    uvc_error_t res = uvc_get_gain(devh, &value, UVC_GET_CUR);
    printf("gain=%d\n", value);
    return res < 0 ? -1 : value;
}

/* This callback function runs once per frame. Use it to perform any
 * quick processing you need, or have it put the frame into your application's
 * input queue. If this function takes too long, you'll start losing frames. */
void cb(uvc_frame_t *frame, void *ptr) {
    uvc_frame_t *bgr;

    if (frame->frame_format == UVC_FRAME_FORMAT_MJPEG) {
        int res = mjpeg2rgb(frame, bgr);
        if (0 == res) {
        }
    } else {
        int res = yuyv2rgb(frame, bgr);
        if (0 == res) {
        }
    }

  /* Call a user function:
   *
   * my_type *my_obj = (*my_type) ptr;
   * my_user_function(ptr, bgr);
   * my_other_function(ptr, bgr->data, bgr->width, bgr->height);
   */
  /* Call a C++ method:
   *
   * my_type *my_obj = (*my_type) ptr;
   * my_obj->my_func(bgr);
   */
}

int main(int argc, char **argv) {
    uvc_context_t *ctx;
    uvc_device_t *dev;
    uvc_device_handle_t *devh;
    uvc_stream_ctrl_t ctrl;
    uvc_error_t res;
    
    int isFindDevice = 0;    // 发现设备
    int isOpenDevice = 0;    // 打开设备
    int isOpenStream = 0;    // 打开流
    int isOpenStreaming = 0; // 打开流线程

    /* Initialize a UVC service context. Libuvc will set up its own libusb
    * context. Replace NULL with a libusb_context pointer to run libuvc
    * from an existing libusb context. */
    res = uvc_init(&ctx, NULL);
    if (res < 0) {
        uvc_perror(res, "uvc_init");
        return res;
    }
    puts("UVC initialized");

    /* Locates the first attached UVC device, stores in dev */
    res = uvc_find_device(
        ctx, 
        &dev,// 设备
        0,   // vid 供应商ID
        0,   // pid 产品ID
        NULL // 序列号
        );
  
    if (res < 0) {
        uvc_perror(res, "uvc_find_device"); /* no devices found */
    } else {
        puts("Device found");
        isFindDevice = 1;

        /* Try to open the device: requires exclusive access */
        res = uvc_open(dev, &devh);
        if (res < 0) {
            uvc_perror(res, "uvc_open"); /* unable to open device */
        } else {
            isOpenDevice = 1;
            puts("Device opened");
            /* Print out a message containing all the information that libuvc
            * knows about the device */
            uvc_print_diag(devh, stderr);

            // 设置参数
            set_camera_params(devh);
            
            int f = 10;
            while(f > 0) {
                if (0 == set_frame_params(devh, &ctrl, "mjpeg", 2592, 1944, f)) {
                    printf("fps=%d ok\n", f);
                    break;
                } else {
                    printf("fps=%d error\n", f);
                }
                f--;
            }

        #if 0
            uvc_frame_t *frame;
            uvc_stream_handle_t *strmhp;
            // 打开流
            res = uvc_stream_open_ctrl(devh, &strmhp, &ctrl);
            if (res < 0) {
                uvc_perror(res, "can not open stream");
            } else {
                isOpenStream = 1;
            
                // // 开启视频流并回调
                // res = uvc_stream_start(
                //     strmhp,       // 设备
                //     cb,           // 回调函数
                //     (void*)12345, // 回调函数参数
                //     0);           // 流标志位（保留）
            
                int cnt = 0;
                while (++cnt < 10000) {
                    // 获取帧
                    res = uvc_stream_get_frame(strmhp, &frame, 0);// 10ms
                    if (res < 0) {
                        uvc_perror(res, "can not get stream");
                    } else {
                        show_bgr_image(frame);
                        // 释放帧
                        uvc_free_frame(frame);

                        get_gain(devh);
                        
                    }
                    sleep(1);
                }
            }
            if (isOpenStream) {
                // 停止流
                uvc_stream_stop(strmhp);
                // 关闭流
                uvc_stream_close(strmhp);
            }
        #else
            // 开启视频流并回调
            res = uvc_start_streaming(
                devh,         // 设备
                &ctrl,        // 控制块
                cb,           // 回调函数
                (void*)12345, // 回调函数参数
                0);           // 流标志位（保留）

            if (res < 0) {
                uvc_perror(res, "can not start streaming");
            } else {
                isOpenStreaming = 1;
                
                // 输出流控制块的值
                uvc_print_stream_ctrl(&ctrl, stderr);
                puts("Streaming...");
                // ******** 这里异常了 ********
                // 停止流视频关闭所有流，结束线程并取消轮询
                
                while(1) {
                    get_gain(devh);
                    sleep(2);
                }
                // uvc_stop_streaming(devh);
            }
        #endif
            /* Release our handle on the device */
            // uvc_close(devh);
        }
        /* Release the device descriptor */
        // uvc_unref_device(dev);
    }
    /* Close the UVC context. This closes and cleans up any existing device handles,
    * and it closes the libusb context if one was not provided. */

    if (isOpenStreaming) {
        uvc_stop_streaming(devh);
    }

    if (isOpenDevice) {
        uvc_close(devh);
        uvc_unref_device(dev);
        puts("Device closed");
        puts("Device unref");
    }
    
    if (isFindDevice) {
        uvc_exit(ctx);
        puts("UVC exited");
    }
    
    return 0;
}
