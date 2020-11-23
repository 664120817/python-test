class MyFile(object):
    def __enter__(self): #上文方法
        print("进入上文")
        self.file=open(self.file_name,self.file_model)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb): #下文方法
        self.file.close()
        print("关闭文件")
    def __init__(self,file_name,file_model):
        self.file_name =file_name
        self.file_model=file_model

if __name__ == '__main__':
    with MyFile(r"C:\Users\Administrator\Desktop\20170415074136494\爱情是什么.txt","r") as f:
        print(f.read())
from contextlib import contextmanager

@contextmanager
def myopen(file_name,file_model):
    #打开文件
    file = open(file_name,file_model)
    #返回资源
    yield file
    #下文
    file.close()

with myopen(r"C:\Users\Administrator\Desktop\20170415074136494\缺口.txt","r") as f:
    print("\n"*10,f.read())