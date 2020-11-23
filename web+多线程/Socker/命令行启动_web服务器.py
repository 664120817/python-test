import socket
import sys

from application import app
class WebServer(object):
    def __init__(self,port):
        # 创建套接字
        tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置地址重用
        tcp_client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口
        tcp_client_socket.bind(("",port))
        # 4,设置监听（设置套接字为被动模式）
        tcp_client_socket.listen(128)
        self.tcp_client_socket =tcp_client_socket

        pass
    def start(self):
        #启动成功提示
        print("web服务器已经启动，等待客户端连接")
        while True:
            new_client_socket,ip_port = self.tcp_client_socket.accept()
            self.request_handler(new_client_socket,ip_port)
    def request_handler(self,new_client_socket,ip_port):
        request_data =app.application("static",new_client_socket,ip_port)
        # 发送报文
        new_client_socket.send(request_data)

        #关闭当前连接
        new_client_socket.close()
def main():
      #获取系统传递参数
    params_list =sys.argv
      #判断参数格式是否正确
    if len(params_list) !=2:
          print("启动失败，参数格式不对！正确格式:python3 文件.py 端口")
          return
    if  not sys.argv[1].isdigit():
        print("启动失败，端口不是纯数字")
        return
    #获取端口号
    port = int(sys.argv[1])

    ws =WebServer(port)
    ws.start()
if __name__ == "__main__":
    main()