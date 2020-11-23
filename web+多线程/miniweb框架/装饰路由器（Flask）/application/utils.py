def create_http_response(status,response_body):
    # 拼接响应
    request_line = "HTTP/1.1 {}\r\n".format(status)  # 请求行
    request_header = "Server:python80WS/2.1\r\n"  # 请求头
    request_header += "Content-Type:text/html\r\n"

    request_blank = "\r\n"  # 请求空行
    request_data = (request_line + request_header + request_blank).encode() + response_body  # 整体拼接
    return request_data