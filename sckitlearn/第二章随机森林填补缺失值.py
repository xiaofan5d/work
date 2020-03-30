 import numpy as np
 from sklearn.ensemble import RandomForestRegressor
 from sklearn.impute import SimpleImputer
 import pandas as pd
 import matplotlib.pyplot as plt
 from sklearn.model_selection import cross_val_score
 from sklearn.datasets import load_boston
 #%%
 dataset = load_boston()

 dataset.data.shape  # 总共506*13=6578个数据

 X_full, y_full = dataset.data, dataset.target
 n_samples = X_full.shape[0]
 n_features = X_full.shape[1]

 rng = np.random.RandomState(0)
 missing_rate = 0.5
 n_missing_samples = int(np.floor(n_samples * n_features * missing_rate))  # np.floor向下取整，返回.0格式的浮点数

 # 所有数据要随机遍布在数据集的各行各列当中，而一个缺失的数据会需要一个行索引和一个列索引 #如果能够创造一个数组，包含3289个分布在0~506中间的行索引，和3289个分布在0~13之间的列索引，那我们就可 以利用索引来为数据中的任意3289个位置赋空值 #然后我们用0，均值和随机森林来填写这些缺失值，然后查看回归的结果如何

 missing_features = rng.randint(0, n_features, n_missing_samples)
 missing_samples = rng.randint(0, n_samples, n_missing_samples)

 # missing_samples = rng.choice(dataset.data.shape[0],n_missing_samples,replace=False)

 # 我们现在采样了3289个数据，远远超过我们的样本量506，所以我们使用随机抽取的函数randint。但如果我们需要 的数据量小于我们的样本量506，那我们可以采用np.random.choice来抽样，choice会随机抽取不重复的随机数， 因此可以帮助我们让数据更加分散，确保数据不会集中在一些行中

 X_missing = X_full.copy()
 y_missing = y_full.copy()

 X_missing[missing_samples, missing_features] = np.nan

 X_missing = pd.DataFrame(X_missing)  # 转换成DataFrame是为了后续方便各种操作，numpy对矩阵的运算速度快到拯救人生，但是在索引等功能上却不如 pandas来得好用

#%%用均值天空
imp_mean=SimpleImputer(missing_values=np.nan,strategy='mean')
X_missing_mean=imp_mean.fit_transform(X_missing)
#%%
imp_0=SimpleImputer(missing_values=np.nan,strategy='constant',fill_value=0)
X_missing_0=imp_0.fit_transform(X_missing)


#%%
pd.DataFrame(X_missing_mean).isnull().sum()

#%%
X_missing_reg=X_missing.copy()
#找出数据中所有缺失值数量的排序
#%%
##返回缺失值数量的排序索引
sortindex=np.argsort(X_missing_reg.isnull().sum()).values

#%%
#创建循环并用随机森林填充
for i in sortindex:
 df = X_missing_reg
 y=df[i]
 x=pd.concat([df.loc[:,df.columns!=i],pd.DataFrame(y_full)],axis=1)
 imp_0=SimpleImputer(missing_values=np.nan,strategy='constant',fill_value=0).fit_transform(x)#空值填充0
 y_train=y.loc[y.notnull()]
 y_test = y.loc[y.isnull()]
 x_train=pd.DataFrame(imp_0).loc[y_train.index,:]
 x_test =pd.DataFrame(imp_0).loc[y_test.index,:]
 clf=RandomForestRegressor(n_estimators=100)
 clf=clf.fit(x_train,y_train)
 predict=clf.predict(x_test)
 X_missing_reg.loc[X_missing_reg.loc[:,i].isnull(), i] = predict
#%%
X_missing_reg
#%%

X_missing_reg[6]

