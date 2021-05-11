# -*- coding: utf-8 -*-
# @Time    : 2021-04-26 22:51
# @Author  : Kevin_Wang
# @File    : match9.py
from datetime import datetime
import execjs
import re
import requests
import time


session = requests.session()

session.headers = {
    'Host': 'match.yuanrenxue.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36',
    'Referer': 'http://match.yuanrenxue.com/match/9',
}


def get_enc_m(timestamp_str):

    with open('match9.js', 'r', encoding='utf-8') as f:
        js_code = f.read()

    ctx = execjs.compile(js_code)

    enc_m = ctx.call('get_m', timestamp_str)

    return enc_m


def get_expire():

    index = 'http://match.yuanrenxue.com/match/9'
    udc_url = 'http://match.yuanrenxue.com/static/match/safety/match9/udc.js'
    res = session.get(index)

    expire = re.findall(r"decrypt\(\'(\d{10})\'\)", res.text)[0]
    print(expire)
    # gmt_format = '%a, %d %b %Y %H:%M:%S GMT'
    # expire_timestamp = int(datetime.timestamp(datetime.strptime(expire, gmt_format)))
    # session.get(udc_url)

    return expire


def get_ans(page_num):

    sum = 0
    count = 0
    expire_time = get_expire()

    for page in range(1, page_num+1):
        m = get_enc_m(expire_time)
        session.cookies.set('m', m, domain='match.yuanrenxue.com')
        # print(session.cookies)
        if page > 3:
            session.headers['User-Agent'] = 'yuanrenxue.project'
        url = f'http://match.yuanrenxue.com/api/match/9?page={page}'

        res = session.get(url=url)
        print(res.json())
        for data in res.json()['data']:
            sum += data['value']
            count += 1

    return sum/count


if __name__ == '__main__':

    print(get_ans(5))


