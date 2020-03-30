# -*- coding: utf-8 -*-
'''
---------------------------------------------------------------------
具体步骤:
1.导入库存,订单以及厂价表
2.库存需要维护厂价表(订单中有的SKU厂价表里没有)
(需要考虑码对应问题)
3.订单的sku库存无需要报错(具体用商品编码对应商品代码匹配)
4.开始QA-散货发货
5.开始QA-整箱发货
6.开始其他-散货发货
7.开始其他-整箱发货
--------------------------------------------------------------------
修改分货逻辑
1 订单拆分
（1）采购数量为0
（2）QA散货分货
（3）QA整箱分货
（4）其他散货分货
（5）其他整箱分货
2 订单以效期先入先出原则为准
订单拆分后包含效期
3 具体分货流程为排序效期 计算累加和 再计算分货数量(需要考虑货不足的情况发生)
4 重要:订单拆分过程中如果没数据需要报错或者跳过
（1）库存长度为0需要跳出进入下一个
（2）每次订单长度为0需要跳出进入下一个

P.S
开发gui界面
箱规原则上先筛选目前有的库存的箱规 再以min箱规为准,无数据的箱规数据改为1,
并报错(某某sku无箱规,默认填为1)

'''
from tkinter import filedialog
from tkinter import messagebox
import warnings
import Outbound_order as oo
import pandas as pd
import pymssql
conn = pymssql.connect(
    "192.168.8.238:1433",
    "sa",
    "Mp123456",
    "Mentholatum2018")
warnings.filterwarnings("ignore")
#########################################################读取数据#############
print('\033[1;32m 请导入库存 \033[0m')
messagebox.showinfo(title='导入数据', message='请导入库存数据')
stock_path = filedialog.askopenfilename()
print('\033[1;32m 请导入订单 \033[0m')
messagebox.showinfo(title='导入数据', message='请导入订单数据')
Order_path = filedialog.askopenfilename()
Order = pd.read_excel(Order_path)
stock = pd.read_excel(stock_path,
                      sheet_name='可用').drop('箱规', axis=1)
sku = pd.read_sql("select * from sku", conn).fillna(0)
messagebox.showinfo(title='结果信息', message='导入成功')
path_to_excel = stock_path.replace('.xlsx', '').replace('.xls', '')
############################################################修改格式##########
stock.商品代码 = stock.商品代码.astype(str)
Order.商品编码 = Order.商品编码.astype(str)
sku.公司货号 = sku.公司货号.astype(str)
stock.到期日期 = pd.to_datetime(stock.到期日期)
Order_column = list(Order.columns)
Order_column.extend(['采购数量1', '箱规'])
# 判断是否订单中的SKU厂价表中已维护
oo.isin_sku(Order, sku)
# 处理库存(散货以及整箱)
stock = oo.stock_cl(stock, sku, Order)
# 处理订单(搞上箱规)(以及判断箱规是否合理)
Order = oo.Order_cl(stock, Order, sku)
# 分数据(0的数据需要修改)
Order['采购数量1'] = Order['采购数量']
Order_QA_sanhuo = Order
stock_QA_sanhuo = stock.loc[(stock.货物状态 == 'QA') & (stock.箱规属性 == '散装')]
stock_NR_sanhuo = stock.loc[(stock.货物状态 != 'QA') & (stock.箱规属性 == '散装')]
stock_QA_zhengxiang = stock.loc[(stock.货物状态 == 'QA') & (stock.箱规属性 == '整箱')]
stock_NR_zhengxiang = stock.loc[(stock.货物状态 != 'QA') & (stock.箱规属性 == '整箱')]
if len(stock_QA_sanhuo) > 0:
    Outbound_order_QA_sanhuo, Order_NR_sanhuo = oo.stock_cl_paixu(
        stock_QA_sanhuo, Order_QA_sanhuo, Order_column)
else:
    print('\033[1;31m 提示:QA散货跳过 \033[0m')
    Outbound_order_QA_sanhuo = pd.DataFrame()
    Order_NR_sanhuo = Order_QA_sanhuo
if len(stock_NR_sanhuo) > 0:
    Outbound_order_NR_sanhuo, Order_QA_zhengxiang = oo.stock_cl_paixu(
        stock_NR_sanhuo, Order_NR_sanhuo, Order_column)
else:
    print('\033[1;31m 提示:NR散货跳过 \033[0m')
    Outbound_order_NR_sanhuo = pd.DataFrame()
    Order_QA_zhengxiang = Order_NR_sanhuo
if len(stock_QA_zhengxiang) > 0:
    Outbound_order_QA_zhengxiang, Order_NR_zhengxiang = oo.stock_cl_paixu(
        stock_QA_zhengxiang, Order_QA_zhengxiang, Order_column, method='zhengxiang')
else:
    print('\033[1;31m 提示:QA整箱跳过 \033[0m')
    Outbound_order_QA_zhengxiang = pd.DataFrame()
    Order_NR_zhengxiang = Order_QA_zhengxiang
Outbound_order_NR_zhengxiang, Order_all = oo.stock_cl_paixu(
    stock_NR_zhengxiang, Order_NR_zhengxiang, Order_column, method='zhengxiang')
data = Outbound_order_QA_sanhuo.append(Outbound_order_QA_zhengxiang).append(
    Outbound_order_NR_sanhuo).append(Outbound_order_NR_zhengxiang)
print('\033[1;32m 正常:分货完成 \033[0m')
oo.export_data(data, path_to_excel, Order.采购数量.sum(), sku)
messagebox.showinfo(title='结果信息', message='导出成功')
