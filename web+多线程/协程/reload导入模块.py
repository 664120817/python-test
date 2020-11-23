import sys

print(sys.path) #查看环境变量具体内容
sys.path.append("路径") #添加指定路径 到环境变量中  但是不是添加系统中  添加在后面
sys.path.insert("路径")  #同上  插入在前面


from imp import reload
reload("导入模块") #解决重复导入

# import 模块.变量   直接引用原变量 会影响原模块变量值

# from 模块 import *  拷贝原变量 在本模块中使用  不会影响原模块变量值
