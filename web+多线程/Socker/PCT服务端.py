#导入模块
import socket
#2.创建套接字
tcp_server_socker =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#设置套接字地址可重复使用
tcp_server_socker.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
#3绑定端口 ip
tcp_server_socker.bind(('',8080))
#4,开启监听（设置套接字为被动模式） 不能主动发数据
tcp_server_socker.listen(128) #windows 128 允许最大连接数  在linux无效
#5，等待客户端连接 ,接收客户端连接 程序阻塞 直到客户端连接 才解阻
#返回一个新的套接字socker 客户端的ip和端口号
while True:
    new_client_socket,client_ip_port =tcp_server_socker.accept()
    #收发数据
    while True:
        #recv 让程序再次阻塞 ，收到数据后解阻
        recv_data =new_client_socket.recv(1024)
        if recv_data:
            recv_text =recv_data.decode('GBK')
            print(recv_text)
            break
        else:
            print("客户端已断开")
            break
        new_client_socket.close() #关闭当前客户端服务
#关闭连接
tcp_server_socker.close()
