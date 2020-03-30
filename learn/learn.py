for i in  range(9,0,-1):
    for j in range(i,0,-1):
        print('%s*%s=%s'%(i,j,i*j),end=' ')
    print()
#%%
for i in  range(9,0,-1):
    print(i)

#%%
try:
    for i in range(1,10):
        print(i)
        if i==4:
            print(sdfsdf)
except Exception as err:
    print(err)


#%%
for i in range(1,10):
    try:
        print(i)
        if i==4:
            print(asdads)
    except Exception as err:
        print(err)

#%%
class MyClass:
    def __init__(self):
        print('i am first Class')
MyClass()


#%%
class Myclass1:
    def __init__(self,name,job):
        self.myname=name
        self.myjob=job
    def Print(self):
        print('My name is'+self.myname+' and my job is'+self.myjob)
x=Myclass1('周其琛','数据分析师')
#%%
x.Print()
#%%

class JIchen(Myclass1):
   def print1(self):
    print('成功')
s=JIchen('周其琛','数据分析师')
s.Print()
s.print1()

#%%
import re
string='https://detail.tmall.hk/hk/item.htm?spm=a1z10.5-b-s.w4011-14785789405.74.678a7c064KANp5&id=541928730880&rn=cd40b4b6138d01b1ad369bee2aef8f74&abbucket=15'
fd='id=(\d+?)&rn'
x=re.compile(fd).findall(string)
x
#%%
import re
string='''http://www.baidu.com  http://www.baidu.cn   http://www.baidu.net'''
fd='[a-zA-z]+://[\S]*\.com|[a-zA-z]+://[\S]*\.cn|[a-zA-z]+://[\S]*\.net'
x=re.compile(fd).findall(string)
x

#%% 简单爬虫的编写
import urllib.request as url
import pandas as pd
data=url.urlopen('https://read.douban.com/provider/all').read().decode('utf-8')
pat='class="name">(.*?)</div><div'
x=re.compile(pat).findall(data)
data_2=dict(出版社名称=x)
pd.DataFrame(data_2)


#%%

data=url.urlopen('https://read.douban.com/provider/all').geturl()
print(data)
#%%
import urllib.request as url
import pandas as pd
for i in range(1,50):
    data = url.urlopen('https://read.douban.com/provider/all', timeout=1)
    try:
        print(len(data.read().decode('utf-8')))
    except Exception as err:
        print('err')


#%%

data=url.urlopen('https://read.douban.com/provider/all').geturl()
print(data)


#%%
import urllib.request as url
import re
myserch='Python'
url=url.urlopen('https://www.baidu.com/s?ie=UTF-8&wd='+myserch)
data=url.read().decode('utf-8')
pat='''"title":"(.*?)","url"'''
x=re.compile(pat).findall(data)
x


#%%
import urllib.request as url
import re
myserch='Python'
data=url.urlopen('https://www.baidu.com/s?ie=UTF-8&wd=Python').read().decode('utf-8')
pat='title'
len(data)
#%%%
import urllib.request as url
data=url.urlopen('https://www.baidu.com/s?ie=UTF-8&wd=python')
data.geturl()


#%%
中文需要转码
url.quote('你好')
import urllib.request as url
data=url.urlopen('https://www.baidu.com/s?ie=UTF-8&wd=python').read()