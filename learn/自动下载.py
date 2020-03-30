#%% post请求
import urllib.request as url
import urllib.parse as parse
import re
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
posturl='https://vcp.jd.com/'

postdatalogin=parse.urlencode(
    {
        'loginname':'shmpdzsw',
        'nloginpwd':'MPDSmanxiu2020'
    }
).encode('GBK','ignore')
req=url.Request(posturl,postdatalogin,headers)
pst=url.urlopen(req).read().decode('GBK')
print(len(pst))

#%%
url2='https://vcp.jd.com/sub_settings/site/downFile?taskId=df0df86c-bcee-4ff2-b3e9-67379064694f'

#%%
import pandas as pd
x=pd.read_csv('https://vcp.jd.com/sub_settings/site/downFile?taskId=df0df86c-bcee-4ff2-b3e9-67379064694f',index_col="商品编号", encoding='gbk', na_values='- ')
x
#%%
url.urlretrieve('https://vcp.jd.com/sub_settings/site/downFile?taskId=df0df86c-bcee-4ff2-b3e9-67379064694f.csv',r'C:\Users\xiaofan\Desktop\测试导出数.csv')
