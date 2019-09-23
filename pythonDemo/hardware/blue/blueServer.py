'''
@Description: 蓝牙服务器
@Version: 1.0
@Autor: lhgcs
@Date: 2019-09-17 09:53:08
@LastEditors: lhgcs
@LastEditTime: 2019-09-19 09:42:50
'''


'''
sudo apt-get install libbluetooth-dev
sudo pip install pybluez
'''

'''
通信方式：
通过RFCOMM方式进行通信
通过L2CAP方式进行通信（端口是0x1001到0x8FFF之间的奇数端口，默认的连接可以传送的可靠报文是672个字节）
'''


import bluetooth
import time

blueDevice = []


'''
@description: 查找设备
@param {type} 
@return: 
'''
def find_device():
    foundDevs = bluetooth.discover_devices(lookup_names=True)
    print("found %d devices" % len(foundDevs))
    for (addr,name) in foundDevs:
        if addr not in blueDevice:
            print("Bluetooth Device:", str(name), "MAC address", str(addr))
            blueDevice.append(addr)


'''
@description: 服务端
@param {type} 
@return: 
'''
def blue_server():
    # 创建套节字监听端口,串行仿真协议RFCOMM
    sk = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    # 允许任何地址的主机连接
    sk.bind(('', bluetooth.PORT_ANY))
    # 监听端口
    sk.listen(1)
    
    uuid = "00001101-0000-1000-8000-00805f9b34fb"
    bluetooth.advertise_service(sk, "SampleServer", service_id=uuid)
    
    port=sk.getsockname()[1]
    print("Waiting for connection on RFCOMM channel %d" % port)

    #阻塞等待
    sock, address = sk.accept()
    print(str(address[0]))
    sock.settimeout(2)

    while True:
        try:
            # 接收1024字节， 自动阻塞
            recv = sock.recv(1024).decode("utf-8")
            print(recv)
            sock.send("123")
        except Exception as e:
            print(e)

    sock.close()
    sk.close()


if __name__ == "__main__":
    find_device()
    blue_server()
    