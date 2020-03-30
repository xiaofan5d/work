import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
#%%
data=pd.read_csv(r'D:\BaiduNetdiskDownload\菜菜的机器学习sklearn课堂\课件\01 决策树课件数据源码\data.csv')
data.info()
#$$数据工程 直接复制的
# 删除缺失值过多的列，和观察判断来说和预测的y没有关系的列
data.drop(["Cabin","Name","Ticket"],inplace=True,axis=1)
# 处理缺失值，对缺失值较多的列进行填补，有一些特征只确实一两个值，可以采取直接删除记录的方法
data["Age"] = data["Age"].fillna(data["Age"].mean())
data = data.dropna()
# 将分类变量转换为数值型变量
# 将二分类变量转换为数值型变量 #astype能够将一个pandas对象转换为某种类型，和apply(int(x))不同，astype可以将文本类转换为数字，用这 个方式可以很便捷地将二分类特征转换为0~1
data["Sex"] = (data["Sex"]== "male").astype("int")
# 将三分类变量转换为数值型变量
labels = data["Embarked"].unique().tolist()
data["Embarked"] = data["Embarked"].apply(lambda x: labels.index(x))
# 查看处理后的数据集
data.head()
#%%
X = data.iloc[:, data.columns != "Survived"]
y = data.iloc[:, data.columns == "Survived"]
from sklearn.model_selection import train_test_split
Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, y, test_size=0.3,random_state=25)
# 修正测试集和训练集的索引
for i in [Xtrain, Xtest, Ytrain, Ytest]:
    i.index = range(i.shape[0])
#查看分好的训练集和测试集
Xtrain.head()
#%% 初次带入模型
clf=DecisionTreeClassifier(random_state=25)
clf=clf.fit(Xtrain,Ytrain)
clf.score(Ytest,Ytest)
#%% 交叉验证10次
clf=DecisionTreeClassifier(random_state=25)
score=cross_val_score(clf,Xtrain,Ytrain,cv=10)
score.mean()
#%% 调参
train_sc=[]
test_sc=[]
for i in range(0,10):
    clf=DecisionTreeClassifier(random_state=25,max_depth=i+1,criterion='entropy'
                                )
    clf=clf.fit(Xtrain,Ytrain)
    score_TRain=clf.score(Xtrain,Ytrain)
    score_TEST=cross_val_score(clf,Xtest,Ytest,cv=10).mean()
    train_sc.append(score_TRain)
    test_sc.append(score_TEST)


#%% 画图
print(max(test_sc))
print(test_sc.index(max(test_sc))+1)
plt.plot(range(1,11),train_sc,label='train')
plt.plot(range(1,11),test_sc,label='test')
plt.legend()
plt.xticks(range(1,11))
plt.show()

#%% 网格搜索
#设定参数
import  numpy as  np
parameters={'criterion':('gini','entropy')
            ,'splitter':('best','random')
            ,'max_depth':[*range(1,10)]
            ,'min_samples_leaf':[*range(1,50,5)]
            ,'min_impurity_decrease':[*np.linspace(0,0.5,50)]
            }
clf=DecisionTreeClassifier(random_state=25)
gs=GridSearchCV(clf,parameters,cv=10)
gs=gs.fit(Xtrain,Ytrain)

#%%
gs.best_params_
#%%
gs.best_score_

