from sklearn.model_selection import cross_val_score
from sklearn.datasets import load_boston
from sklearn.tree import DecisionTreeRegressor
data=load_boston()
#%%输出评分
rer=DecisionTreeRegressor(random_state=0)
cross_val_score(rer,data.data,data.target,cv=10,
                scoring='neg_mean_squared_error'
                )



#%%


#%%
data.data.shape

