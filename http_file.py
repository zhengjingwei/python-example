
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import json
import requests
import time
import math



url = 'https://daishu.qq.com//testWebService/api?cmd=test1002'
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
display_req = 500

index = 1

dataset = 'location.csv'
fin = open('data/{}'.format(dataset), 'r')
fout = open('incode_data/{}'.format(dataset), 'w')
ferr = open('incode_data/error-{}'.format(dataset), 'w')


for line in fin:
    line = line.strip();
    barCode = line.split(',')[0]
    x = line.split(',')[1]
    y = line.split(',')[2]
    z = line.split(',')[3]
    print('|'.join([barCode,x,y,z]))

    index += 1

    body = str({"code":barCode,"codeType":"0"})
    req = requests.post(url, data=body, headers=headers)

    responseStatus = str(req.status_code)

    # 最多重新请求5次
    while(responseStatus != '200' and rerequest < 5):
        time.sleep(0.1) # 100毫秒延时
        req = requests.post(url, data=body, headers=headers)
        responseStatus = str(req.status_code)    
        rerequest += 1
    rerequest = 0


    if responseStatus != '200':
        ferr.write(','.join([barCode, responseStatus])+ '\n')
        continue
        
    r = req.text
    rjson = json.loads(r)

    if(rjson.get('ret') == '0'): 
        print('ret 0')
        ferr.write(','.join([barCode, responseStatus])+ '\n')
        continue

    fout.write(','.join([rjson['data']['customCode'], x,y,z]) + '\n') 

