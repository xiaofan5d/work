import urllib.request
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
url='https://www.baidu.com/s?wd=python'
req=urllib.request.Request(url,headers=headers)
PST=urllib.request.urlopen(req).read().decode('utf-8')
len(PST)




#%% 拉取百度搜索标题
import urllib.request
import re
import pandas as pd
zhengze='''data-tools='{"title":"(.*?)","url"'''
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
suosuo='python'
url='https://www.baidu.com/s?wd='+str(suosuo)
req=urllib.request.Request(url,headers=headers)
data=urllib.request.urlopen(req).read().decode('utf-8')
x=re.compile(zhengze).findall(data)
data_end=dict(搜索内容=x)
data_end=pd.DataFrame(data_end)
data_end
#%%
data

