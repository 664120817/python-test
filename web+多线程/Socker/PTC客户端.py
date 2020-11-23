#导入模块
import socket
#2.创建套接字
tcp_server_socker =socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#3，建立连接
tcp_server_socker.connect(("192.168.121.1",8080))
#4,发送数据
tcp_server_socker.send("约吗".encode())
#接收数据
recv_data=tcp_server_socker.recv(1024)
print(recv_data)
#5,关闭套接字
tcp_server_socker.close()