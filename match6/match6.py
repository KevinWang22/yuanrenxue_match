# -*- coding: utf-8 -*-
# @Time    : 2021-04-13 23:07
# @Author  : Kevin_Wang
# @File    : match6.py
import time
import execjs
import requests
from urllib.parse import urlencode


def get_m(timestamp, times):

    # data = {'timestamp': timestamp, 'times': times}
    # encrypt_url = 'http://localhost:2229/encrypt'
    #
    # res = requests.post(url=encrypt_url, data=data)
    #
    # print(res.text)

    with open('match6.js', 'r', encoding='utf-8') as f:
        js_code = f.read()

    ctx = execjs.compile(js_code)

    m = ctx.call('r', timestamp, times)

    return m


def get_ans(page_num):

    headers = {
        'Host': 'match.yuanrenxue.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://match.yuanrenxue.com/match/6',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    ans = 0

    for page in range(1, page_num+1):

        timestamp = int(time.time()) * 1000
        # print(timestamp)
        m = get_m(timestamp, 1)
        # print(m)
        q = '1-' + str(timestamp) + '|'
        # print(q)

        params = {
            'm': m,
            'q': q,
        }

        url = f'http://match.yuanrenxue.com/api/match/6?page={str(page)}&'
        # print(url + urlencode(params))

        url += urlencode(params)

        if page > 3:
            headers['User-Agent'] = 'yuanrenxue.project'

        res = requests.get(url=url, headers=headers).json()

        for value in res['data']:
            ans += value['value']

    print(ans * 24)



if __name__ == '__main__':

    get_ans(5)
    # print(get_m(1618369392000, 1))


