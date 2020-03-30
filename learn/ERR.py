import urllib.error as err
import urllib.request as url
try:
   x=url.urlopen('https://www.baidu.com11')
except err.URLError as e:
    print(e)
#%%
try:
    x = url.urlopen('https://www.bilibili.com/').read().decode('utf-8')
    len(x)
except err.URLError as e:
    if hasattr(e, 'code'):
        print(e.code)
    if hasattr(e, 'reason'):
        print(e.reason)

