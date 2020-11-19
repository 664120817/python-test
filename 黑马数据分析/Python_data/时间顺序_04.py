import pandas as pd
import numpy as np
from datetime import datetime
# now = datetime.now()
# print(now)
# print(now.year, now.month, now.day)
# delta = datetime(2011, 1, 7) - datetime(2008, 6, 24, 8, 15)
# print(delta) #（天，秒）
# print(delta.days)#天
# print(delta.seconds)#秒
# from datetime import timedelta
# start = datetime(2011, 1, 7)
# print(start + timedelta(12))
# print(start - 2 * timedelta(12))
#
# stamp = datetime(2011, 1, 3)
# print(str(stamp))
# print(stamp.strftime('%Y-%m-%d')) #指定时间格式
# value = '2011-01-03'
# print(datetime.strptime(value, '%Y-%m-%d'))  #把字串value 变成时间
# datestrs = ['7/6/2011', '8/6/2011']
# print([datetime.strptime(x, '%m/%d/%Y') for x in datestrs]) #字符串变时间

# #pandas 解析字符串变时间
# from dateutil.parser import parse
# # print(parse('2011-01-03'))
# print(parse('Jan 31, 1997 10:45 PM'))
# print(parse('6/12/2011', dayfirst=True))
# datestrs = ['2011-07-06 12:00:00', '2011-08-06 00:00:00']
# print(pd.to_datetime(datestrs))
# idx = pd.to_datetime(datestrs + [None])  #None 遗失值
# print(idx)
# # print(idx[2]) #取出遗失值
# # pd.isnull(idx)
#
#
# from datetime import datetime
# dates = [datetime(2011, 1, 2), datetime(2011, 1, 5),
#          datetime(2011, 1, 7), datetime(2011, 1, 8),
#          datetime(2011, 1, 10), datetime(2011, 1, 12)]
# ts = pd.Series(np.random.randn(6), index=dates)
# print(ts)
# print(ts.index)
# print(ts + ts[::2]) #相同index 相加
# print(ts.index.dtype)
# stamp = ts.index[0]
# print(stamp)
#
# stamp = ts.index[2]
# print(ts[stamp])
# print(ts['1/10/2011'])
# print(ts['20110110'])
# longer_ts = pd.Series(np.random.randn(1000),
#                       index=pd.date_range('1/1/2000', periods=1000))
# print(longer_ts)
# print(longer_ts['2001']) #索引 2001 值
# print(longer_ts['2001-05']) #索引 2001-05 值
# print(ts[datetime(2011, 1, 7):])   #索引切片 后面日期都要
# print(ts)
# print(ts['1/6/2011':'1/11/2011'])  #索引切片
# ts.truncate(after='1/9/2011') #after='1/9/2011' 日期后的不要  before日期之前的不要
# dates = pd.date_range('1/1/2000', periods=100, freq='W-WED')
# long_df = pd.DataFrame(np.random.randn(100, 4),
#                        index=dates,
#                        columns=['Colorado', 'Texas',
#                                 'New York', 'Ohio'])
# print(long_df.loc['5-2001']) #对标签索引
#
# #这一段还比较重要   生成日期
# # print(ts)
# resampler = ts.resample('W-SUN')  #根据时间戳来分组  ts.resample('W-SUN').mean()
# print("666",list(resampler))
#
# index = pd.date_range('2012-04-01', '2012-06-01') #生成'2012-04-01', '2012-06-01' 时间段
# print(pd.date_range(start='2012-04-01', periods=20))  #生成'2012-04-01',为开头的20个  时间段
# print(pd.date_range(end='2012-06-01', periods=20)) #生成'2012-06-01',为结尾的 前20个  时间段
# print(pd.date_range('2000-01-01', '2000-12-01', freq='BM'))  #生成 每个月的最后一天  时间段
# print(pd.date_range('2012-05-02 12:56:31', periods=5))  #往后生成5个  以天为单位的这样时间
# print(pd.date_range('2012-05-02 12:56:31', periods=5, normalize=True))   #normalize=True生成时间 保留到天
# print(pd.date_range('2000-01-01', '2000-02-01', freq='4h'))  # freq='4h' 每隔4小时生成一段时间 更多freq去百度
#
#
#
# p = pd.Period(2007, freq='A-DEC')  #A 代表年
# print(p)
# print(p + 5)
# print(p - 2)
# print(pd.Period('2014', freq='A-DEC')-p)
# rng = pd.period_range('2000-01-01', '2000-06-30', freq='M') #按月生成
# print(rng)
# pd.Series(np.random.randn(6), index=rng)  #用生成的rng 当index
# values = ['2001Q3', '2002Q2', '2003Q1']
# index = pd.PeriodIndex(values, freq='Q-DEC') #
# print(index)
#
# p = pd.Period('2007', freq='A-DEC')
# print(p)
# p.asfreq('M', how='start')  #生成最开始月  2007-01
# p.asfreq('M', how='end')#生成最后月  2007-12
# p = pd.Period('2007', freq='A-JUN')  #结束月
# print(p)
# p.asfreq('M', 'start')  #求开始月
# p.asfreq('M', 'end')   #结束月
# p = pd.Period('Aug-2007', 'M')
# p.asfreq('A-JUN') #这个月份属于哪个年度
# rng = pd.period_range('2006', '2009', freq='A-DEC')
# ts = pd.Series(np.random.randn(len(rng)), index=rng)
# print(ts)
# print(ts.asfreq('M', how='start'))
# ts.asfreq('B', how='end')
#
# #案例
# rng = pd.date_range('2000-01-01', periods=12, freq='T')
# ts = pd.Series(np.arange(12), index=rng)
# print(ts)
# print(ts.resample('5min', closed='right').sum())   #每5分钟求一次总和
# ts.resample('5min', closed='right', label='right').sum()
# ts.resample('5min', closed='right',
#             label='right', loffset='-1s').sum()    #loffset 让世界往左平移1秒（-1秒）
# ts.resample('5min').ohlc()

#案例2
import matplotlib.pyplot as plt
close_px_all = pd.read_csv(r'C:\Users\Administrator\Desktop\数据\pydata-book-2nd-edition\examples\stock_px_2.csv',
                           parse_dates=True, index_col=0)
close_px = close_px_all[['AAPL', 'MSFT', 'XOM']]
print(close_px)
close_px = close_px.resample('B').ffill() #抓取周间日  ffill()如果为空 就用上一个填补
plt.figure()
close_px.AAPL.plot()
close_px.AAPL.rolling(250).mean().plot()  #.rolling 取250个数据  rolling('20D')选20天的数据
plt.figure()
appl_std250 = close_px.AAPL.rolling(250, min_periods=10).std() #第10个数字开始
appl_std250[5:12]
appl_std250.plot()
expanding_mean = appl_std250.expanding().mean()
plt.figure()
close_px.rolling(60).mean().plot(logy=True)
close_px.rolling('20D').mean()
plt.show()