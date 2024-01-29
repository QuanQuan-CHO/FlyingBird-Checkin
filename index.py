import datetime
import os
import sys
import re

import pytz
import requests


email, passwd = sys.argv[1:]
session = requests.session()
timezone = pytz.timezone('Asia/Shanghai')
host = 'https://flyingbird.pro'
print(datetime.datetime.now(timezone).strftime("%Y-%m-%d %H:%M:%S"))


def log(msg):
    print(msg)
    os.system(f'echo "{msg}" >> log')


# 1.login
res = session.post(url=f'{host}/auth/login',
                   data={'email': email, 'passwd': passwd})
message = res.json()['msg']
if message != '登录成功':
    log('login fail')
    raise Exception(message)
log('login success')

# 2.checkin
response = session.post(url=f'{host}/user/checkin')
log(response.json()['msg'])

# 3.log remain and today's network flow
html = session.get(url=f'{host}/user').text
remain_flow = (re.findall('\"Unused_Traffic\", \".+GB', html)[0]
               .replace('\"Unused_Traffic\", \"', ''))
today_flow = re.findall('今日已用: .+GB', html)[0]
log(today_flow)
log(f'剩余流量: {remain_flow}'+'\n')
