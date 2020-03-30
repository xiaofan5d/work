import urllib.request as url
import re
X=url.urlopen('https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=13723192103&spuId=286980694&sellerId=725677994&groupId&_ksTS=1571914346572_228&callback=jsonp229').read().decode('UTF-8')
x=re.compile('11953').findall(X)
x
#%%
import urllib.request
headers={'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}
url='https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=13723192103&spuId=286980694&sellerId=725677994&groupId&_ksTS=1571914346572_228&callback=jsonp229'
req=urllib.request.Request(url,headers=headers)
PST=urllib.request.urlopen(req).read().decode('utf-8')
len(PST)


#%%
try:
    x = url.urlopen('https://dsr-rate.tmall.com/list_dsr_info.htm?itemId=13723192103&spuId=286980694&sellerId=725677994&groupId&_ksTS=1571914346572_228&callback=jsonp229').read().decode('utf-8')
    len(x)
except err.URLError as e:
    if hasattr(e, 'code'):
        print(e.code)
    if hasattr(e, 'reason'):
        print(e.reason)


