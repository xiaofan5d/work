from sklearn import tree
from sklearn.datasets import  load_wine
from sklearn.model_selection   import train_test_split
wine=load_wine()
wine
#%%
import pandas as pd
data=pd.DataFrame(wine.data,columns=wine.feature_names)
data


#%%
data=pd.concat([data,pd.DataFrame(wine.target,columns=['label'])],axis=1)



#%%
x_train,x_test,y_train,y_test=train_test_split(wine.data,wine.target,test_size=0.3,random_state=0)
#%%
clf=tree.DecisionTreeClassifier(criterion='gini',random_state=0)
clf.fit(x_train,y_train)
clf.score(x_test,y_test)

#%%
import graphviz
data_1=tree.export_graphviz(clf
                     ,feature_names=wine.feature_names
                     ,class_names=wine.target_names
                     ,filled=True
                     ,rounded=True
                     )
graphviz=graphviz.Source(data_1)
graphviz



#%%
clf.feature_importances_ ##属性重要性(gini或者信息熵)

[*zip(wine.feature_names,clf.feature_importances_)]



#%%
import matplotlib.pyplot as plot
x=[]
for i in range(10):
    clf=tree.DecisionTreeClassifier(
                                    max_depth=i+1
                                    ,splitter='random'
                                    ,random_state=30
                                    ,criterion='entropy'
                                        )
    clf.fit(x_train,y_train)
    score=clf.score(x_test,y_test)
    x.append(score)
print (x)

#%%
plot.plot(range(1,11),x,label='max_depth')
plot.show()
#%%
reshape(1，-1)
