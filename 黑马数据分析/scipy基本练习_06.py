import numpy as np
import pandas as pd
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import scipy.fftpack as fft
#读取图片数据
plt.figure(figsize=(15,10),dpi=88)
moon_data=plt.imread('登月.jpg')
print(moon_data.shape)
plt.imshow(moon_data,cmap='gray') #cmap='gray' 指定颜色
# plt.show()
#使用scipy中快速傅里叶转换进行变换
moon_data_fft=fft.fft2(moon_data)
print(moon_data_fft.max(),moon_data_fft.min())
#根据条件进行虑波
moon_data_fft=np.where(np.abs(moon_data_fft)>1e5,0,moon_data_fft)
print(moon_data_fft)
#傅里叶逆转换
moon_data_ifft=fft.ifft2(moon_data_fft)
#去除虚部
moon_data_result = np.real(moon_data_ifft)
moon_data_result=np.int16(moon_data_result)
plt.imshow(moon_data_result,cmap = 'gray')
# plt.show()

#使用scipy.integrate进行积分，调用quad()方法
from scipy import integrate
x=np.linspace(-1,1,1000)
f=lambda x:(1-x**2)**0.5
pi_1,err = integrate.quad(f,-1,1)
print(pi_1,err)
pi=pi_1*2
print(pi)

#scipy 文件输入/输出
from scipy import io
nd=np.random.randint(0,150,size=(10,5))
io.savemat('nd',{'data':nd})  #以二进制保存 没有后缀名
#io.loadmat()读取数据
data1=io.loadmat('nd')
# print(data1)
#读写图片使用scipy 中 misc.imread()/imsave()  更多使用百度查询
from scipy import misc
data_girl=misc.imread('girl.jpeg')
print(data_girl)
plt.imshow(np.uint8(data_girl))
plt.show()

