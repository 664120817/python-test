import  socket
#创建套接字
tcp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#创建连接
tcp_client_socket.connect(("www.xinshipu.com",80))
# 拼接请求协议
request_line = "GET/HTTP/1.1\r\n" #请求行
request_header = "Host:www.xinshipu.com\r\n"#请求头
request_blank = "\r\n"#请求空行
request_data =request_line+request_header+request_blank  #整体拼接
tcp_client_socket.send(request_data.encode()) #发送请求协议
recv_data=tcp_client_socket.recv(4096)
recv_text=recv_data.decode()
print(recv_text)

tcp_client_socket.close()
