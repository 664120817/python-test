
import asyncore,sys,threading,time
from queue import Queue
DATA_PACKET_TYPE_SEND=689
DATA_PACKET_TYPE_RECV=690
def encode_content(content):
    """
    序列化函数
    :param content:
    :return:
    """
    if isinstance(content,str):#判断是否为字符串
        return content.replace(r'@',r'@A').replace(r'/',r'@S')
    elif isinstance(content,dict):
        return r'/'.join(["{}@={}".format(encode_content(k),encode_content(v))for k,v in content.items()])+r'/'
    elif isinstance(content, list):
        return r'/'.join([encode_content(i) for i in content])+r'/'
    return ""
def decode_to_str(content):
    """
    反序列化字符串
    :param content:字符串数据
    :return:
    """
    if isinstance(content,str):
        return content.replace(r'@S',r'/').replace(r'@A',r'@')
    return ""
def decode_to_dict(content):
    """
    反序列 字典
    :param content: 字典数据
    :return:
    """
    ret_dic = dict()
    if isinstance(content,str):
        item_strings=content.split(r"/")
        for item in item_strings:
            k_v_list=item.split(r"@=")
            if k_v_list is not None and len(k_v_list)>1:
                k=decode_to_str(k_v_list[0])
                v=decode_to_str(k_v_list[1])
                ret_dic [k]=v
    return ret_dic
def decode_to_list(content):
    """
    反序列 列表
    :param content:
    :return:
    """
    ret_list=list()
    if isinstance(content, str):
        lss=content.split(r"/")
        for idx,ls in enumerate(lss,):
            print(ls)
            if idx<len(lss)-1:
                if isinstance(ls, str):
                   ret_list.append(decode_to_str(ls))
                elif isinstance(ls, dict):
                    ret_list.append(decode_to_dict(ls))
                elif isinstance(ls, list):
                    ret_list.append(decode_to_list(ls))
    return ret_list

class Datapacket():
    def __init__(self,type=DATA_PACKET_TYPE_SEND,content="",data_bytes=None):
        if data_bytes is  None:
            self.type=type #数据包的类型
            self.content=content#数据部分内容
            self.encrypt_flag=0 #加密字段
            self.preserve_flag=0#保留字段
        else:
            self.type=int.from_bytes(data_bytes[4:6],byteorder='little',signed=False)
            self.encrypt_flag=int.from_bytes(data_bytes[6:7],byteorder='little',signed=False)
            self.preserve_flag=int.from_bytes(data_bytes[7:8],byteorder='little',signed=False)
            #构建数据部分
            self.content=str(data_bytes[8:-1],encoding='utf-8')

    def get_length(self):
        #获取当前数据包的长度，为以后需要发送数据包做准备
        return 4 +2+1+1 +len(self.content.encode('utf-8'))+1
    def get_bytes(self): #通过数据包转换成 二进制数据类型
        data=bytes()
        #构建4个字节的消息长度数据
        data_packet_length=self.get_length()
        # to_bytes 把一个整型数据转换成二进制数据
        #第一个参数 表示需要转换的二进制数据占几个字节
        #byteorder 第二个参数 描述字节序
        #设置是否有符号

        data+=data_packet_length.to_bytes(4,byteorder='little',signed=False)#处理消息长度 byteorder='little'设置成小端整型
        data+=self.type.to_bytes(2,byteorder='little',signed=False) #处理消息类型 signed=False设置无符号
        data += self.encrypt_flag.to_bytes(1,byteorder='little',signed=False)#处理加密字段
        data += self.preserve_flag.to_bytes(1,byteorder='little',signed=False)# 处理保留字段
        data += self.content.encode('GBK') #处理数据内容
        #数据结束要添加 \0 数据
        data+=b'\0'
        return data
class DouyuClient(asyncore.dispatcher):
    # 实现类的回调函数代码
    def __init__(self, host, port,callback=None):
        self.send_queue=Queue()#存放发送数据包对象
        self.recv_queue=Queue()#存放接收数据包对象
        self.callback=callback# 定义外部传入的自定义回调函数
        asyncore.dispatcher.__init__(self)  # 调用父类方法
        self.create_socket()# 创建Socker对象
        address = (host, port)
        self.connect(address)# 连接服务器
        #构建一个专门处理接收数据包容器中的数据包的线程
        self.callback_thread=threading.Thread(target=self.do_callback)
        self.callback_thread.setDaemon(True)#守护线程
        self.callback_thread.start()
        #构建心跳线程
        self.heart_thread=threading.Thread(target=self.do_ping)
        self.heart_thread.setDaemon(True)  # 守护线程
        self.ping_runing=False #属性 查看是否ping_runing
        self.heart_thread.start()
    # 实现 handle_connect 回调函数
    def handle_connect(self):
        print("连接成功")
        self.start_ping()

    # 实现  writable 回调函数
    def writable(self):
        # return False  # 返回值为TRUE为可写，FLASE为不可写
        return self.send_queue.qsize()>0
    # 实现 handle_write 回调函数
    def handle_write(self):
        """内部实现服务器发送的代码
        调用 send方法发送数据，参数是字节数据
        self.send('hello world\n'.encode('utf-8'))"""
        #从发送数据包队列中获取数据包对象
        dp=self.send_queue.get()
         #获取数据包的长度,并发送给服务器
        dp_length=dp.get_length()
        dp_length_data=dp_length.to_bytes(4,byteorder='little',signed=False)
        self.send(dp_length_data)
        # 发送数据包二进制数据
        self.send(dp.get_bytes())
        self.send_queue.task_done()
    # 实现  readable 回调函数
    def readable(self):
        return True  # TRUE可读取数据

    # 实现 handle_read 回调函数
    def handle_read(self):
        # 主动接收数据，参数是需要接收数据的长度,返回数据是字节数据
        length_data=self.recv(4)#读取长度，二进制数据
        length=int.from_bytes(length_data,byteorder='little',signed=False)#通过二进制获取length 具体数据
        data = self.recv(length)#通过数据包长度获取数据
        dp=Datapacket(data_bytes=data)#通过二进制数据构建数据包对象
        self.recv_queue.put(dp)#把数据放入接收数据容器中



    # 实现 handle_error 回调函数
    def handle_error(self):
        # 编写处理错误的方法
        t, e, trace = sys.exc_info()
        print(t, e, trace)
        self.close()  # 发生错误时，实现关闭操作

    # 实现 handle_close 回调函数
    def handle_close(self):
        print("连接关闭")
        self.stop_ping()
        self.close()

    def login_room_id(self,room_id):
        #构建登陆数据包
        self.room_id=room_id
        print(room_id)
        send_data={
            "type":"loginreq",
            "roomid":str(room_id)
        }
        content="type@=loginreq/roomid@={}/".format(send_data)
        login_dp=Datapacket(DATA_PACKET_TYPE_SEND,content=content)
        #把数据包添加到发送数据包容器中
        self.send_queue.put(login_dp)

    def join_room_group(self):
        """
        加入弹幕分组
        :return:
        """
        send_data={
            "type":"joingroup",
            "rid":str(self.room_id),
            "gid":"-9999"
        }
        content=encode_content(send_data)
        dp=Datapacket(type=DATA_PACKET_TYPE_SEND,content=content)
        self.send_queue.put(dp)

    def send_heart_data_packet(self):
        send_data={
            "type":"mrkl"
        }
        content=encode_content(send_data)
        dp=Datapacket(type=DATA_PACKET_TYPE_SEND,content=content)
        self.send_queue.put(dp)
    def start_ping(self):
        """
        开启心跳
        :return:
        """
        self.ping_runing=True

    def stop_ping(self):
        """
        关闭心跳
        :return:
        """
        self.ping_runing = False
    def do_ping(self):
        """
        执行心跳
        :return:
        """
        while True:
            if self.ping_runing:
               self.send_heart_data_packet()
               time.sleep(40)
    def do_callback(self):
        #专门负责处理接收数据包容器中的数据
        while True:
            dp=self.recv_queue.get()#从接受数据包容器中获取数据包
            #对数据进行处理
            if self.callback is not None:
                self.callback(self,dp)
            self.recv_queue.task_done()
            pass
def data_callback(client,dp):
    """
    自定义回调函数
    :return:
    """
    resp_data =decode_to_dict(dp.content)
    # print(resp_data)
    try:
        if resp_data["type"] =="loginres":
            #调用加入分组请求
            client.join_room_group()
            # print("登陆成功",resp_data)
            # print("data_callback:", resp_data)
        elif resp_data["type"]=="chatmsg":
            print("{}:{}".format(resp_data["nn"],resp_data["txt"]))
            pass
        elif resp_data["type"]=="onlinegift":#暴击鱼丸
            print("暴击鱼丸")
        elif resp_data["type"] == "uenter":
            print("{} 进入房间".format(resp_data["nn"]))
    except Exception:
        pass

if __name__ == "__main__":
    client=DouyuClient('openbarrage.douyutv.com',8601,callback=data_callback)
    #开始启动运行循环
    client.login_room_id('4403598')
    asyncore.loop(timeout=10)
    # data={
    #     "a":"b@d",
    #     "c":"d/b"
    # }
    # data="a@=b/c@=d"
    # data=["ath","b/a","c@h","123",{'a':'b'},["c@h","123",{'a':'b'}]]
    # # data=["a","a/b","c@f"]
    # print(encode_content(data))
    # print(decode_to_list(encode_content(data)))