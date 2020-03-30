
import urllib.request
import re
import pandas as pd
area=pd.read_excel(r'C:\Users\xiaofan\Desktop\京东爬虫\城市地区.xlsx')
url = 'https://item.jd.com/188550.html'
class spyder:
    def __init__(self,url):
        self.url=url
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
        self.req=urllib.request.Request(self.url, headers=self.headers)
    def stock(self):
        x = 'cat: \[(.*?)\]'  # 正则表达式
        data = urllib.request.urlopen(self.req).read().decode('gbk')  # 读取jd网址
        y = re.compile(x, re.S).findall(data)[0]
        sku = re.compile('https://item.jd.com/(\d*)').findall(url)[0]  # 提取网页中的sku
        return [sku, y]
    def price(self):
        x = '"StockStateName":"(.*?)",'  # 有无货正则表达式
        data = urllib.request.urlopen(self.req).read().decode('gbk')  # 读取jd网址
        y = re.compile(x, re.S).findall(data)[0]
        x1='"op":"(\S*?)"'# 京东价正则表达式
        y1=re.compile(x1, re.S).findall(data)[0]
        x2='"p":"(\S*?)"'#前台价正则表达式
        y2 = re.compile(x2, re.S).findall(data)[0]
        return [y,y1,y2]

    def yushou(self):
        x = '"presaleEndTime":"(.*?)",'  # 预售结束时间
        data = urllib.request.urlopen(self.req).read().decode('gbk')  # 读取jd网址
        y = re.compile(x, re.S).findall(data)[0]
        x1 = '"count":(\S*?)"'  # 京东价正则表达式
        y1 = re.compile(x1, re.S).findall(data)[0]
        return [y, y1]

    def shifouyushou(self):
        x = '<strong>预售</strong>'  # 预售结束时间
        data = urllib.request.urlopen(self.req).read().decode('gbk')
        y = re.compile(x, re.S).findall(data)[0]
        return len(y)





    #%%
url = 'https://item.jd.com/188550.html'
stock=spyder(url).stock()
liebiao=[stock[0]]
for i in area.一级:
    url2='https://c0.3.cn/stock?skuId='+str(stock[0])+'&area='+str(i)+'_0_0_0&choseSuitSkuIds=&cat='+str(stock[1])
    price=spyder(url2).price()

    print(liebiao)
    liebiao.extend(price)
    #if  url首页len()大于继续爬
    if





    yushou = spyder(url2).price()

网页包含预售
调到





#%%
liebiao.append_

#%%

price




#%%
url2='https://c0.3.cn/stock?skuId=188550&area=13_0_0_0&choseSuitSkuIds=&cat=1316,16831,16840'

spyder(url2).price()

#%%
rst={'是否有货': '现货', '京东价': '49.90', '前台价': '30.90'}
pd.DataFrame(rst)

#%%
stock

#%%

https://c0.3.cn/stock?skuId=55593671974&area=2_2813_51976_0&choseSuitSkuIds=&cat=1316,1381,1396

爬取cat用来看有货无货
StockStateName 有无货,采购中
jdPrice":{"op":"34.90","m":"44.90","




#%%


url2='https://c0.3.cn/stock?skuId='+'area='+    +'_2813_51976_0&choseSuitSkuIds=&cat='+


#%%



https://c0.3.cn/stock?skuId=55593671974&area=2_2813_51976_0&choseSuitSkuIds=&cat=1316,1381,1396

爬取cat用来看有货无货
StockStateName 有无货,采购中
jdPrice":{"op":"34.90","m":"44.90","




if 初始页有预售
    过去 https: // yuding.jd.com / presaleInfo / getPresaleInfo.action?callback = jQuery5322222 & sku = 100009261520
presaleEndTime":"2019-10-31
"count":967
添加是否开启预售和结束时间和预售数量

#%%
#京东城市代码

u'''2f4
jQuery1006253([{"areaCode":"","id":52113,"name":"\u57CE\u533A"},{"areaCode":"","id":52114,"name":"\u516B\u4E00\u9547"},{"areaCode":"","id":52115,"name":"\u7EA2\u83F1\u9547"},{"areaCode":"","id":52116,"name":"\u6797\u76DB\u4E61"},{"areaCode":"","id":52117,"name":"\u6C99\u6CB3\u9547"},{"areaCode":"","id":52118,"name":"\u5341\u91CC\u6CB3\u9547"},{"areaCode":"","id":52119,"name":"\u9648\u76F8\u9547"},{"areaCode":"","id":52120,"name":"\u59DA\u5343\u6237\u5C6F\u9547"},{"areaCode":"","id":52121,"name":"\u738B\u7EB2\u5821\u4E61"},{"areaCode":"","id":52122,"name":"\u6C38\u4E50\u4E61"},{"areaCode":"","id":52123,"name":"\u5927\u6C9F\u4E61"},{"areaCode":"","id":52124,"name":"\u767D\u6E05\u5BE8\u4E61"},{"areaCode":"","id":52125,"name":"\u4F5F\u6C9F\u4E61"}])id":3635,"name":"\u8354\u6E7E\u533A"},{"areaCode":"","id":3637,"name":"\u8D8A\u79C0\u533A"},{"areaCode":"","id":36953,"name":"\u756A\u79BA\u533A"},{"areaCode":"","id":50256,"name":"\u82B1\u90FD\u533A"},{"areaCode":"","id":50258,"name":"\u767D\u4E91\u533A"},{"areaCode":"","id":50259,"name":"\u5357\u6C99\u533A"},{"areaCode":"","id":50283,"name":"\u9EC4\u57D4\u533A"},{"areaCode":"","id":50284,"name":"\u589E\u57CE\u533A"},{"areaCode":"","id":50285,"name":"\u4ECE\u5316\u533A"},{"areaCode":"","id":51091,"name":"\u5E7F\u5DDE\u5927\u5B66\u57CE"}])'''