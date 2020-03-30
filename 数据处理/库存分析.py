import pandas as pd
import numpy as np
import pandas as pd
import pymssql
import numpy as np
from datetime import datetime
from datetime import timedelta
import warnings
warnings.filterwarnings("ignore")
from sqlalchemy import create_engine
engine = create_engine('mssql+pymssql://sa:Mp123456@192.168.8.238:1433/jingdong_salls',echo=True, encoding="utf-8")
engine2 = create_engine('mssql+pymssql://sa:Mp123456@192.168.8.238:1433/Mentholatum2018',echo=True, encoding="utf-8")
税额=1.13
####读取日销,标卡以及库存数据
conn = pymssql.connect("192.168.8.238:1433", "sa", "Mp123456", "jingdong_salls")
data=pd.read_sql("select * from temp_rixiao_cl",conn)
#conn1= pymssql.connect("192.168.8.238:1433", "sa", "Mp123456", "jinxiaocun")
##库存_源数据=pd.read_sql("select * from Stock_now",conn1)
##190805改成自动读取
库存_源数据=pd.read_sql("select * from jinxiaocun..Stock_now", engine)
标卡=pd.read_sql("select * from Mentholatum2018.. sku", engine2)
库存分析移库=pd.read_excel('D://work//曼秀雷敦//库存分析移库.xlsx')
##将生产批号数据转化成小写
库存_源数据.生产批号=库存_源数据.生产批号.astype(str)
库存_源数据.生产批号=库存_源数据.生产批号.map(lambda X:X.lower())
库存_源数据.商品代码=库存_源数据.商品代码.astype(str)
##定义转换的函数
def shuxing(x):
    if x.find('sm')>=0:
        return 'SM货'
    if x.find('tc')>=0:
        return '退货'
    if x.find('退货')>=0:
        return '退货'
    if x.find('拆套')>=0:
        return '退货'
    if x.find('盘点')>=0:
        return '退货'
    if x.find('盘盈')>=0:
        return '退货'
    if x.find('星茁转库')>=0:
        return '退货'
    if x.find('调整')>=0:
        return '退货'
    else:
        return '正常商品'
def kefa(x):
    if x.find('残次')>=0:
        return '残次'
###转换数据
库存_源数据['商品属性']=库存_源数据.生产批号.map(lambda x:shuxing(x))
库存_源数据['是否可发']=库存_源数据.生产批号.map(lambda x:kefa(x))
库存_源数据['是否可发']='是'
库存_源数据.loc[库存_源数据.货物状态=='DM','是否可发']='残次'
库存_源数据.loc[库存_源数据.货物状态=='OD','是否赠品']='是'
库存_源数据.loc[库存_源数据.货物状态!='OD','是否赠品']='否'
库存_源数据.loc[(库存_源数据.生产批号=='sm-j')|(库存_源数据.生产批号=='sm1905')|(库存_源数据.生产批号=='sm-n')|(库存_源数据.生产批号=='sm-1909'),'商品属性']='正常商品'
库存2=pd.merge(left=库存_源数据,right=标卡.loc[:,['公司货号','商品编码','条码','子品牌','保质期','茂浦采购价未税']].drop_duplicates(),left_on='商品代码',right_on='公司货号',how='left').fillna(0)
库存=库存2.pivot_table(index=['货物状态','是否赠品','是否可发','条码','商品编码','商品代码','商品名称','子品牌','茂浦采购价未税','变动日期','商品属性','到期日期','收货日期','生产批号','库位','保质期'],values=['可用数量'],aggfunc='sum').reset_index()
###时间转换
库存.到期日期=pd.to_datetime(库存.到期日期)
库存.变动日期=pd.to_datetime(库存.变动日期)
库存.收货日期=pd.to_datetime(库存.收货日期)
库存['生产日期']=库存.到期日期-库存.保质期.fillna(0).map(lambda x:timedelta(x))
库存.loc[库存.保质期==730,'超保时间']=库存.生产日期+timedelta(730-487)
库存.loc[库存.保质期==1095,'超保时间']=库存.生产日期+timedelta(1095-730)
库存.loc[库存.保质期==1460,'超保时间']=库存.生产日期+timedelta(1460-974)
库存.loc[库存.保质期==1825,'超保时间']=库存.生产日期+timedelta(1825-1217)
库存.loc[库存.保质期==0,'超保时间']=库存.到期日期
库存.loc[(库存.保质期==730)&(库存.是否赠品=='否'),'临期时间']=库存.生产日期+timedelta(730-236)
库存.loc[(库存.保质期==1095)&(库存.是否赠品=='否'),'临期时间']=库存.生产日期+timedelta(1095-339)
库存.loc[(库存.保质期==1460)&(库存.是否赠品=='否'),'临期时间']=库存.生产日期+timedelta(1460-412)
库存.loc[(库存.保质期==1825)&(库存.是否赠品=='否'),'临期时间']=库存.生产日期+timedelta(1825-485)
库存.loc[(库存.保质期==730)&(库存.是否赠品=='是'),'临期时间']=库存.生产日期+timedelta(730-206)
库存.loc[(库存.保质期==1095)&(库存.是否赠品=='是'),'临期时间']=库存.生产日期+timedelta(1095-279)
库存.loc[(库存.保质期==1460)&(库存.是否赠品=='是'),'临期时间']=库存.生产日期+timedelta(1460-352)
库存.loc[(库存.保质期==1825)&(库存.是否赠品=='是'),'临期时间']=库存.生产日期+timedelta(1825-425)
库存.loc[(库存.保质期==0),'临期时间']=库存.到期日期
库存['当日时间']=datetime.today()
库存['可售时长']=(库存.到期日期-(库存.保质期*0.2).map(lambda x:max(x,90)).fillna(0).map(lambda x:timedelta(x)))-pd.to_datetime(库存.当日时间)
库存['剩余入仓天数']=pd.to_datetime(库存.超保时间)-pd.to_datetime(库存.当日时间)
库存['库龄']=pd.to_datetime(datetime.today())-库存.收货日期
库存.库龄=库存.库龄.map(lambda X:X.days)
库存.loc[(库存.库龄>=60)&(库存.库龄<90),'库龄时间段']='长库龄（60-90）'
库存.loc[(库存.库龄>=90)&(库存.库龄<180),'库龄时间段']='长库龄（90-180）'
库存.loc[(库存.库龄>=180)&(库存.库龄<360),'库龄时间段']='长库龄（180-360）'
库存.loc[(库存.库龄>=360),'库龄时间段']='长库龄（>360天）'
库存.loc[(库存.库龄<60),'库龄时间段']='库龄（60天以下）'
库存['有效期属性']='正常'
库存.loc[库存.超保时间<datetime.now().date()+timedelta(5),'有效期属性']='超保'
库存.loc[库存.临期时间<datetime.now().date(),'有效期属性']='临期'
库存.loc[库存.到期日期<datetime.now().date(),'有效期属性']='过期'
库存.loc[(库存.有效期属性=='临期'),'是否可发']='临期'
库存.loc[(库存.有效期属性=='过期'),'是否可发']='过期'
###时间转换
库存.超保时间=库存.超保时间.map(lambda x:x.strftime('%Y-%m-%d'))
库存.临期时间=库存.临期时间.map(lambda x:x.strftime('%Y-%m-%d'))
库存.到期日期=库存.到期日期.map(lambda x:x.strftime('%Y-%m-%d'))
库存.变动日期=库存.变动日期.map(lambda x:x.strftime('%Y-%m-%d'))
库存.收货日期=库存.收货日期.map(lambda x:x.strftime('%Y-%m-%d'))
库存.生产日期=库存.生产日期.map(lambda x:x.strftime('%Y-%m-%d'))
##################################################################日销处理
data_rixiao=data.loc[:,['排序','条码','商品编号','商品名称','子品牌','商品价格','茂浦采购价未税','全国日销计算','全国可订购','茂浦库存']].drop_duplicates()
库存.商品编码=库存.商品编码.astype(str)
#2019-7-9 增加SKU标卡
SKU1=data_rixiao[~data_rixiao.商品编号.isin(库存.商品编码)].drop(['排序','全国日销计算','茂浦库存','商品价格','全国可订购'],axis=1)
SKU1=SKU1.rename(columns={'商品编号':'商品编码'})
库存=库存.append(SKU1)
stock=pd.merge(left=库存,right=data_rixiao.drop(['条码','商品名称','子品牌','茂浦采购价未税'],axis=1),left_on='商品编码',right_on='商品编号',how='left').sort_values('排序').drop('商品编号',axis=1)
stock.loc[stock.排序.isnull()==True,'库存属性']='JD无运营'
stock.loc[stock.排序.isnull()==False,'库存属性']='JD运营'
stock.loc[stock.排序.isnull()==True,'排序']='JD无运营'
stock.loc[stock.全国日销计算.isnull()==True,'全国日销计算']=0
stock.loc[stock.可用数量.isnull()==True,'可用数量']=0
stock.loc[stock.库龄时间段.isnull()==True,'库龄时间段']='库龄（60天以下）'
stock.条码=stock.条码.astype(str)
stock.商品代码=stock.商品代码.astype(str)
##stock.loc[stock.条码=='0','条码']='无数据'
##stock.loc[stock.商品编码=='0','商品编码']='无数据'
stock.loc[(stock.全国日销计算.notnull()==True)&(stock.全国日销计算!=0),'周转天数']=stock.可用数量/stock.loc[(stock.全国日销计算.notnull()==True)&(stock.全国日销计算!=0),'全国日销计算']
stock.周转天数=stock.周转天数.fillna(0)
if 库存_源数据.可用数量.sum()-stock.可用数量.sum()==0:
    print('库存无差异！')
else:
    库存_源数据_检查=库存_源数据.pivot_table(index='商品代码',values='可用数量',aggfunc='sum').reset_index()
    stock_检查=stock.pivot_table(index='商品代码',values='可用数量',aggfunc='sum').reset_index()
    data_检查=pd.merge(left=stock_检查,right=库存_源数据_检查,on='商品代码',how='left')
    print('库存差异为'+str(库存_源数据.可用数量.sum()-stock.可用数量.sum())+'支,请调整SKU表!,以下为有错误的sku明细:')
    print(data_检查.loc[data_检查.可用数量_x-data_检查.可用数量_y!=0])
stock.loc[stock.周转天数==0,'周转天数属性']='不动销'
stock.loc[(stock.周转天数<=30)&(stock.周转天数>0),'周转天数属性']='周转0-30天'
stock.loc[(stock.周转天数<=60)&(stock.周转天数>30),'周转天数属性']='周转30-60天'
stock.loc[stock.周转天数>60,'周转天数属性']='滞销'
stock.loc[stock.当日时间.map(lambda X:X.day)<=30,'第几周']='第四周'
stock.loc[stock.当日时间.map(lambda X:X.day)<=21,'第几周']='第三周'
stock.loc[stock.当日时间.map(lambda X:X.day)<=14,'第几周']='第二周'
stock.loc[stock.当日时间.map(lambda X:X.day)<=7,'第几周']='第一周'
stock['年月']=stock.当日时间.map(lambda X:X.month)
print('共有'+str(len(stock.loc[stock.条码=='0','商品代码'].drop_duplicates()))+'条数据需要维护SKU表,具体明细为:')
stock.loc[stock.条码=='0',['商品代码','商品名称']].drop_duplicates()
stock_mc=stock.loc[:,['条码','商品名称']].drop_duplicates()
stock_mc['len']=stock.商品名称.str.len()
stock_mc['len2']=stock_mc['len'].groupby(stock_mc['条码']).rank(ascending=True,method='first')
stock_mc=stock_mc.loc[stock_mc.len2==1]
stock_mc.drop(['len','len2'],axis=1,inplace=True)
stock.可售时长=stock.可售时长.map(lambda X:X.days)
stock.剩余入仓天数=stock.剩余入仓天数.map(lambda X:X.days)
stock.周转天数=stock.周转天数.round(2)
yunying=pd.read_sql('''
select distinct 商品编号 from jingdong_salls..salls  
where 日期=CONVERT(varchar(100), DateAdd(dd,-1,getdate()), 23) and 状态='上柜'
''', engine)
stock.loc[stock.商品编码.isin(list(yunying.商品编号)),'库存属性']='JD运营'
stock.loc[~stock.商品编码.isin(list(yunying.商品编号)),'库存属性']='JD无运营'
#新增库位
#A库可送jD的正常品(商品属性 正常+退货 效期 正常+超保 库存属性=JD运营)
#B库临期的正常品 商品属性 正常+退货+sm 效期 临期 库存属性!=JD运营
#C库DM库+全过期
#先在定义A库 效期为正常+超保&库存属性=JD运营 定义B库 库存属性 JD不运营或者效期=临期, 在定义C库
stock.loc[(stock.库存属性=='JD运营')&((stock.有效期属性=='正常')|(stock.有效期属性=='超保'))&(stock.商品属性!='SM货'),'库位分类']='A库'
stock.loc[(stock.库存属性=='JD运营')&(stock.库位分类.isnull()==True),'库位分类']='B库'
stock.loc[stock.库存属性!='JD运营','库位分类']='B库'
stock.loc[(stock.商品代码.isin(库存分析移库.商品代码)==True)&(stock.库位分类=='B库')&((stock.有效期属性=='正常')|(stock.有效期属性=='超保'))&(stock.商品属性!='SM货'),'库位分类']='A库'
stock.loc[(stock.子品牌=='男士')|(stock.子品牌=='肌研'),'库位分类']='B库'
stock.loc[(stock.货物状态=='DM')|(stock.有效期属性=='过期'),'库位分类']='C库'
print('库位分类剩余未分配长度为:')
print(len(stock.drop('茂浦库存',axis=1).loc[(stock.年月.isnull()==False)&(stock.库位分类.isnull()==True)]))
#stock.drop('茂浦库存',axis=1).loc[stock.年月.isnull()==False].to_excel('C:\\Users\\xiaofan\\Desktop\\test1.xlsx')
print(stock.loc[stock.条码=='0',['商品代码','商品名称']].drop_duplicates())
#%%
# 建立数据库连接
if len(stock.loc[stock.条码=='0','商品代码'].drop_duplicates()) == 0 and 库存_源数据.可用数量.sum()-stock.可用数量.sum()==0:
    pd.io.sql.to_sql(stock.drop(['茂浦库存','商品价格','全国日销计算','全国可订购'],axis=1).loc[stock.年月.isnull()==False],'stock_Analysis',con=engine,if_exists='append',index=False)
    engine.dispose()
    print('\033[1;32m 正常:数据导入数据库成功 \033[0m')
else:
    print('\033[1;31m 警告:数据导入数据库失败 \033[0m')
##stock=stock.rename(columns={'可用数量':'数量'})
##stock.loc[stock.商品属性!='残次','可用数量']=stock.数量
#剔除C库
#%%
stock
#%%
stock.loc[(stock.商品属性=='正常商品')&((stock.有效期属性=='正常')|(stock.有效期属性=='超保')),'是否可发']='是'
stock.loc[stock.是否可发!='是','是否可发']='否'
#剔除C库的可用数量
stock.loc[stock.库位分类=='C库','可用数量']=0
stock_pivot1=stock.fillna(0).pivot_table(index=['排序','库存属性','子品牌','商品编码','条码','商品价格','茂浦采购价未税','全国日销计算','全国可订购','是否可发'],values='可用数量',aggfunc='sum').reset_index()
stock_pivot2=stock.fillna(0).pivot_table(index=['排序','库存属性','子品牌','商品编码','条码','商品价格','茂浦采购价未税','全国日销计算','全国可订购','是否可发'],values='可用数量',columns=['库龄时间段'],aggfunc='sum',fill_value=0).reset_index()
stock_pivot=pd.merge(left=stock_pivot1,right=stock_pivot2,on=['排序','库存属性','商品编码','条码','商品价格','茂浦采购价未税','全国日销计算','全国可订购','是否可发','子品牌']).reset_index()
stock_pivot1=pd.merge(left=stock_pivot,right=stock_mc,on='条码',how='left')
stock_pivot1['周转']=round(stock_pivot1.可用数量/stock_pivot1.全国日销计算,1)
stock_pivot1.loc[stock_pivot1.周转>45,'滞销数量']=stock_pivot1.可用数量-stock_pivot1.全国日销计算*45
stock_pivot1['滞销金额']=round(stock_pivot1.滞销数量*stock_pivot1.茂浦采购价未税*0.56*税额,0)
stock_pivot1['库龄（60天以下）金额']=round(stock_pivot1['库龄（60天以下）']*stock_pivot1.茂浦采购价未税*0.56*税额,0)
stock_pivot1['长库龄（90-180）金额']=round(stock_pivot1['长库龄（90-180）']*stock_pivot1.茂浦采购价未税*0.56*税额,0)
stock_pivot1['长库龄（180-360）金额']=round(stock_pivot1['长库龄（180-360）']*stock_pivot1.茂浦采购价未税*0.56*税额,0)
stock_pivot1['长库龄（>360天）金额']=round(stock_pivot1['长库龄（>360天）']*stock_pivot1.茂浦采购价未税*0.56*税额,0)
stock_pivot1['长库龄（60-90）金额']=round(stock_pivot1['长库龄（60-90）']*stock_pivot1.茂浦采购价未税*0.56*税额,0)
stock_pivot1=stock_pivot1.sort_values(['排序','是否可发'],ascending=[True,False])
stock_now=pd.DataFrame()
for i3 in stock_pivot1.商品编码.unique():
    data=stock_pivot1.loc[stock_pivot1.商品编码==i3]
    data['筛选']=np.arange(1,len(data)+1)
    stock_now=stock_now.append(data)
stock_now=stock_now.loc[stock_now.筛选==1]
stock_now.茂浦采购价未税=round(stock_now.茂浦采购价未税*税额,2)
stock_now=stock_now.rename(columns={'可用数量':'茂浦库存','周转':'茂浦周转','商品价格':'京东前台价','茂浦采购价未税':'零售价(13)'})
stock_now['周转（京东+茂浦）']=round((stock_now.全国可订购+stock_now.茂浦库存)/stock_now.全国日销计算,1)
stock_now['周转（京东）']=round((stock_now.全国可订购)/stock_now.全国日销计算,1)
stock_now=stock_now.reindex(columns=['排序','库存属性','条码','商品编码','商品名称','子品牌','是否可发','零售价(13)','京东前台价','全国可订购','茂浦库存','全国日销计算','周转（京东）','周转（京东+茂浦）','茂浦周转','滞销数量','滞销金额','库龄（60天以下）','库龄（60天以下）金额','长库龄（60-90）','长库龄（60-90）金额','长库龄（90-180）','长库龄（90-180）金额','长库龄（180-360）','长库龄（180-360）金额','长库龄（>360天）','长库龄（>360天）金额'])
stock_now.to_excel(r'C:\Users\xiaofan\Desktop\test8.xlsx')
print('\033[1;32m 正常:数据导入数据库成功 \033[0m')