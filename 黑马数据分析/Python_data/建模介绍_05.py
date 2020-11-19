import pandas as pd
import numpy as np
# data = pd.DataFrame({
#     'x0': [1, 2, 3, 4, 5],
#     'x1': [0.01, -0.01, 0.25, -4.1, 0.],
#     'y': [-1.5, 0., 3.6, 1.3, -2.]})
#
# df2 = pd.DataFrame(data.values, columns=['one', 'two', 'three'])
# model_cols = ['x0', 'x1']
# data.loc[:, model_cols].values
# data['category'] = pd.Categorical(['a', 'b', 'a', 'a', 'b'],
#                                   categories=['a', 'b'])
# print(data)
# dummies = pd.get_dummies(data.category, prefix='category') #c =pd.get_dummies(data)   数字列自动提前，字符列离散化
# print(dummies)
# data_with_dummies = data.drop('category', axis=1).join(dummies)
# print(data_with_dummies)

#sklearn 建模
train = pd.read_csv(r'C:\Users\Administrator\Desktop\数据\pydata-book-2nd-edition\datasets/titanic/train.csv')
test = pd.read_csv(r'C:\Users\Administrator\Desktop\数据\pydata-book-2nd-edition\datasets/titanic/test.csv')
print(train[:4])
print(train.isnull().sum())  #查看每列 nan值数量
print(test.isnull().sum())   #查看每列 nan值数量
impute_value = train['Age'].median()   #median()计算 中位数
train['Age'] = train['Age'].fillna(impute_value)  #中位数填补nan
test['Age'] = test['Age'].fillna(impute_value)   #中位数填补nan
train['IsFemale'] = (train['Sex'] == 'female').astype(int) #train['Sex'] == 'female'等于女性 转为整数型   然后添加这列
test['IsFemale'] = (test['Sex'] == 'female').astype(int)
predictors = ['Pclass', 'IsFemale', 'Age']   #取出 仓，是否女，年龄  这三列
X_train = train[predictors].values
X_test = test[predictors].values
y_train = train['Survived'].values  #取出标准答案
print("X_train:",X_train[:5])
print("y_train:",y_train[:5]) #训练值

from sklearn.linear_model import LogisticRegression
model = LogisticRegression() #建模
model.fit(X_train, y_train) #模型进行训练
y_predict = model.predict(X_test)  #测试值对比，
print("y_predict:",y_predict[:10])
# (y_true == y_predict).mean()   #y_true用真实答案对比

from sklearn.linear_model import LogisticRegressionCV
model_cv = LogisticRegressionCV(10)
model_cv.fit(X_train, y_train)
from sklearn.model_selection import cross_val_score
model = LogisticRegression(C=10)
scores = cross_val_score(model, X_train, y_train, cv=4)  # 4 代表取4个准确率
print(scores)