from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_wine
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
#%%
data=load_wine()
Xtrain,Xtest,Ytrain,Ytest=train_test_split(data.data,data.target,test_size=0.3)

#%%
clf1=RandomForestClassifier(random_state=0,n_estimators=100)
clf2=DecisionTreeClassifier(random_state=0)
clf1=clf1.fit(Xtrain,Ytrain)
clf2=clf2.fit(Xtrain,Ytrain)
score1=clf1.score(Xtest,Ytest)
score2=clf2.score(Xtest,Ytest)
print('随机森林%.2f:'%score1+'\n'+'决策树%.2f:'%score2)
#%%复习交叉验证
from sklearn.model_selection import cross_val_score
clf_3=RandomForestClassifier(random_state=0,n_estimators=100)
cross_val_score(clf_3,data.data,data.target,cv=5)


#%%
clf_4=RandomForestClassifier(random_state=2,n_estimators=25,oob_score=True)
clf_4=clf_4.fit(Xtrain,Ytrain)
clf_4.estimators_
#%%
clf_4.oob_score_
#%%
clf_4.feature_importances_
[*zip(data.feature_names,clf_4.feature_importances_)]
#%%
clf_4.apply(Xtest)
#%%
clf_4.predict_proba(Xtest)

#%%基分类器准确率需要大于50%,要不随机森林算法没有必要
import sklearn
sklearn.metrics.SCORERS.keys()
#%%
from sklearn.datasets import load_boston
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor

boston = load_boston()
regressor = RandomForestRegressor(n_estimators=100, random_state=0)
cross_val_score(regressor, boston.data, boston.target, cv=10 ,scoring = "neg_mean_squared_error")

