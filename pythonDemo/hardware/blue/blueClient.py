'''
@Description: 蓝牙客户端
@Version: 1.0
@Autor: lhgcs
@Date: 2019-09-17 09:53:08
@LastEditors: lhgcs
@LastEditTime: 2019-09-19 10:15:55
'''


'''
sudo apt-get install libbluetooth-dev
sudo pip install pybluez
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

        services = bluetooth.find_service(address=addr)
        for svc in services:
            print("Service Name: %s"    % svc["name"])
            print("    Host:        %s" % svc["host"])
            print("    Description: %s" % svc["description"])
            print("    Provided By: %s" % svc["provider"])
            print("    Protocol:    %s" % svc["protocol"])
            print("    channel/PSM: %s" % svc["port"])
            print("    svc classes: %s "% svc["service-classes"])
            print("    profiles:    %s "% svc["profiles"])
            print("    service id:  %s "% svc["service-id"])
            print("")


'''
@description: 客户端
@param {type} 
@return: 
'''
def client(_id, ch):
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.settimeout(None)
    sock.connect((_id, ch))
    sock.setblocking(False)
    print("connect")
    while True:
        try:
            # 接收1024字节， 自动阻塞
            #recv = sock.recv(1024).decode("utf-8")
            #print(recv)
            sock.send("123")
        except Exception as e:
            print(e)

    sock.close()


if __name__ == "__main__":
    find_device()
    addr = "AC:83:F3:4A:70:EB"
    ch = 1
    client(addr, ch)
    