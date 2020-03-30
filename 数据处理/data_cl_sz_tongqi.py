import pandas as pd
import numpy as np
from datetime import datetime
import re
import time
from sqlalchemy import create_engine
engine = create_engine('mssql+pymssql://sa:Mp123456@192.168.8.238:1433/jingdong_salls', echo=True,
                       encoding="utf-8")  # 建立数据库连接
年 = 2019
月 = 3
# 这个是存放网上down下来的原始数据地址
path3 = 'D://data_jd//data_sz//'+str(年)+'//'
while True:
    日 = int(input('请输入日期,隔月数据需要修改源代码:\n'))
    if 日 == 0:
        break
    # 这个是存储转换后数据的地址
    path1 = 'D://data_jd//data_sz_cl//' + str(年) + '-' + str(月) + '//'
    MX1 = pd.read_excel(path3 + str(月) + '.' + str(日) + '商品明细' + '.xls', index_col="商品ID", na_values='-').reset_index()
    日期 = datetime(年, 月, 日)
    MX1["日期"] = 日期
    print('已完成,请输入下一个日期，按‘0’结束')
    time.sleep(0.01)
    sqldata = list(pd.read_sql("select distinct 日期 from salls_sz", engine).日期)
    if 日期.strftime('%Y-%m-%d') not in sqldata:
        pd.io.sql.to_sql(MX1, 'salls_sz', con=engine, if_exists='append', index=False)
    else:
        print('数据已导入')
engine.dispose()


#%%
MX1 = pd.read_excel(path3 + str(月) + '.' + str('9') + '商品明细' + '.xls', index_col="商品ID", na_values='-').reset_index()


