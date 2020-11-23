from application import utils
from application import urls
def parse_request(new_client_socket,ip_port):
    # 接收客户端浏览器发送的请求
    request_data = new_client_socket.recv(1024)
    # 判断协议是否为空
    if not request_data:
        print("{}客户端已下线".format(ip_port))
        new_client_socket.close()
        return
    # 根据客户端浏览器请求的资源路径，返回请求资源,
    # 1,把请求协议解码，得到请求报文的字符串
    request_text = request_data.decode('GBK')
    # 2，得到请求行
    # (1),查找第一个 \r\n 出现的位置
    loc = request_text.find('\r\n')
    print(loc, "abc")
    # (2),截取字符串
    request_line = request_text[:loc]
    print(request_line, "666")
    # (3),按空格拆分得到一个列表
    request_line_list = request_line.split(" ")
    # (4),得到请求路径
    file_path = request_line_list[1]
    print("{}正在请求{}路径".format(ip_port, file_path))
    if file_path == "/":
        file_path = "/a.html"
    return file_path


def application(current_dir,new_client_socket,ip_port):
    #定义变量保存资源路径
    file_path =parse_request(new_client_socket,ip_port)
    #改进动态判断后缀
    if file_path.endswith(".py"): #让.py 和 .html 的内容区别开
        #根据不同内容显示不同的资源内容
        if file_path in urls.route_dict:
            response_body =urls.route_dict[file_path]()
            request_data = utils.create_http_response("200 OK", response_body.encode())  # 调用utils模块处理拼接响应协议

        else:
            response_body = "Sorry page Not Found! 404".encode()
            request_data = utils.create_http_response("404 Not Found", response_body)  # 调用utils模块处理拼接响应协议





    else:
        resource_path = current_dir +str(file_path)

        try:
            with open(resource_path, "rb") as file:
                response_body = file.read()
                request_data=utils.create_http_response("200 OK",response_body)#调用utils模块处理拼接响应协议
        except Exception as e:
            response_body = "Error!{}".format(str(e)).encode()
            request_data = utils.create_http_response("404 Not Found", response_body)  # 调用utils模块处理拼接响应协议
    return request_data