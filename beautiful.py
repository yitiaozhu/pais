# coding: utf-8
# @author wang

import MySQLdb
import requests
import json
import time
import sys
import re
from pandas.io.json import json_normalize
import pandas as pd


reload(sys)
sys.setdefaultencoding('utf-8')


def parse(html):
    fp = open('1.html', 'w')
    fp.write(html)
    fp.close()
    print html


def utf(keyword):
    keyword = keyword.encode('utf-8')
    return keyword


headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN, zh; q=0.8',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Host': 'www.lagou.com',
           'Referer': 'None',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36 Core/1.47.933.400 QQBrowser/9.4.8699.400',
           'X-Requester-With': 'XMLHttpRequest'
           }
# 获取网页
url = 'http://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false'
pqyload = {'pn': '1', 'kd': '数据分析师'}
data = requests.post(url, params=pqyload)

# 获取json结果
jsondata = data.json()
result = jsondata['content']['positionResult']['result']

#转化为dataframe
result = json_normalize(result)

p_id = pd.DataFrame()
bz = pd.DataFrame()

for i in list(range(len(result))):
    result_i = result.loc[i]
    business_zone = result_i.loc['businessZones']
    business_zone = pd.Series(business_zone)
    bz[i] = business_zone

    position_id = result_i.loc['positionId']
    position_id = pd.Series(position_id)
    p_id[i] = position_id
    time.sleep(0.1)

df = p_id.append(bz)
df = df.T
result.to_sql()
#df.to_csv('C:\Users\Administrator\Desktop\zones.csv')
#result.to_csv('C:\Users\Administrator\Desktop\la.csv')

'''
for each in result:
    print each['city'], each['companyShortName'], each['financeStage'], each['industryField']
    print each['education'], each['jobNature']
    print each['positionName'], each['salary'], '\n'
'''