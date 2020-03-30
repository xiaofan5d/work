import pandas as pd
import pymssql
from sqlalchemy import create_engine
engine = create_engine('mssql+pymssql://sa:Mp123456@192.168.8.238:1433/Mentholatum2018',echo=True, encoding="utf-8")  # 建立数据库连接
data=pd.read_excel('D://work//曼秀雷敦//最新厂价表2020.1.17.xlsx',sheet_name='SKU').fillna(0)
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
def delete():
    ms=MSSQL("192.168.8.238:1433", "sa", "Mp123456", "Mentholatum2018")
    back_val=ms.ExecNonQuery("DELETE FROM sku")  #注意，这里back_val为None值。
    return back_val
delete()
pd.io.sql.to_sql(data,'SKU',con=engine,if_exists='append',index=False)
engine.dispose()