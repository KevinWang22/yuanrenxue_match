# -*- coding: utf-8 -*-
# @Time    : 2021-04-25 14:04
# @Author  : Kevin_Wang
# @File    : match16.py

import execjs
import requests
import time


def get_m(time_str):
    with open('match16.js', 'r', encoding='utf-8') as f:
        js_code = f.read()

    ctx = execjs.compile(js_code)
    m = ctx.call('mybtoa', time_str)

    return m


def get_ans(page_num):

    ans = 0
    headers = {
        'Host': 'match.yuanrenxue.com',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'http://match.yuanrenxue.com/match/16',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': 'sessionid=f6q5j5yc6p68v45a0heyl39e88vz4rkx',
    }

    for page in range(1, page_num+1):
        timestamp = str(int(time.time()) * 1000)
        # print(timestamp)
        m = get_m(timestamp)
        # print(m)
        url = f'http://match.yuanrenxue.com/api/match/16?page={page}&m={m}&t={timestamp}'
        # print(url)
        if page > 3:
            headers['User-Agent'] = 'yuanrenxue.project'

        res = requests.get(url=url, headers=headers)

        datas = res.json()['data']

        for data in datas:
            ans += data['value']

    print(ans)


if __name__ == '__main__':
    get_ans(5)
