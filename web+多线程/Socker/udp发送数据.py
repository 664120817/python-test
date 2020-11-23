#coding=utf-8
from socket import *

#1、创建socket套接字
#socket(参数1，参数2)
#参数1 = AF_INET固定的
#参数2 = SOCK_DGRAM表示udp，上篇文章中说过SOCK_STREM表示tcp
udpSocket = socket(AF_INET,SOCK_DGRAM)

#2、准备接收方的地址
sendAddress = ("192.168.121.1",8888)
udpSocket.bind(sendAddress)
#3、从键盘输入需要发送的数据
sendData = input("请输入要发送的数据：")

#4、发送数据到指定电脑
udpSocket.sendto(sendData.encode(),sendAddress)

#5、等待接收对方发送的数据
receiveData,ip_port = udpSocket.recvfrom(1024)

#6、显示对方发送的数据
print(receiveData.decode('utf-8'))
#5、关闭socket套接字
udpSocket.close()