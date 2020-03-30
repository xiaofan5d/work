import pandas as pd
import pymssql
import numpy as np
from datetime import datetime
#path1='C://Users//xiaofan//Desktop//2012//关键词数据//'
##path2=r'C:\Users\xiaofan\Desktop\2012\人群包'
##path3=r'C:\Users\xiaofan\Desktop\1111'
def data(x):
    data1=pd.DataFrame()
    for i in range(1,31):
        data=pd.read_csv(x+'trades_112042195_2019-11-'+str(i).zfill(2)+'.csv')
        data['month']='2019-11-'+str(i).zfill(2)
        data1=data1.append(data)
    return data1
    #%%
x=data('C://Users//xiaofan//Desktop//1111')

#%%
for i in range(1,31):
    print(str(i).zfill(2))

#%%
s=data('C://Users//xiaofan//Desktop//2012//海投//经典海投品类列表')
def data2(x):
    data1=pd.DataFrame()
    for i in [4,5,6,9,10,11,12]:
        data=pd.read_csv(x+str(i)+'.csv')
        data['month']=str(i)+'月'
        data1=data1.append(data)
    return data1
b=data2('C://Users//xiaofan//Desktop//2012//购物触点//购物触点账户推广计划报表')
s.to_excel('C://Users//xiaofan//Desktop//2012//经典海投品类列表.xlsx',index=None)
b.to_excel('C://Users//xiaofan//Desktop//2012//购物触点账户推广计划报表.xlsx',index=None)
#%%
y.to_excel('C://Users//xiaofan//Desktop//2012//人群包.xlsx',index=None)
z.to_excel('C://Users//xiaofan//Desktop//2012//商品品类数据.xlsx',index=None)

#%%
import pandas as pd
import pymssql
import numpy as np
from datetime import datetime
path2='C://Users//xiaofan//Desktop//TEMP//'
def data(x):
    data1=pd.DataFrame()
    for i in [1,8,9,10,11,12]:
        data=pd.read_excel(x+str(i)+'.xls')
        data['month']=str(i)+'月'
        data1=data1.append(data)
    return data1
    #%%
x=data(path2)
#%%
x.to_excel('C://Users//xiaofan//Desktop//TEMP//汇总.xlsx',index=None)
#%%
import pandas as pd
import pymssql
import numpy as np
from datetime import datetime
#path1='C://Users//xiaofan//Desktop//2012//关键词数据//'
##path2=r'C:\Users\xiaofan\Desktop\2012\人群包'
##path3=r'C:\Users\xiaofan\Desktop\1111'
def data(x):
    data1=pd.DataFrame()
    for i in range(1,31):
        data=pd.read_csv(x+'trades_116845644_2019-11-'+str(i).zfill(2)+'.csv',encoding='gbk')
        data['month']='2019-11-'+str(i).zfill(2)
        data1=data1.append(data)
    return data1
#%%
##x=data('C://Users//xiaofan//Desktop//1111//').to_excel('C://Users//xiaofan//Desktop//1111//汇总.xlsx')
x=data('C://Users//xiaofan//Desktop//2222//').to_excel('C://Users//xiaofan//Desktop//2222//汇总.xlsx')

#%%
for i in range(1,31):
    print(i)
