#coding=utf-8
import math
from datetime import timedelta
from datetime import datetime
import warnings
import numpy as np
import pandas as pd
print('开始分仓,请稍后')
warnings.filterwarnings("ignore")
# 需要修改的参数
path_订单 = '3-20广州订单'
path_库存 = '广州库存0320'
订单 = pd.read_excel('D://work//曼秀雷敦//出库单发仓库//' + path_订单 + '.xlsx')
库存_源数据 = pd.read_excel(
    'D://work//曼秀雷敦//库存//{0}.xls'.format(path_库存),
    sheet_name='可用')
标卡 = pd.read_excel(
    'D://work//曼秀雷敦//最新厂价表2020.1.17副本.xlsx',
    sheet_name='SKU').fillna(0)
# 要删除
标卡.公司货号 = 标卡.公司货号.astype(str)
库存_源数据 = 库存_源数据[(库存_源数据.货物状态 == 'NR') | (
    库存_源数据.货物状态 == 'OD') | (库存_源数据.货物状态 == 'QA')]
# 新增
库存_源数据.商品代码 = 库存_源数据.商品代码.astype(str)
# 修改源代码
库存2 = pd.merge(left=库存_源数据,
               right=标卡.loc[:,
                            ['公司货号',
                             '商品编码',
                             '条码',
                             '保质期',
                             '体积',
                             '重量',
                             '发货箱规']].drop_duplicates(),
               left_on='商品代码',
               right_on='公司货号',
               how='left')
库存 = 库存2.pivot_table(
    index=[
        '商品编码',
        '条码',
        '商品代码',
        '商品名称',
        '库位',
        '生产批号',
        '到期日期',
        '发货箱规',
        '保质期',
        '体积',
        '重量',
        '货物状态'],
    values=['可用数量'],
    aggfunc='sum').reset_index()
库存需要维护 = 库存[库存.商品编码 == 0]
库存 = 库存[(库存.可用数量 != 0) & (库存.商品编码 != 0)]
库存.loc[库存.发货箱规 == 0, '发货箱规'] = 1
库存['散货数量'] = 库存.可用数量 - (库存.可用数量 / 库存.发货箱规).astype(int) * 库存.发货箱规
库存['可用数量'] = 库存.可用数量 - 库存.散货数量
库存拆分1 = 库存.drop('散货数量', axis=1)
库存拆分2 = 库存.drop('可用数量', axis=1).rename(columns={'散货数量': '可用数量'})
库存拆分1 = 库存拆分1[库存拆分1.可用数量 != 0]
库存拆分1['箱柜属性'] = '整箱'
库存拆分2 = 库存拆分2[库存拆分2.可用数量 != 0]
库存拆分2['箱柜属性'] = '散装'
库存拆分 = [库存拆分1, 库存拆分2]
库存 = pd.concat(库存拆分)
订单_剔除 = 订单
# 新增提示!提示订单中无标卡数据的商品编码
标卡_提示 = 标卡.loc[:, ['商品编码']].drop_duplicates().astype('str')
订单_提示 = 订单.loc[:, ['商品编码']].drop_duplicates().astype('str')
库存.商品编码 = 库存.商品编码.astype(np.str)
print('订单采购SKU需要维护明细:')
print(订单_提示[订单_提示.商品编码.isin(标卡_提示.商品编码) == False])
print('订单采购SKU需要维护箱规:')
print(订单_提示[订单_提示.商品编码.isin(库存.loc[库存.发货箱规 == 1].商品编码)])
# 新增去除采购数量为0的数据
订单 = 订单.loc[订单.采购数量 != 0]
订单_column = 订单.columns
订单_column1 = list(订单_column)
订单_column1.append('仓库实发数量')
订单_column2 = list(订单_column)
订单_column2.append('采购数量1')
# 20190522 发现会引用之前的数据 顾删掉此3张表
订单处理_最终1 = pd.DataFrame()
订单处理_最终2 = pd.DataFrame()
# 修改有效期格式
# 修改 删除
库存.到期日期 = pd.to_datetime(库存.到期日期)
# 修改 删除
# 已经完成编码和条码的匹配以及聚合
# 按照数量需要排序(升序)
库存处理 = pd.DataFrame()
订单.商品编码 = 订单.商品编码.astype(str)
for i in 库存.商品编码.unique():
    库存1 = 库存[(库存.商品编码 == i) & (库存.箱柜属性 == '散装')]
    # 需要修改
    库存1 = 库存1.sort_values(['箱柜属性', '到期日期'], ascending=[True, True])
    库存1['辅助列'] = np.arange(1, len(库存1) + 1)
    库存处理 = 库存处理.append(库存1)
库存处理.辅助列 = 库存处理.辅助列.astype(int).astype(str)
库存处理.商品编码 = 库存处理.商品编码.astype(str)
库存处理['辅助列1'] = 库存处理.商品编码 + 库存处理.辅助列
x = 库存处理.辅助列.astype(int).max()
y = pd.DataFrame()
for i3 in np.arange(1, x + 1):
    订单[i3] = i3
    订单[i3] = 订单[i3].astype(str)
    订单[i3] = 订单['商品编码'] + 订单[i3]
z = 1
while z <= x:
    订单 = pd.merge(left=订单,
                  right=库存处理.loc[:,
                                 ['辅助列1',
                                  '可用数量']],
                  left_on=z,
                  right_on='辅助列1',
                  how='left').fillna(0)
    订单 = 订单.drop('辅助列1', axis=1)
    订单.可用数量 = 订单.可用数量.astype(int)
    订单 = 订单.rename(columns={'可用数量': x + z})
    z = z + 1
库存修改箱柜 = 库存处理.pivot_table(
    index='商品编码',
    values='发货箱规',
    aggfunc='max').reset_index()
订单 = pd.merge(
    left=订单,
    right=库存修改箱柜,
    left_on='商品编码',
    right_on='商品编码',
    how='left')
订单['采购数量1'] = 订单['采购数量']
订单_bak = 订单.reindex(columns=订单_column2)
# 标记
订单 = 订单.drop('发货箱规', axis=1)
ix = 1
订单处理h = pd.DataFrame()
while ix <= x and len(订单) > 0:
    订单处理 = pd.DataFrame()
    for i2 in 订单.商品编码.unique():
        订单1 = 订单[订单.商品编码 == i2].sort_values('采购数量1')
        订单1['累加和'] = 订单1.采购数量1.cumsum()
        订单处理 = 订单处理.append(订单1)
    订单处理[x * 2 + ix] = 订单处理[x + ix] - 订单处理['累加和']
    订单处理.loc[订单处理[x * 2 + ix] >= 0, x * 3 + 1] = 订单处理['采购数量1']
    订单处理.loc[(订单处理[x * 2 + ix] < 0) & (订单处理.采购数量1 + 订单处理[x * 2 + ix]
                                       > 0), x * 3 + 1] = 订单处理.采购数量1 + 订单处理[x * 2 + ix]
    订单处理.loc[(订单处理[x * 2 + ix] < 0) & (订单处理.采购数量1 +
                                       订单处理[x * 2 + ix] <= 0), x * 3 + 1] = 0
    订单处理1 = 订单处理[订单处理[x * 3 + 1] >= 0]
    订单处理1.loc[订单处理1[x * 3 + 1] > 0, '调拨条码'] = 订单处理1[ix]
    订单处理h = 订单处理h.append(订单处理1)
    订单 = 订单处理[(订单处理[x * 3 + 1] == 0) | (订单处理[x * 3 + 1] - 订单处理.采购数量1 < 0)]
    订单.采购数量1 = 订单.采购数量1 - 订单[x * 3 + 1]
    ix = ix + 1
# 20190521修改
if len(订单处理h) > 0:
    订单处理_最终 = pd.merge(
        left=订单处理h,
        right=库存处理,
        left_on='调拨条码',
        right_on='辅助列1',
        how='left')
    订单处理_最终 = 订单处理_最终.reindex(
        columns=[
            '订单号',
            '分配机构',
            '仓库',
            '详细地址',
            '联系人',
            '联系方式',
            '商品编码_x',
            '条码',
            '商品名称_x',
            '采购数量',
            '采购金额',
            '库位',
            '生产批号',
            '商品代码',
            x * 3 + 1,
            '到期日期',
            '发货箱规',
            '箱数',
            '保质期',
            '体积',
            '重量'])
    订单处理_最终 = 订单处理_最终.rename(
        columns={
            '商品编码_x': '商品编码',
            '商品名称_x': '商品名称',
            x * 3 + 1: '仓库实发数量'})
    标卡1 = 库存.loc[库存.箱柜属性 == '整箱', ['商品编码', '发货箱规']].drop_duplicates()
    print('注意！！！,整箱发货对应此次发货京东码对应的箱规有个SKU箱规有多个的sku:')
    标卡1.商品编码.value_counts().reset_index(
    ).loc[标卡1.商品编码.value_counts().reset_index().商品编码 > 1]
    # 0429
    标卡1 = 标卡1.pivot_table(index='商品编码', values='发货箱规', aggfunc='min')
    订单_new2 = 订单处理_最终.loc[订单处理_最终.仓库实发数量 == 0]
    订单_new2 = 订单_new2.drop('发货箱规', axis=1)
    订单_new2 = pd.merge(left=订单_new2, right=标卡1, on='商品编码', how='left')
    订单_new2 = 订单_new2.loc[订单_new2.发货箱规 > 订单_new2.采购数量]
    订单_new2 = 订单_new2.drop_duplicates()
    print('未满一箱数据准备完毕!')
    订单处理_最终1 = 订单处理_最终.loc[订单处理_最终.仓库实发数量 != 0]
    订单处理_1 = 订单处理_最终.loc[订单处理_最终.仓库实发数量 != 0].pivot_table(
        index=['订单号', '商品编码'], values=['仓库实发数量'], aggfunc='sum').reset_index()
    print('散货分货完毕!')
    订单处理_2 = 订单_new2.loc[:, ['订单号', '商品编码', '采购数量']]
    订单处理_2.drop_duplicates(keep='first', inplace=True)
    订单处理_2 = 订单处理_2.rename(columns={'采购数量': '仓库实发数量'})
    订单处理_3 = 订单处理_1.append(订单处理_2)
    订单处理_3 = 订单处理_3.pivot_table(
        index=[
            '订单号',
            '商品编码'],
        values='仓库实发数量',
        aggfunc='sum').reset_index()
    订单_new = pd.merge(
        left=订单_bak, right=订单处理_3, left_on=[
            '商品编码', '订单号'], right_on=[
            '商品编码', '订单号'], how='left')
    # 20190523修改
    if len(订单处理_3) == 0:
        订单_new['采购数量2'] = 订单_new.采购数量1.fillna(0) - 0
    else:
        订单_new['仓库实发数量'] = 订单_new.仓库实发数量.fillna(0)
        订单_new['采购数量2'] = 订单_new.采购数量1.fillna(0) - 订单_new.仓库实发数量
# 0429 前面用的散货的箱规 这里必须重新更新箱规
    # 标记 订单_new=订单_new.drop('箱规',axis=1)
    订单_new = pd.merge(left=订单_new, right=标卡1, on='商品编码', how='left')
    订单 = 订单_new
# 再来一次
库存处理 = pd.DataFrame()
订单.商品编码 = 订单.商品编码.astype(str)
for i in 库存.商品编码.unique():
    库存1 = 库存[(库存.商品编码 == i) & (库存.箱柜属性 == '整箱')]
    # 需要修改
    库存1 = 库存1.sort_values(['箱柜属性', '到期日期'], ascending=[True, True])
    库存1['辅助列'] = np.arange(1, len(库存1) + 1)
    库存处理 = 库存处理.append(库存1)
库存处理.辅助列 = 库存处理.辅助列.astype(int).astype(str)
库存处理.商品编码 = 库存处理.商品编码.astype(str)
库存处理['辅助列1'] = 库存处理.商品编码 + 库存处理.辅助列
x = 库存处理.辅助列.astype(int).max()
y = pd.DataFrame()
for i3 in np.arange(1, x + 1):
    订单[i3] = i3
    订单[i3] = 订单[i3].astype(str)
    订单[i3] = 订单['商品编码'] + 订单[i3]
z = 1
while z <= x:
    订单 = pd.merge(left=订单,
                  right=库存处理.loc[:,
                                 ['辅助列1',
                                  '可用数量']],
                  left_on=z,
                  right_on='辅助列1',
                  how='left').fillna(0)
    订单 = 订单.drop('辅助列1', axis=1)
    订单.可用数量 = 订单.可用数量.astype(int)
    订单 = 订单.rename(columns={'可用数量': x + z})
    z = z + 1
订单.采购数量1 = 订单.采购数量2
订单.loc[订单.发货箱规 == 0, '发货箱规'] = 1
订单['采购数量1'] = (订单['采购数量1'] / 订单.发货箱规.fillna(1)).astype(int) * 订单.发货箱规.fillna(1)
订单 = 订单.drop('发货箱规', axis=1)
ix = 1
订单处理h = pd.DataFrame()
while ix <= x and len(订单) > 0:
    订单处理 = pd.DataFrame()
    for i2 in 订单.商品编码.unique():
        订单1 = 订单[订单.商品编码 == i2].sort_values('采购数量1')
        订单1['累加和'] = 订单1.采购数量1.cumsum()
        订单处理 = 订单处理.append(订单1)
    订单处理[x * 2 + ix] = 订单处理[x + ix] - 订单处理['累加和']
    订单处理.loc[订单处理[x * 2 + ix] >= 0, x * 3 + 1] = 订单处理['采购数量1']
    订单处理.loc[(订单处理[x * 2 + ix] < 0) & (订单处理.采购数量1 + 订单处理[x * 2 + ix]
                                       > 0), x * 3 + 1] = 订单处理.采购数量1 + 订单处理[x * 2 + ix]
    订单处理.loc[(订单处理[x * 2 + ix] < 0) & (订单处理.采购数量1 +
                                       订单处理[x * 2 + ix] <= 0), x * 3 + 1] = 0
    订单处理1 = 订单处理[订单处理[x * 3 + 1] >= 0]
    订单处理1.loc[订单处理1[x * 3 + 1] > 0, '调拨条码'] = 订单处理1[ix]
    订单处理h = 订单处理h.append(订单处理1)
    订单 = 订单处理[(订单处理[x * 3 + 1] == 0) | (订单处理[x * 3 + 1] - 订单处理.采购数量1 < 0)]
    订单.采购数量1 = 订单.采购数量1 - 订单[x * 3 + 1]
    ix = ix + 1
订单处理_最终 = pd.merge(
    left=订单处理h,
    right=库存处理,
    left_on='调拨条码',
    right_on='辅助列1',
    how='left')
订单处理_最终 = 订单处理_最终.reindex(
    columns=[
        '订单号',
        '分配机构',
        '仓库',
        '详细地址',
        '联系人',
        '联系方式',
        '商品编码_x',
        '条码',
        '商品名称_x',
        '采购数量',
        '采购金额',
        '库位',
        '生产批号',
        '商品代码',
        x * 3 + 1,
        '到期日期',
        '发货箱规',
        '箱数',
        '保质期',
        '体积',
        '重量'])
订单处理_最终 = 订单处理_最终.rename(
    columns={
        '商品编码_x': '商品编码',
        '商品名称_x': '商品名称',
        x * 3 + 1: '仓库实发数量'})
订单处理_最终2 = 订单处理_最终.drop_duplicates()
print('整箱分货完毕')
订单处理_最终 = 订单处理_最终1.append(订单处理_最终2)
订单处理_最终 = 订单处理_最终.drop_duplicates()
订单处理_最终.订单号 = 订单处理_最终.订单号.astype(str)
订单处理_最终['数据'] = 订单处理_最终.订单号 + 订单处理_最终.商品编码
订单处理_最终 = pd.merge(
    left=订单处理_最终,
    right=订单处理_最终.数据.value_counts().reset_index(),
    left_on='数据',
    right_on='index',
    how='left')
订单处理_最终 = 订单处理_最终.loc[(订单处理_最终.仓库实发数量 != 0) | (
    (订单处理_最终.数据_y == 1) & (订单处理_最终.仓库实发数量 == 0))]

订单处理_最终 = pd.merge(left=订单处理_最终,
                   right=标卡.loc[:,
                                ['公司货号',
                                 '茂浦采购价未税',
                                 '箱规']].drop_duplicates(),
                   left_on='商品代码',
                   right_on='公司货号',
                   how='left')
订单处理_最终.loc[订单处理_最终.箱规 == 0, '箱规'] = 1
订单处理_最终.loc[订单处理_最终.仓库实发数量 != 0, '箱数'] = 订单处理_最终.loc[订单处理_最终.仓库实发数量 !=
                                                     0, '仓库实发数量'] / (订单处理_最终.loc[订单处理_最终.仓库实发数量 != 0, '箱规'].fillna(1))
订单处理_最终.loc[订单处理_最终.仓库实发数量 != 0,
            '箱数'] = 订单处理_最终.loc[订单处理_最终.仓库实发数量 != 0,
                                '箱数'].map(lambda x: math.ceil(x))
订单处理_最终['总体积'] = 订单处理_最终.体积 * 订单处理_最终.箱数
订单处理_最终['总重量'] = 订单处理_最终.重量 * 订单处理_最终.箱数
订单处理_最终['货品总额'] = 订单处理_最终.采购金额 / 0.63 / 订单处理_最终.采购数量 * 0.56 * 订单处理_最终.仓库实发数量
订单处理_订单汇总 = 订单处理_最终.pivot_table(
    index=[
        '订单号',
        '分配机构',
        '仓库',
        '详细地址',
        '联系方式'],
    values=[
        '仓库实发数量',
        '箱数',
        '总体积',
        '货品总额',
        '总重量'],
    aggfunc='sum').reset_index()
订单处理_订单汇总['填开日期'] = datetime.today().strftime('%Y-%m-%d')
订单处理_订单汇总['客户名称'] = '上海茂浦电子商务有限公司'
订单处理_订单汇总['始发地'] = '上海'
订单处理_订单汇总['电商名称'] = '京东商城'
订单处理_订单汇总 = 订单处理_订单汇总.reindex(
    columns=[
        '填开日期',
        '客户名称',
        '始发地',
        '分配机构',
        '电商名称',
        '订单号',
        '仓库实发数量',
        '箱数',
        '货品总额',
        '总重量',
        '总体积',
        '预约状态',
        '预约日期',
        '送货时间段',
        '预约号',
        '仓库',
        '详细地址',
        '联系方式',
        '备注'])
订单处理_订单汇总 = 订单处理_订单汇总.sort_values(['分配机构', '仓库', '订单号'])
订单处理_发货明细 = 订单处理_最终.sort_values(['分配机构', '仓库', '订单号'])
订单处理_发货明细.loc[订单处理_发货明细.到期日期.notnull(),
              '有效期'] = 订单处理_发货明细.loc[订单处理_发货明细.到期日期.notnull(),
                                     '到期日期'].map(lambda x: x.strftime('%Y-%m-%d'))
订单处理_发货明细 = 订单处理_发货明细.drop('到期日期', axis=1)
# 标记
订单处理_发货明细1 = 订单处理_发货明细.reindex(
    columns=[
        '订单号',
        '分配机构',
        '仓库',
        '详细地址',
        '联系人',
        '联系方式',
        '商品编码',
        '条码',
        '茂浦采购价未税',
        '商品名称',
        '采购数量',
        '采购金额',
        '库位',
        '生产批号',
        '商品代码',
        '仓库实发数量',
        '有效期',
        '箱数',
        '箱规',
        '保质期',
        '体积',
        '重量',
        '总体积',
        '总重量'])
订单处理_发货明细 = 订单处理_发货明细.reindex(
    columns=[
        '订单号',
        '分配机构',
        '仓库',
        '详细地址',
        '联系人',
        '联系方式',
        '商品编码',
        '条码',
        '商品名称',
        '采购数量',
        '采购金额',
        '库位',
        '生产批号',
        '商品代码',
        '仓库实发数量',
        '有效期',
        '箱数',
        '箱规',
        '保质期',
        '总体积',
        '总重量'])
订单处理_发货明细.条码 = 订单处理_发货明细.条码.astype(str)
订单处理_发货明细 = 订单处理_发货明细.sort_values(['分配机构', '仓库', '订单号', '商品编码'])
订单箱数 = 订单处理_发货明细.pivot_table(
    index='订单号',
    values='箱数',
    aggfunc='sum').reset_index()
订单箱数 = 订单箱数.rename(columns={'箱数': '订单箱数'})
订单处理_发货明细 = pd.merge(left=订单处理_发货明细, right=订单箱数, on='订单号', how='left')
订单处理_发货明细1 = pd.merge(left=订单处理_发货明细1, right=订单箱数, on='订单号', how='left')
# 添加订单箱数
订单处理_发货明细 = 订单处理_发货明细.set_index(['订单号',
                                 '分配机构',
                                 '仓库',
                                 '详细地址',
                                 '联系人',
                                 '联系方式',
                                 '订单箱数',
                                 '商品编码',
                                 '商品名称',
                                 '采购数量',
                                 '采购金额',
                                 '条码',
                                 '库位',
                                 '生产批号',
                                 '商品代码'])
定义 = 订单处理_最终.保质期.fillna(0).map(lambda x: timedelta(x))
订单处理_最终['生产日期'] = (订单处理_最终.到期日期 - 定义 + 定义 / 3).map(lambda x: x.date())
订单处理_最终['是否超保'] = '否'
订单处理_最终.loc[订单处理_最终.生产日期 < datetime.now().date() + timedelta(5), '是否超保'] = '超保'
导出路径 = pd.ExcelWriter('D://work//曼秀雷敦//出库单发仓库出库明细@' + path_库存 + '(发仓库).xlsx')
订单处理_订单汇总.to_excel(导出路径, '订单汇总', index=None)
订单处理_发货明细.to_excel(导出路径, '发货明细')
订单处理_最终['生产日期'] = (订单处理_最终.到期日期 - 定义).map(lambda x: x.date())
订单处理_超保 = 订单处理_最终[(订单处理_最终.是否超保 == '超保') & (
    订单处理_最终.仓库实发数量 != 0) & (订单处理_最终.仓库实发数量.notnull())]
订单处理_最终.loc[订单处理_最终.是否超保 == '超保']
订单处理_超保['采销部门'] = '个护'
订单处理_超保明细 = 订单处理_超保.reindex(columns=['分配机构',
                                     '仓库',
                                     '采销部门',
                                     '订单号',
                                     '商品编码',
                                     '商品名称',
                                     '仓库实发数量',
                                     '保质期',
                                     '生产日期',
                                     '到期日期']).sort_values(['订单号',
                                                           '分配机构',
                                                           '仓库'])
订单处理_超保明细['到期日期'] = 订单处理_超保明细.到期日期.map(lambda x: x.strftime('%Y-%m-%d'))
print('第二次分配完毕,正在正在进行导出,请稍后...')
订单处理_超保明细.to_excel(导出路径, '超保明细', index=None)
data_out = 订单处理_发货明细1.reset_index()
data_out['标卡'] = data_out.订单号 + data_out.商品编码
data_out1 = data_out.groupby(['订单号', '商品编码', '商品名称', '订单箱数', '茂浦采购价未税', '箱规', '体积', '重量'])[
    '仓库实发数量', '箱数', '总体积', '总重量'].sum().reset_index()
data_out.仓库实发数量 = data_out.仓库实发数量.astype(np.int64).astype(str)
data_out.箱数 = data_out.箱数.fillna(0).astype(np.int64).astype(str)
data_out.生产批号 = data_out.生产批号.fillna(0).astype(str)
data_all = pd.DataFrame()
for i in data_out.标卡.unique():
    data1 = data_out.loc[data_out.标卡 == i]
    data1['生产批号cat'] = data1.生产批号.str.cat(sep=';')
    data1['库位cat'] = data1.库位.astype(str).str.cat(sep=';')
    data1['商品代码cat'] = data1.商品代码.str.cat(sep=';')
    data1['仓库实发数量cat'] = data1.仓库实发数量.str.cat(sep=';')
    data1['有效期cat'] = data1.有效期.str.cat(sep=';')
    data1['箱数cat'] = data1.箱数.str.cat(sep=';')
    data1 = data1.drop(['订单箱数',
                        '商品名称',
                        '生产批号',
                        '库位',
                        '商品代码',
                        '仓库实发数量',
                        '有效期',
                        '箱数',
                        '体积',
                        '重量',
                        '标卡',
                        '总体积',
                        '总重量',
                        '茂浦采购价未税',
                        '箱规'],
                       axis=1)
    data_all = data_all.append(data1)
data_out2 = data_all.drop('index', axis=1).drop_duplicates()
data_out3 = pd.merge(data_out2, data_out1, on=['订单号', '商品编码'], how='left')
data_out3['始发仓库'] = '华夏龙'
data_out3['下单日期'] = datetime.today()
data_out3.下单日期 = data_out3.下单日期.map(lambda x: x.strftime('%Y-%m-%d'))
data_out3.茂浦采购价未税 = data_out3.茂浦采购价未税 * 1.13
data_out3['出库折扣'] = 0.63
data_out3 = data_out3.reindex(
    columns=[
        '订单号',
        '商品代码cat',
        '商品编码',
        '条码',
        '茂浦采购价未税',
        '商品名称',
        '箱规',
        '始发仓库',
        '分配机构',
        '下单日期',
        '',
        '库位cat',
        '生产批号cat',
        '采购数量',
        '',
        '',
        '',
        '',
        '仓库实发数量cat',
        '仓库实发数量',
        '',
        '',
        '',
        '有效期cat',
        '箱数cat',
        '箱数',
        '订单箱数',
        '',
        '',
        '',
        '',
        '',
        '',
        '',
        '出库折扣',
        '',
        '',
        '',
        '体积',
        '重量',
        '总体积',
        '总重量',
        '保质期'])
data_out3.to_excel(导出路径, '出库明细', index=None)
导出路径.save()
print('已完成并导出')
input('请美化下表格并按任意键退出')
