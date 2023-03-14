import datetime
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

# 账号
email = ''
# 密码
passwd = ''
# session
session = requests.session()


# 登陆
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
    print(msg)
    ret = ''
    if msg == '登录成功':
        # 登陆成功之后，去更新hosts.txt
        del headers['Content-Type']
        html = session.get(f'{host}/user', headers=headers).text
        soup = BeautifulSoup(html, 'lxml')
        hosts = set()
        for i in soup.find_all('h5'):
            a = i.find('a', text=re.compile('http.*'))
            if a:
                hosts.add(a.text)
        with open('hosts.txt', 'w', encoding='utf-8') as f:
            for i in hosts:
                f.write(f'{i}\n')
        # 获取登陆信息
        statistics = soup.find_all(class_='card card-statistic-2')
        for i in statistics:
            for j in i.text.split('\n'):
                if len(j) > 1:
                    a = j.replace('\n', '').replace('\r', '').replace('升级套餐', '').strip()
                    ret += a + ' '
            ret += '\n\n'
        return ret
    else:
        raise Exception(msg)


# 速鹰666签到领流量
def clockIn(host):
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
    res = session.post(url=url, headers=headers)
    json = res.json()
    print(json)
    return json


def main_handler():
    hosts = [i.strip() for i in open('hosts.txt', 'r', encoding='utf-8').readlines()]
    for host in hosts:
        try:
            print('try', host)
            lmsg = login(host)
            json = clockIn(host)
            msg = json['msg']
            print(lmsg + '今日签到 ' + msg)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(datetime.datetime.now())
    email, passwd = sys.argv[1:]
    if (not len(email)) or (not len(passwd)):
        print('email or passwd is null')
        exit()
    main_handler()
