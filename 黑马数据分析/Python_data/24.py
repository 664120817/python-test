import pandas as pd
#显示所有列
# pd.set_option('display.max_columns', None)
#显示所有行
# pd.set_option('display.max_rows', None)
n=0
m=pd.read_html(r"https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20190101&end=20200621")
for i in m:
    n +=1
    # print(i,n)
    # i.set_index([' Date '])
    print(n)
M = pd.DataFrame(m[2])
print("m", M.values)
M.to_excel('test2.xlsx',index=False)
# m=m[0].values
# print(m)
# M=pd.DataFrame(m)# ndex=stock添加行索引 columns=date添加列索引

# # stock_ = ["fh","dh","dx1","dx2","dx3","dx4","dx5","hj","time","bz"]
# # M.reset_index(drop=True)
# print(M)
# # M=M.index(["fh","dh","dx1","dx2","dx3","dx4","dx5","hj","time","bz"])
#
# M.to_excel('test2.xlsx',index=False)