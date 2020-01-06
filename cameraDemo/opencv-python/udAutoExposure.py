import cv2
import time
import numpy as np

frameNumber = 0
latestFps = 0
t1 = time.time()
udExposure = -3.0

# 分辨率
capW = 1920
capH = 1080

def getFPS2():
    global t1, frameNumber, latestFps
    frameNumber += 1
    t2 = time.time()
    if (t2 - t1 >= 1):
        latestFps = frameNumber
        t1 = time.time()
        frameNumber = 0
    return latestFps

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, capW)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, capH)

def getPixelAvgValue(frame):
    pixelNumber = frame.shape[0] * frame.shape[1]
    sumB = np.sum(frame[:, :, 0]) / pixelNumber
    sumG = np.sum(frame[:, :, 1]) / pixelNumber
    sumR = np.sum(frame[:, :, 2]) / pixelNumber
    avgValue = (sumB + sumG + sumR) / 3
    print(avgValue, flush = True)
    return avgValue

udAutoExposureTimer = time.time()
def udAutoExposure(cap, frame):
    global udExposure
    global udAutoExposureTimer
    avgValue = getPixelAvgValue(frame)
    if (time.time() - udAutoExposureTimer >= 2):
        udAutoExposureTimer = time.time()
        if (avgValue - 128 > 25):
            udExposure -= 1
        elif (avgValue - 128 < -25):
            udExposure += 1
        else:
            print("ud exposure ok")
    print("udExposure:", udExposure)
    cap.set(cv2.CAP_PROP_EXPOSURE, udExposure)

while True:
    ret,frame = cap.read()
    udAutoExposure(cap, frame)
    exposure = cap.get(cv2.CAP_PROP_EXPOSURE)
    brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
    print("exposure", exposure, "brightness", brightness, flush = True)
    isAutoExposure = cap.get(cv2.CAP_PROP_AUTO_EXPOSURE)
    print("isAutoExposure", isAutoExposure, flush = True )
    fps = getFPS2()
    cv2.putText(frame, "fps:" + str(fps), (20, 100), 1, 3, (255, 255, 255), 12)
    cv2.putText(frame, "fps:" + str(fps), (20, 100), 1, 3, (0, 0, 255), 3)
    cv2.imshow("frame", frame)
    key = cv2.waitKey(30)
    if key == 27 or key == 32 or key == 13:
        break