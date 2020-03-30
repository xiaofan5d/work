#%% test
# -*- coding: UTF-8 -*-
print('开始分仓,请稍后')
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")
# 需要修改的参数
path_订单 = '10-15订单'
path_库存 = '库存1015'
订单 = pd.read_excel('D://work//曼秀雷敦//出库单发仓库//' + path_订单 + '.xls')
库存_源数据 = pd.read_excel('D://work//曼秀雷敦//库存//' + path_库存 + '.xlsx', sheetname='可用')

标卡 = pd.read_excel('D://work//曼秀雷敦//最新厂价表190719副本.xlsx', sheetname='SKU').fillna(0)

#%%
print(标卡)
#%%






