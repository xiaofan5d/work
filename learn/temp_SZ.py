import pandas as pd
import numpy as np
from datetime import datetime
import re
import time
from sqlalchemy import create_engine


年 = 2019
月 = 11
# 这个是存放网上down下来的原始数据地址
path3 = 'D://data_jd//data_sz//2019//'
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

    # input("请退出……")
    path2 = 'D://data_jd//data_sz_cl//' + str(年) + '-' + str(月) + '//'
    MX2 = pd.read_excel(path3 + '' + str(月) + '.' + str(日) + '流量来源' + '.xls', index_col="一级来源",
                        na_values='-').reset_index()
    日期 = datetime(年, 月, 日)
    MX2["日期"] = 日期
    print('已完成,请输入下一个日期，按‘0’结束')
    time.sleep(0.01)
    MX2.columns = MX2.columns.str.replace('.', '')
    MX2.columns = MX2.columns.str.replace('_', '')
    MX2.columns = MX2.columns.str.replace('（', '')
    MX2.columns = MX2.columns.str.replace('）', '')
    MX2.columns = MX2.columns.str.replace('(', '')
    MX2.columns = MX2.columns.str.replace(')', '')
    MX2 = MX2.reindex(columns=MX2.columns[~MX2.columns.str.contains('[0-9]')])


    导出路径 = pd.ExcelWriter(path1 + str(月) + '-' + str(日) + '.xlsx')
    MX1.to_excel(导出路径, 'MX', index=False)
    MX2.to_excel(导出路径, 'MX2', index=False)
    导出路径.save()
