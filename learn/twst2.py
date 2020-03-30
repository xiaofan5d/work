import urllib.request
import re
url='https://item.jd.com/188550.html'

def stock(url):
    #添加浏览器伪装headers
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
    x='cat: \[(.*?)\]' #正则表达式
    req = urllib.request.Request(url, headers=headers)
    data = urllib.request.urlopen(req).read().decode('gbk')#读取jd网址
    y=re.compile(x,re.S).findall(data)
    print(y)
#%%
stock(url)


