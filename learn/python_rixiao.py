import pandas as pd
import pymssql
import numpy as np
from datetime import datetime
conn = pymssql.connect("192.168.8.202:1433", "sa", "123456", "jingdong_salls")
data=pd.read_sql("select * from TEMP_rixiao1",conn)
from sqlalchemy import create_engine
engine = create_engine('mssql+pymssql://sa:123456@192.168.8.202:1433/jingdong_salls',echo=True)  # 建立数据库连接
data['活动异常品']=data.大大大前日日销
data.loc[np.abs(data.大大前日日销/data.大大大前日日销-1)<0.3,'活动异常品']=data.loc[np.abs(data.大大前日日销/data.大大大前日日销-1)<0.3,'大大前日日销']
data.loc[np.abs(data.大前日日销/data.大大前日日销-1)<0.3,'活动异常品']=data.loc[np.abs(data.大前日日销/data.大大前日日销-1)<0.3,'大前日日销']
data.loc[np.abs(data.前日日销/data.大前日日销-1)<0.3,'活动异常品']=data.loc[np.abs(data.前日日销/data.大前日日销-1)<0.3,'前日日销']
data.loc[np.abs(data.八仓日销/data.前日日销-1)<0.3,'活动异常品']=data.loc[np.abs(data.八仓日销/data.前日日销-1)<0.3,'八仓日销']
data.loc[data.区域异常天数==4,'活动异常品']=data.loc[data.区域异常天数==4,'八仓日销']
data['八仓日销计算']=data.活动异常品
##data.loc[data.缺货数量.fillna(0)!=0,'八仓日销计算']=data.loc[data.缺货数量.fillna(0)!=0,'缺货数量']
##data.loc[data.新品30天.fillna(0)!=0,'八仓日销计算']=data.loc[data.新品30天.fillna(0)!=0,'新品30天']
##data.loc[data.新品60至90天.fillna(0)!=0,'八仓日销计算']=data.loc[data.新品60至90天.fillna(0)!=0,'新品60至90天']
##data.loc[data.新品30至60天.fillna(0)!=0,'八仓日销计算']=data.loc[data.新品30至60天.fillna(0)!=0,'新品30至60天']
data['全国活动异常品']=data.全国大大大前日日销
data.loc[np.abs(data.全国大大前日日销/data.全国大大大前日日销-1)<0.3,'全国活动异常品']=data.loc[np.abs(data.全国大大前日日销/data.全国大大大前日日销-1)<0.3,'全国大大前日日销']
data.loc[np.abs(data.全国大前日日销/data.全国大大前日日销-1)<0.3,'全国活动异常品']=data.loc[np.abs(data.全国大前日日销/data.全国大大前日日销-1)<0.3,'全国大前日日销']
data.loc[np.abs(data.全国前日日销/data.全国大前日日销-1)<0.3,'全国活动异常品']=data.loc[np.abs(data.全国前日日销/data.全国大前日日销-1)<0.3,'全国前日日销']
data.loc[np.abs(data.全国昨日日销/data.全国前日日销-1)<0.3,'全国活动异常品']=data.loc[np.abs(data.全国昨日日销/data.全国前日日销-1)<0.3,'全国昨日日销']
data.loc[data.全国异常天数==4,'全国活动异常品']=data.loc[data.全国异常天数==4,'全国昨日日销']
data['全国日销计算']=data.全国活动异常品
##data.loc[data.全国缺货.fillna(0)!=0,'全国日销计算']=data.loc[data.全国缺货.fillna(0)!=0,'全国缺货']
##data.loc[data.全国新品30天.fillna(0)!=0,'全国日销计算']=data.loc[data.全国新品30天.fillna(0)!=0,'全国新品30天']
##data.loc[data.全国新品60至90天.fillna(0)!=0,'全国日销计算']=data.loc[data.全国新品60至90天.fillna(0)!=0,'全国新品60至90天']
##data.loc[data.全国新品30至60天.fillna(0)!=0,'全国日销计算']=data.loc[data.全国新品30至60天.fillna(0)!=0,'全国新品30至60天']
data1=data.loc[:,['商品编号','全国昨日日销']].sort_values('全国昨日日销',ascending=False).drop_duplicates()
data1['排序']=np.arange(1,len(data1)+1)
data=pd.merge(left=data,right=data1.loc[:,['商品编号','排序']],on='商品编号',how='left')
data=data.sort_values(['全国昨日日销','商品编号','区域'],ascending=[False,True,True])
data.set_index(['排序','商品编号']).to_excel('C:\\Users\\xiaofan\\Desktop\\'+str(datetime.now().month)+str(datetime.now().day)+'日销.xlsx')
class MSSQL:
    def __init__(self,host,user,pwd,db): #类的构造函数，初始化数据库连接ip或者域名，以及用户名，密码，要连接的数据库名称
        self.host=host
        self.user=user
        self.pwd=pwd
        self.db=db
    def __GetConnect(self):  #得到数据库连接信息函数， 返回: conn.cursor()
        if not self.db:
            rasie(NameError,"没有设置数据库信息")
        self.conn=pymssql.connect(host=self.host,user=self.user,password=self.pwd,database=self.db,charset='utf8')
        cur=self.conn.cursor()  #将数据库连接信息，赋值给cur。
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    #执行查询语句,返回的是一个包含tuple的list，list的元素是记录行，tuple的元素是每行记录的字段
    def ExecQuery(self,sql):  #执行Sql语句函数，返回结果
        cur = self.__GetConnect()   #获得数据库连接信息
        cur.execute(sql)  #执行Sql语句
        resList = cur.fetchall()  #获得所有的查询结果
        #查询完毕后必须关闭连接
        self.conn.close()   #返回查询结果
        return resList
    def ExecNonQuery(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
