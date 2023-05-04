import datetime
import os
import re
import sys
import pytz

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
    }
    res = session.post(url=url, data=params, timeout=10)
    msg = res.json()['msg']
    if msg == '登录成功':
        # 登陆成功之后，更新hosts.txt
        html = session.get(f'{host}/user').text
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


def checkin(host) -> str:
    url = f'{host}/user/checkin'
    response = session.post(url=url)
    return response.json()['msg']


if __name__ == '__main__':
    email, passwd = sys.argv[1:]

    hosts = [line.strip() for line in open('hosts.txt', 'r', encoding='utf-8').readlines()]
    for host in hosts:
        try:
            log(datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S"))
            login(host)
            log(f'login {host}')
            log(checkin(host)+'\n')
            return
        except Exception as e:
            continue
    log("服务器炸了")
