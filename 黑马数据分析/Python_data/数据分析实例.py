from numpy.random import randn
import numpy as np
np.random.seed(123)
import os
import matplotlib.pyplot as plt
import pandas as pd

import json
path = r'C:\Users\Administrator\Desktop\数据\pydata-book-2nd-edition\datasets/bitly_usagov/example.txt'
records = [json.loads(line) for line in open(path)]  #读取每一行
# print(records)
# time_zones = [rec['tz'] for rec in records]
time_zones = [rec['tz'] for rec in records if 'tz' in rec] #如果 'tz' 在 rec中  就取出 rec['tz']
print(time_zones[:10])
def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts
#同上
from collections import defaultdict
def get_counts2(sequence):
    counts = defaultdict(int) # values will initialize to 0  ＃值将初始化为0 整数型
    for x in sequence:
        counts[x] += 1
    return counts
counts = get_counts(time_zones)

print(counts['America/New_York']) #查看这个时区个数
len(time_zones)
def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]
top_counts(counts)
from collections import Counter
counts = Counter(time_zones)
counts.most_common(10)

#pandas 处理数据
import pandas as pd
frame = pd.DataFrame(records)
print(frame.info())  #归纳信息
# print(frame['tz'][:10])
tz_counts = frame['tz'].value_counts() #统计['tz']时区各种数量
print(tz_counts[:10])
clean_tz = frame['tz'].fillna('Missing') #填补nan
clean_tz[clean_tz == ''] = 'Unknown'
tz_counts = clean_tz.value_counts()
print(tz_counts[:10])
plt.figure(figsize=(10, 4))

import seaborn as sns  #画图  Seaborn和Matplotlib是Python最强大的两个可视化库。Seaborn其默认主题让人惊讶，而Matplotlib可以通过其多个分类为用户打造专属功能。
subset = tz_counts[:10]
sns.barplot(y=subset.index, x=subset.values)
frame['a'][1]
frame['a'][50]
frame['a'][51][:50]  # long line
results = pd.Series([x.split()[0] for x in frame.a.dropna()])
results[:5]
results.value_counts()[:8]
cframe = frame[frame.a.notnull()]
cframe = cframe.copy()
cframe['os'] = np.where(cframe['a'].str.contains('Windows'),
                        'Windows', 'Not Windows')
cframe['os'][:5]
by_tz_os = cframe.groupby(['tz', 'os'])
agg_counts = by_tz_os.size().unstack().fillna(0)
agg_counts[:10]
# Use to sort in ascending order
indexer = agg_counts.sum(1).argsort()
indexer[:10]
count_subset = agg_counts.take(indexer[-10:])
count_subset
agg_counts.sum(1).nlargest(10)
plt.figure()