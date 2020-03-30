import pandas as pd
import numpy as np
from datetime import datetime
import re
import time
from sqlalchemy import create_engine
engine = create_engine('mssql+pymssql://sa:123456@192.168.8.202:1433/jingdong_salls', echo=True,
                       encoding="utf-8")  # 建立数据库连接
年 = 2019
月 = 11
# 这个是存放网上down下来的原始数据地址
def xiugai(data):
    x='(.*)-(.*)'
    y=re.search(x,data)
    return (float(y.group(2))+float(y.group(1)))/2
path3 = 'D:\\work\\天猫旗舰店\\data\\'
riqi=input('请输入日期号:(两位文本)数')
data=pd.read_csv(path3+str(年)+'-'+str(月)+'-'+riqi+'.csv',encoding="gbk",na_values='-')
data['日期'] = datetime(年,月,int(riqi))
data=data.drop(['浏览量（仅C店）','书号(仅书籍)','7天销量', '7天销量升降', '30天销量', '30天付款人数'],axis=1)
data.loc[data.标价.str.contains('-'),'标价']=data.loc[data.标价.str.contains('-'),'标价'].map(xiugai)
data.loc[data.折扣价.str.contains('-'),'折扣价']=data.loc[data.折扣价.str.contains('-'),'折扣价'].map(xiugai)
data.标价=data.标价.astype('float')
data.折扣价=data.折扣价.astype('float')
sqldata = list(pd.read_sql("select distinct 日期 from tianmao_salls", engine).日期)
if datetime(年,月,int(riqi)) not in sqldata:
    pd.io.sql.to_sql(data, 'tianmao_salls', con=engine, if_exists='append', index=False)
else:
    print('数据已导入')
engine.dispose()





