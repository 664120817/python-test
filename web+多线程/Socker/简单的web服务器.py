import socket

def main():
    #创建套接字
    tcp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #设置地址重用
    tcp_client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    #绑定端口
    tcp_client_socket.bind(("",8080))
    #4,设置监听（设置套接字为被动模式）
    tcp_client_socket.listen(128)
    #接收客户端连接 定义函数
    while True:
        new_client_socket,ip_port = tcp_client_socket.accept()
        request_handler(new_client_socket,ip_port)
def request_handler(new_client_socket,ip_port):
    #接收客户端浏览器发送的请求
    request_data = new_client_socket.recv(1024)
    #判断协议是否为空
    if not request_data:
        print("{}客户端已下线".format(ip_port))
        new_client_socket.close()
        return
    #拼接响应
    request_line = "HTTP/1.1 200 OK\r\n"  # 请求行
    request_header = "Server:python80WS/2.1\r\n"  # 请求头
    request_blank = "\r\n"  # 请求空行
    # response_body = "你好，陈豪欢迎你"
    # request_data = request_line + request_header + request_blank +response_body  # 整体拼接
    # #发送报文
    # new_client_socket.send(request_data.encode())
    with open(r"C:\Users\Administrator\Desktop\信任区\664120817.github.io-master\3D相册.html","rb") as file:
        response_body = file.read()
    request_data = (request_line + request_header + request_blank).encode() + response_body  # 整体拼接
    # 发送报文
    new_client_socket.send(request_data)

    #关闭当前连接
    new_client_socket.close()

if __name__ == "__main__":
    main()