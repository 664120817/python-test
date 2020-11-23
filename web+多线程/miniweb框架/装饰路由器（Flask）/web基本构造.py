import socket
import threading
from application import app
class WebServer(object):
    def __init__(self):
        # 创建套接字
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置地址重用
        tcp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口
        tcp_client_socket.bind(("", 8082))
        # 4,设置监听（设置套接字为被动模式）
        tcp_client_socket.listen(128)
        self.tcp_client_socket =tcp_client_socket

        pass
    def start(self):
        while True:
            new_client_socket,ip_port = self.tcp_client_socket.accept()
            handler_thread = threading.Thread(target=self.request_handler, args=(new_client_socket, ip_port))
            # 子线程守护主线程
            handler_thread.setDaemon(True)  # 如果主线程结束 子线程也结束
            handler_thread.start()

    def request_handler(self,new_client_socket,ip_port):
        request_data =app.application("static",new_client_socket,ip_port)
        # 发送报文
        new_client_socket.send(request_data)

        #关闭当前连接
        new_client_socket.close()
def main():
       ws =WebServer()
       ws.start()
if __name__ == "__main__":
    main()