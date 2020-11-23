import socket

def main():
    #创建套接字
    tcp_client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #设置地址重用
    tcp_client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,True)
    #绑定端口
    tcp_client_socket.bind(("",8081))
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
    #根据客户端浏览器请求的资源路径，返回请求资源,
    #1,把请求协议解码，得到请求报文的字符串
    request_text =request_data.decode()
    #2，得到请求行
    #(1),查找第一个 \r\n 出现的位置
    loc=request_text.find('\r\n')
    print(loc,"abc")
    #(2),截取字符串
    request_line = request_text[:loc]
    print(request_line,"666")
    #(3),按空格拆分得到一个列表
    request_line_list =request_line.split(" ")
    #(4),得到请求路径
    file_path = request_line_list[1]
    print("{}正在请求{}路径".format(str(ip_port),str(file_path)))
    if file_path == "/":
        file_path ="/a.html"
    #拼接响应
    request_line = "HTTP/1.1 200 OK\r\n"  # 请求行
    request_header = "Server:python80WS/2.1\r\n"  # 请求头
    request_blank = "\r\n"  # 请求空行
    try:
        with open("static"+ str(file_path),"rb") as file:
            response_body = file.read()
    except Exception as e :
        request_line ="HTTP/1.1 404 Not Found\r\n" #修改响应行 404
        response_body = "Error!{}".format(str(e)).encode()
    request_data = (request_line + request_header + request_blank).encode() + response_body  # 整体拼接
    # 发送报文
    new_client_socket.send(request_data)

    #关闭当前连接
    new_client_socket.close()

if __name__ == "__main__":
    main()