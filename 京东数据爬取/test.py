import urllib.request
import re
import pandas as pd
class spyder:
    def __init__(self,url):
        self.url=url
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        self.req=urllib.request.Request(self.url, headers=self.headers)
    def stock(self):
        x = 'cat: \[(.*?)\]'  # 正则表达式
        data = urllib.request.urlopen(self.req).read().decode('gbk')  # 读取jd网址
        y = re.compile(x, re.S).findall(data)[0]
        return y

        return [y]
    def price(self):
        x = '"StockStateName":"(.*?)",'  # 有无货正则表达式
        data = urllib.request.urlopen(self.req).read().decode('gbk')  # 读取jd网址
        y = re.compile(x, re.S).findall(data)[0]
        x1='"op":"(\S*?)"'# 京东价正则表达式
        y1=re.compile(x1, re.S).findall(data)[0]
        x2='"p":"(\S*?)"'#前台价正则表达式
        y2 = re.compile(x2, re.S).findall(data)[0]
        return pd.DataFrame([dict(有无货=y, 京东价=y1, 前台价=y2)])



    def yushou(self):
        x = '"presaleEndTime":"(.*?)",'  # 预售结束时间
        data = urllib.request.urlopen(self.req).read().decode('gbk')  # 读取jd网址
        y = re.compile(x, re.S).findall(data)[0]
        x1 = '"count":(\S*?)"'  # 京东价正则表达式
        y1 = re.compile(x1, re.S).findall(data)[0]
        return pd.DataFrame([dict(预售数量=y1,预售结束时间=y,是否预售='是')])

    def shifouyushou(self):
        x = '<strong>预售</strong>'  # 预售结束时间
        data = urllib.request.urlopen(self.req).read().decode('gbk')
        y = re.compile(x, re.S).findall(data)
        return len(y)

def sku(url):
    sku = re.compile('https://item.jd.com/(.*?).html').findall(url)[0]# 提取网页中的sku
    return sku
area=pd.read_excel(r'C:\Users\xiaofan\Desktop\京东爬虫\城市地区.xlsx',sheetname='地区')
data=pd.read_excel(r'C:\Users\xiaofan\Desktop\京东爬虫\城市地区.xlsx',sheetname='sku')
data_all=pd.DataFrame()
for url2 in data.网址:
    stock = spyder(url2).stock()
    for i in area.一级:
        url3 = 'https://c0.3.cn/stock?skuId=' + str(sku(url2)) + '&area=' + str(
           i) + '_0_0_0&choseSuitSkuIds=&cat=' + str(stock)
        price = spyder(url3).price()
        price['SKU'] = sku(url2)
        price['地区'] = i
        data_all=data_all.append(price)

#%%



