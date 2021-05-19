# -*- coding: utf-8 -*-
# @Time    : 2021-05-17 23:40
# @Author  : Kevin_Wang
# @File    : match18.py

import execjs
import requests
import time
from random import randint


session = requests.session()

session.headers = {
        'Host': 'match.yuanrenxue.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
        'Referer': 'http://match.yuanrenxue.com/match/18',
    }

session.cookies.set('sessionid', 'm1likb0iptgvnzxm4dzulojicwf2e3is',)


def get_ans(page_num):

    ans = 0
    for page in range(1, page_num+1):
        if page > 3:
            session.headers['User-Agent'] = 'yuanrenxue.project'

        timestamp = int(time.time())
        # print(timestamp)
        mouses = []
        for _ in range(3):
            mouses.append(f'{randint(500, 600)}m{randint(500, 600)}')
        mouses.append(f'{randint(500, 600)}d{randint(500,600)}')
        mouses.append(f'{randint(500, 600)}u{randint(500, 600)}')
        # print(mouses)
        ori_text = str(page) + '|' + ','.join(mouses)
        # print(ori_text)
        str_timestamp = format(timestamp, 'x') * 2
        # print(str_timestamp)
        with open('match18.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
        ctx = execjs.compile(js_code)
        enc_v = ctx.call('get_v', ori_text, str_timestamp)

        # print(enc_v)
        url = f'http://match.yuanrenxue.com/match/18data?page={page}&t={timestamp}&v={enc_v}'
        # print(url)
        resp = session.get(url).json()
        for data in resp['data']:
            ans += data['value']

        print(ans)


if __name__ == '__main__':

    get_ans(5)
