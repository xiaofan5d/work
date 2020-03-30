import pymssql
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import re
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
engine = create_engine('mssql+pymssql://sa:Mp123456@192.168.8.238:1433/jingdong_salls', echo=True,
                       encoding="utf-8")
年 = 2020
月 = 3
root = tk.Tk()
root.title('My Window')
root.geometry('400x250+10+10')
def 区域(value):
    m = re.match(r'(.*?)(库存|可订购|出库销量)', value)
    if m and m.group(1):
        return m.group(1)
def 类型(value):
    m = re.match(r'(.*?)(库存|可订购|出库销量)', value)
    if m and m.group(2):
        return m.group(2)
l1 = tk.Label(root, text="年份:")
l1.pack()  #这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
sheet_text1 = tk.StringVar()
sheet1 = tk.Entry(root, textvariable = sheet_text1)
sheet_text1.set("2020")
sheet1.pack()
l3 = tk.Label(root, text="月份：")
l3.pack()  #这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
sheet_text3 = tk.StringVar()
sheet3 = tk.Entry(root, textvariable = sheet_text3)
sheet_text3.set("3")
sheet3.pack()
l2 = tk.Label(root, text="日期(号)：")
l2.pack()  #这里的side可以赋值为LEFT  RTGHT TOP  BOTTOM
sheet_text = tk.StringVar()
sheet = tk.Entry(root, textvariable = sheet_text)
sheet_text.set(" ")
sheet.pack()
def jingdongvc():
    file_path = filedialog.askopenfilename()
    日=sheet_text.get()
    年 = sheet_text1.get()
    月 = sheet_text3.get()
    MX = pd.read_csv(file_path, index_col="商品编号", encoding='gbk', na_values='- ').drop(
        "合计").drop(["全国总出库销量", "全国总库存", "总可订购"], axis=1).fillna(0).reset_index()
    MX = MX.set_index(['商品编号', '商品名称', '商品品牌', '状态', '商品价格']).stack().reset_index().rename(
        columns={'level_5': '属性', 0: '数量'})
    MX["类型"] = MX['属性'].map(类型)
    MX["区域"] = MX['属性'].map(区域)
    日期 = datetime(int(年), int(月), int(日))
    MX["日期"] = 日期
    MX = MX.pivot_table(index=['日期', '商品编号', '商品名称', '商品品牌', '状态', '商品价格', '区域'], values="数量",
                        columns="类型").reset_index()
    MX = MX.loc[(MX.出库销量 != 0) | (MX.可订购 != 0) | (MX.库存 != 0)]
    sqldata = list(pd.read_sql("select distinct 日期 from salls_apache", engine).日期)
    if 日期.strftime('%Y-%m-%d') not in sqldata:
        pd.io.sql.to_sql(MX, 'salls_apache', con=engine, if_exists='append', index=False)
        messagebox.showinfo(title='结果信息', message='导入成功')
    else:
        messagebox.showinfo(title='结果信息', message='数据已存在,无需导入')
    engine.dispose()
B = tk.Button(root, text="京东VC后台", command=jingdongvc)
B.pack()
root.mainloop()






