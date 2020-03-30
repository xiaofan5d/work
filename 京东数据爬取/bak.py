
import urllib.request
import urllib.parse
import http.cookiejar
import re
import pandas as pd
from sqlalchemy import create_engine
# %%使用最新的上柜SKU
engine = create_engine(
    'mssql+pymssql://sa:Mp123456@192.168.8.238:1433/jingdong_salls',
    echo=True,
    encoding="utf-8")  # 建立数据库连接
#%%阿帕奇数据
data=pd.read_excel(
    r'C:\Users\xiaofan\Desktop\京东爬虫\城市地区.xlsx',
    sheet_name='sku')
#%%曼秀数据
data = pd.read_sql('''
select  'https://item.jd.com/' +商品编号+'.html' as 商品链接 from(
select distinct 商品编号 from jingdong_salls..salls
where 日期=CONVERT(varchar(100), DateAdd(dd,-1,getdate()), 23)
and 状态='上柜')T
WHERE not exists(select 1 from jingdong_salls..zengpin where zengpin.京东码=t.商品编号)
                ''', engine)
# %%
data

# %%
# 定义函数
class spyder:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36'}
        self.req = urllib.request.Request(self.url, headers=self.headers)

    def title(self):
        x = r'<title>(.*?)【行情 报价 价格 评测】-京东</title>'  # 正则表达式
        data = urllib.request.urlopen(
            self.req).read().decode(
            'gbk', "ignore")  # 读取jd网址
        y = re.compile(x, re.S).findall(data)[0]
        return y

    def stock(self):
        x = r'cat: \[(.*?)\]'  # 正则表达式
        data = urllib.request.urlopen(
            self.req).read().decode(
            'gbk', "ignore")  # 读取jd网址
        y = re.compile(x, re.S).findall(data)[0]
        return y

    def venderId(self):
        x = r'venderId:(\d*?),'  # 正则表达式
        data = urllib.request.urlopen(
            self.req).read().decode(
            'gbk', "ignore")  # 读取jd网址
        y = re.compile(x, re.S).findall(data)[0]
        return y

    def price(self):
        x = '"StockStateName":"(.*?)",'  # 有无货正则表达式
        data = urllib.request.urlopen(
            self.req).read().decode(
            'gbk', "ignore")  # 读取jd网址
        y = re.compile(x, re.S).findall(data)[0]
        x1 = r'"op":"(\S*?)"'  # 京东价正则表达式
        y1 = re.compile(x1, re.S).findall(data)[0]
        x2 = r'"p":"(\S*?)"'  # 前台价正则表达式
        y2 = re.compile(x2, re.S).findall(data)[0]
        return pd.DataFrame([dict(有无货=y, 京东价=y1, 前台价=y2)])

    def cuxiao(self):
        x = r'name":"(\w*?|\w*/\w*?)","pid"'  # 有无货正则表达式
        data = urllib.request.urlopen(
            self.req, ).read().decode(
            'utf-8', "ignore")  # 读取jd网址
        y = re.compile(x, re.S).findall(data)
        x1 = r'"content":"(\S*?)"'  # 京东价正则表达式
        y1 = re.compile(x1, re.S).findall(data)

        return [*zip(y, y1)], y, y1

    def youhuiquan(self):
        x = 'name":"(.*?)","timeDesc"'  # 有无货正则表达式
        data = urllib.request.urlopen(
            self.req,).read().decode(
            'utf-8', "ignore")  # 读取jd网址
        y = re.compile(x, re.S).findall(data)
        x1 = r'"quota":(\S*?),"'  # 京东价正则表达式
        x2 = r'"discount":(\S*?),"'
        y2 = re.compile(x1, re.S).findall(data)
        y3 = re.compile(x2, re.S).findall(data)
        a = []
        for i, i1 in zip(y2, y3):
            a.append('满' + i + '减' + i1)
        return a

    def yushou(self):
        x = '"presaleEndTime":"(.*?)",'  # 预售结束时间
        data = urllib.request.urlopen(
            self.req).read().decode(
            'gbk', "ignore")  # 读取jd网址
        y = re.compile(x, re.S).findall(data)[0]
        x1 = r'"count":(\S*?)"'  # 京东价正则表达式
        y1 = re.compile(x1, re.S).findall(data)[0]
        return pd.DataFrame([dict(预售数量=y1, 预售结束时间=y, 是否预售='是')])

    def shifouyushou(self):
        x = '<strong>预售</strong>'  # 预售结束时间
        data = urllib.request.urlopen(self.req).read().decode('gbk', "ignore")
        y = re.compile(x, re.S).findall(data)
        return len(y)


def sku(url):
    sku = re.compile(
        'https://item.jd.com/(.*?).html').findall(url)[0]  # 提取网页中的sku
    return sku


area = pd.read_excel(
    r'C:\Users\xiaofan\Desktop\京东爬虫\城市地区.xlsx',
    sheet_name='地区')

# %%
# cookies
#data_cookies = {'username': '15221609153', 'password': '19891124nz',}
#postdata = urllib.parse.urlencode(data_cookies).encode('utf8')
#cjar = http.cookiejar.CookieJar()
# 使用HTTPCookieProcessor创建cookie处理器，并以其为参数构建opener对象
#cookie = urllib.request.HTTPCookieProcessor(cjar)
#opener = urllib.request.build_opener(cookie)
# 将opener安装为全局
# urllib.request.install_opener(opener)
# %% 预售信息
print('正在拉取预售信息')
yushou_all = pd.DataFrame()
for url in data.网址:
    yushouurl = 'https://yuding.jd.com/presaleInfo/getPresaleInfo.action?callback=jQuery' + \
        str(sku(url)) + '&sku=' + str(sku(url))
    if spyder(url).shifouyushou() > 0:
        yushou = spyder(yushouurl).yushou()
        yushou['SKU'] = sku(url)
        yushou_all = yushou_all.append(yushou)
        print('SKU:' + str(sku(url)) + '预售信息拉取完毕')
    else:
        print('SKU:' + str(sku(url)) + '无预售信息')
print('预售信息拉取完毕')
# %% 促销信息
print('正在拉取促销信息')
cuxiao_all = pd.DataFrame()
column = []
for url4 in data.网址:
    venderId = spyder(url4).venderId()
    stock = spyder(url4).stock()
    cuxiaourl = 'https://cd.jd.com/promotion/v2?callback=jQuery&skuId=' + \
        str(sku(url4)) + '&area=2_0_0_0&' + 'venderId=' + str(venderId) + '&cat=' + str(stock)
    all, name, name2 = spyder(cuxiaourl).cuxiao()
    temp_name = name.copy()
    temp_name.extend(['促销信息汇总', 'SKU', 'Title', '优惠券'])
    column.extend(temp_name)
    column = list(set(column))
    cuxiao_all = cuxiao_all.reindex(columns=column)
    cuxiao = pd.DataFrame(columns=column, index=[0])
    cuxiao.loc[:, '促销信息汇总'] = str(all)
    cuxiao['SKU'] = sku(url4)
    cuxiao['Title'] = spyder(url4).title()
    cuxiao['优惠券'] = str(spyder(cuxiaourl).youhuiquan())
    for i in range(0, len(name)):
        x1 = name[i]
        y1 = name2[i]
        cuxiao.loc[:, x1] = y1
    print('SKU:' + str(sku(url4)) + '促销信息拉取完毕')
    cuxiao_all = cuxiao_all.append(cuxiao)
print('促销信息拉取完毕')
# %%
cuxiao_all
# %%循环
print('正在拉取基础价格信息,有无货信息')
data_all = pd.DataFrame()
for url2 in data.网址:
    venderId = spyder(url2).venderId()
    stock = spyder(url2).stock()
    for i in area.一级:
        url3 = 'https://c0.3.cn/stock?skuId=' + str(sku(url2)) + '&area=' + str(
            i) + '_0_0_0&' + 'venderId=' + str(venderId) + '&choseSuitSkuIds=&cat=' + str(stock)
        price = spyder(url3).price()
        price['SKU'] = sku(url2)
        price['地区'] = area.loc[area.一级 == i, "属性"].values[0]
        data_all = data_all.append(price)
        print(str(area.loc[area.一级 == i, "属性"].values[0]) +
              'sku:' + str(sku(url2)) + '基础信息拉取完毕')
print('基础信息信息拉取完毕')

# %%


def min_sample(str):
    min_sample = []
    x = re.compile('总价打(.*?)折').findall(str)
    y = re.compile(r'满(\d*?)元，可减(.*?)元现金').findall(str)
    if len(x) + len(y) > 0:
        if len(x) > 0:
            x_min = float(min(x)) / 10
        else:
            x_min = 1
        if len(y) > 0:
            for i in y:
                num = (int(i[0]) - int(i[1])) / int(i[0])
                min_sample.append(num)
            y_min = min(min_sample)
        else:
            y_min = 1
        return min(x_min, y_min)
    else:
        return 1


cuxiao_all['折扣'] = cuxiao_all['促销信息汇总'].map(min_sample)
# %%导出数据
if len(yushou_all) > 0:
    data_rst = pd.merge(
        left=pd.merge(
            left=data_all,
            right=yushou_all,
            on='SKU',
            how='left'),
        right=cuxiao_all,
        on='SKU',
        how='left')

else:
    data_rst = pd.merge(left=data_all, right=cuxiao_all, on='SKU', how='left')
# data_rst=data_rst.reindex(columns=[])
data_rst.to_excel(r'C:\Users\xiaofan\Desktop\测试sku1.xlsx', index=None)

# %%
data_rst = pd.merge(left=data_all, right=cuxiao_all, on='SKU', how='left')
data_rst.to_excel(r'C:\Users\xiaofan\Desktop\测试sku1.xlsx', index=None)
