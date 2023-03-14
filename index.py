import datetime
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

email = ''
passwd = ''
session = requests.session()


def log(msg):
    print(msg)
    os.system(f'echo "{msg}">> log')


def login(host):
    url = f'{host}/auth/login'
    params = {
        'email': email,
        'passwd': passwd,
        'code': ''
    }
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': url,
        'Referer': f'{url}/auth/login',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'X-Requested-With': 'XMLHttpRequest',
    }
    res = session.post(url=url, headers=headers, data=params, timeout=10)
    msg = res.json()['msg']
    if msg == '登录成功':
        # 登陆成功之后，更新hosts.txt
        del headers['Content-Type']
        html = session.get(f'{host}/user', headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        hosts = []
        for i in soup.find_all('h5'):
            host = i.find('a', text=re.compile('http.*'))
            if host:
                hosts.append(host.text)
        with open('hosts.txt', 'w', encoding='utf-8') as f:
            for i in hosts:
                f.write(f'{i}\n')
    else:
        raise Exception(msg)


# 速鹰666签到领流量
def checkin(host) -> str:
    url = f'{host}/user/checkin'
    headers = {
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': url,
        'Referer': f'{host}/user',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    response = session.post(url=url, headers=headers)
    return response.json()['msg']


if __name__ == '__main__':
    email, passwd = sys.argv[1:]

    hosts = [line.strip() for line in open('hosts.txt', 'r', encoding='utf-8').readlines()]
    for host in hosts:
        try:
            log(datetime.date.today())
            login(host)
            log(f'login {host}')
            log(checkin(host))
            break
        except Exception as e:
            log(e)
