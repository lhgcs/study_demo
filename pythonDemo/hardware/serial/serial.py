import serial
import GlobalVarible
import threading
import time
from ProcMsg import ProcMsg

ser = serial.Serial('com2', 38400, timeout=0.5)
index = 0
i = 0


def loop():
    print("串口状态:" + str(ser.is_open))
    while ser.isOpen():
        if (ser.in_waiting > 0):
            buffer = ser.read(ser.in_waiting)
            i = len(buffer)
            p = ProcMsg(buffer)
            print(type(buffer))
            p.proc()
        elif (ser.in_waiting <= 0):
            time.sleep(1)
           


t = threading.Thread(target=loop(), name="LoopThread")
t.start()

t.join()
