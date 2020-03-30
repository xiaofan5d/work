import tkinter as tk
import pymssql
from tkinter import messagebox
from tkinter import filedialog
import re
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
engine = create_engine('mssql+pymssql://sa:Mp123456@192.168.8.238:1433/jinxiaocun', echo=True,
                       encoding="utf-8")  #
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
    ms=MSSQL("192.168.8.238:1433", "sa", "Mp123456", "jinxiaocun")
    back_val=ms.ExecNonQuery('''
use jinxiaocun
drop table jinxiaocun..Stock_now_bak
EXEC sp_rename 'Stock_now','Stock_now_bak'
select * into jinxiaocun..Stock_now  from jinxiaocun..Stock_initial where 1!=1
''')  #注意，这里back_val为None值。
    return back_val
delete()
# data=pd.read_sql("select * from Stock_now", engine)
root = tk.Tk()
root.title('库存汇总')
root.geometry('400x250+10+10')

def huaxialong():
    data = pd.read_sql("select * from Stock_now", engine).columns
    data1 = pd.DataFrame()
    file_path = filedialog.askopenfilenames()
    for i in file_path:
        temp = pd.read_excel(i)
        data1 = data1.append(temp)
    data1 = data1.reindex(columns=data)
    data1.到期日期 = data1.到期日期.map(lambda x: x.strftime('%Y/%m/%d'))
    data1.收货日期 = data1.loc[data1.收货日期.notnull() == True, '收货日期'].map(lambda x: x.strftime('%Y/%m/%d'))
    data1.变动日期 = data1.loc[data1.变动日期.notnull() == True, '变动日期'].map(lambda x: x.strftime('%Y/%m/%d'))
    pd.io.sql.to_sql(data1, 'stock_now', con=engine, if_exists='append', index=False)
    messagebox.showinfo(title='结果信息', message='导入成功')

def huisheng():
    data = pd.read_sql("select * from Stock_now", engine).columns
    file_path = filedialog.askopenfilename()
    temp = pd.read_excel(file_path, sheet_name='恵晟')
    temp = temp.reindex(columns=['商品代码', '条码', '商品名称', '货物状态', '生产批号', '到期日期', '数量'])
    temp['可用数量'] = temp.数量
    temp = temp.reindex(columns=data)
    temp.到期日期 = temp.到期日期.map(lambda x: x.strftime('%Y/%m/%d'))
    pd.io.sql.to_sql(temp, 'stock_now', con=engine, if_exists='append', index=False)
    messagebox.showinfo(title='结果信息', message='导入成功')

B = tk.Button(root, text="华夏龙库存", command=huaxialong)
B.pack()
B1 = tk.Button(root, text="惠晟库存", command=huisheng)
B1.pack()
root.mainloop()
