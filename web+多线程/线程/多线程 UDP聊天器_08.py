#coding=utf-8
from socket import *
import threading,time
def main ():
    #1、创建socket套接字
    udpSocket = socket(AF_INET,SOCK_DGRAM)

    #2、准备接收方的地址
    sendAddress = ("",8888)
    udpSocket.bind(sendAddress)
    #创建子线程，单独接收用户发送消息
    udp_recv=threading.Thread(target=recv_msg,args=(udpSocket,))
    #子线程守护主线程
    udp_recv.setDaemon(True)  # 如果主线程结束 子线程也结束
    udp_recv.start()
    while True:
        time.sleep(0.1)
        print("\n\n1 发送信息:")
        print("2 退出系统:")
        sel_num=int(input("请输入选项:\n"))
        if sel_num ==1:
            send_msg(udpSocket)
        elif sel_num == 2:
            print("系统即将退出")
            break
    udpSocket.close()

#3、从键盘输入需要发送的数据
def send_msg(udpSocket):
    ip=(input("请输入要发送的IP："))
    port=int(input("请输入要发送的端口："))
    sendAddress=(ip,port)
    sendData = input("请输入要发送的内容：")
    #4、发送数据到指定电脑
    udpSocket.sendto(sendData.encode(),sendAddress)
def  recv_msg(udpSocket):
    while True:
        #5、等待接收对方发送的数据
        recv_data,ip_port = udpSocket.recvfrom(1024)
        recv_text=recv_data.decode()
        #6、显示对方发送的数据
        print(recv_text)


if __name__ == '__main__':
    main()
