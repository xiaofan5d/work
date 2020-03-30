#%% post请求
import urllib.request as url
import urllib.parse as parse
import re
posturl='https://www.iqianyue.com/mypost'
postdata=parse.urlencode(
    {
        'name':'周其琛',
        'pass':'123456'
    }
).encode('utf-8')
req=url.Request(posturl,postdata)
pst=url.urlopen(req).read().decode('utf-8')
print(pst)

#%%
import urllib.request as url
import urllib.parse as parse
posturl='https://passport.jd.com/new/login.aspx?rs=vc&ReturnUrl=//vcp.jd.com'
postdata

loginName

#%%
x=['A','B']
hasattr(x,'A')