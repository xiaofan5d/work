import pandas as pd
import numpy as np
from datetime import datetime
import re
import time
from sqlalchemy import create_engine
engine = create_engine('mssql+pymssql://sa:Mp123456@192.168.8.238:1433/jingdong_salls', echo=True,
                       encoding="utf-8")  # 建立数据库连接
年 = 2020
月 = 1
# 这个是存放网上down下来的原始数据地址
path3 = 'D://data_jd//data_sz//'+str(年)+'//'
path1 = 'D://data_jd//data_sz//'+str(年-1)+'//'
while True:
    日 = int(input('请输入日期,隔月数据需要修改源代码:\n'))
    if 日 == 0:
        break
    MX1 = pd.read_csv(path3 + str(月) + '.' + str(日) + '商品明细' + '.csv', index_col="SKU", na_values='-').reset_index()
    日期 = datetime(年, 月, 日)
    MX1["日期"] = 日期
    MX2 = pd.read_csv(path1 + str(月) + '.' + str(日) + '商品明细' + '.csv', index_col="SKU", na_values='-').reset_index()
    日期同期 = datetime(年-1, 月, 日)
    MX2["日期"] = 日期同期
    MX=MX1.append(MX2)
    MX=MX.loc[MX.店铺名称=='曼秀雷敦自营官方旗舰店']
    MX=MX.drop(['品牌','一级类目','二级类目','三级类目','店铺名称','人均浏览量','平均停留时长','成交客单价','加购转化率','时间','经营模式'],axis=1)
    MX = MX.rename(columns={'SKU': '商品ID','成交人数':'成交客户数'})
    MX.商品ID=MX.商品ID.astype(int).astype(str)
    MX.成交转化率 = MX.成交转化率.astype(float)
    print('已完成,请输入下一个日期，按‘0’结束,同期数据只需要做到20年5.31日')
    time.sleep(0.01)
    sqldata = list(pd.read_sql("select distinct 日期 from salls_sz", engine).日期)
    if 日期 not in sqldata:
        pd.io.sql.to_sql(MX, 'salls_sz', con=engine, if_exists='append', index=False)
    else:
        print('数据已导入')

        print('数据已导入')

engine.dispose()

#%%
MX.dtypes
