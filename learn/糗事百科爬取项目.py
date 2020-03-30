#爬取糗事百科的前10页的笑话
import urllib.request
import re
import pandas as pd
url='http://www.lovehhy.net/Joke/Detail/QSBK/'
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
h=pd.DataFrame()
for i in range(1,11):
    url_new=url+str(i)
    req=urllib.request.Request(url_new,headers=headers)
    data=urllib.request.urlopen(req).read().decode('gb2312',"ignore")
    len(data)
    target='target="_blank">(.*?)</a></h3><div'
    test='</a></h3><div id="endtext">　　(.*?)<br /><br /><br /></div>'
    x=re.compile(target).findall(data)
    y=re.compile(test,re.S).findall(data)
    z=dict(标题=x,内容=y)
    z=pd.DataFrame(z)
    h=h.append(z)
def sub(x):
    data=re.sub('<br />　　','', x)
    return data
h.内容=h.内容.map(sub)
h.to_csv('C:\\Users\\xiaofan\\Desktop\\xiaohua.csv',encoding='gb2312')



#%%
def sub(x):
    data=re.sub('<br />　　','', x)
    return data
z=h.内容.map(sub)
z

#%%
import  pandas as pd
data=pd.read_excel(r'C:\Users\xiaofan\Desktop\新建 Microsoft Excel 工作表.xlsx',ecodeing='gbk')
data
#%%
def sub(x):
    data=re.sub(str(x.code),str(x.name),x.forluma)
    return data
#%%
data
#%%
def sub(x):
    str(x.name)+str(x.name)
    return data
#%%
x=data.apply(sub,axis=1)
x

#%%
from sklearn.feature_selection import VarianceThreshold
def var():
    var = VarianceThreshold(0.2)
    data = var.fit_transform([[0, 2, 0, 3], [0, 1, 4, 3], [0, 1, 1, 3]])
    print(data)
    return None


var()
#%%
[[0, 2, 0, 3], [0, 1, 4, 3], [0, 1, 1, 3]]


#%%
import numpy as np

np.var((2,1,1))

#%%
x=(1,2)
x[1]
