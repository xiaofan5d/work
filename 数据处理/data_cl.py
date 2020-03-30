import pandas as pd
import numpy as np
from datetime import datetime
import re
import time
from sqlalchemy import create_engine
engine = create_engine('mssql+pymssql://sa:Mp123456@192.168.8.238:1433/jingdong_salls', echo=True,
                       encoding="utf-8")  # 建立数据库连接
年 = 2020
月 = 3
# 这个是存放网上down下来的原始数据地址
path3 = 'D://data_jd//data//'+str(年)+'//'
def 区域(value):
    m = re.match(r'(.*?)(库存|可订购|出库销量)', value)
    if m and m.group(1):
        return m.group(1)
def 类型(value):
    m = re.match(r'(.*?)(库存|可订购|出库销量)', value)
    if m and m.group(2):
        return m.group(2)
while True:
    日 = int(input('请输入日期,隔月数据需要修改源代码:\n'))
    if 日 == 0:
        break
    # 这个是存储转换后数据的地址
    path1 = 'D://data_jd//data_cl//' + str(年) + '-' + str(月) + '//'
    MX = pd.read_csv(path3 + str(月) + '-' + str(日) + '.csv', index_col="商品编号", encoding='gbk', na_values='- ').drop(
        "合计").drop(["全国总出库销量", "全国总库存", "总可订购"], axis=1).fillna(0).reset_index()
    MX = MX.set_index(['商品编号', '商品名称', '商品品牌', '状态', '商品价格']).stack().reset_index().rename(
        columns={'level_5': '属性', 0: '数量'})
    MX["类型"] = MX['属性'].map(类型)
    MX["区域"] = MX['属性'].map(区域)
    日期 = datetime(年, 月, 日)
    MX["日期"] = 日期
    MX = MX.pivot_table(index=['日期', '商品编号', '商品名称', '商品品牌', '状态', '商品价格', '区域'], values="数量",
                        columns="类型").reset_index()
    MX = MX.loc[(MX.出库销量 != 0) | (MX.可订购 != 0) | (MX.库存 != 0)]
    导出路径 = pd.ExcelWriter(path1 + str(月) + '-' + str(日) + '.xlsx')
    MX.to_excel(导出路径, 'MX', index=False)
    导出路径.save()
    print('已完成,请输入下一个日期，按‘0’结束')
    time.sleep(0.01)
    sqldata = list(pd.read_sql("select distinct 日期 from salls", engine).日期)
    if 日期.strftime('%Y-%m-%d') not in sqldata:
        pd.io.sql.to_sql(MX, 'salls', con=engine, if_exists='append', index=False)
    else:
        print('数据已导入')
# input("请退出……")
engine.dispose()


