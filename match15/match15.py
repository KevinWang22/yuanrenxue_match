# -*- coding: utf-8 -*-
# @Time    : 2021-04-24 16:30
# @Author  : Kevin_Wang
# @File    : match15.py

import time
import math
import pywasm
import random
import requests


def get_wasm():
    url = 'http://match.yuanrenxue.com/static/match/match15/main.wasm'
    headers = {
        'Referer': 'http://match.yuanrenxue.com/match/15',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
        'Cookie': 'sessionid=ah3it1h5672m69x73moc7dlufwy1krby'
    }

    resp = requests.get(url=url, headers=headers)

    with open('match15.wasm', 'wb') as f:
        f.write(resp.content)


def get_ans(page_num):

    headers = {
        'Host': 'match.yuanrenxue.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Referer': 'http://match.yuanrenxue.com/match/15',
        'Cookie': 'sessionid=ah3it1h5672m69x73moc7dlufwy1krby',
    }
    ans = 0
    get_wasm()

    for page in range(1, page_num+1):
        timestamp1 = int(int(time.time()) / 2)
        timestamp2 = int(int(time.time()) / 2 - math.floor(random.random() * 50 + 1))
        vm = pywasm.load('match15.wasm')
        m = str(vm.exec('encode', [timestamp1, timestamp2])) + '|' + str(timestamp1) + '|' + str(timestamp2)
        url = f'http://match.yuanrenxue.com/api/match/15?m={m}&page={page}'
        if page > 3:
            headers['User-Agent'] = 'yuanrenxue.project'

        res = requests.get(url=url, headers=headers)
        print(res.json())
        for data in res.json()['data']:
            ans += data['value']

    print('总和：' + str(ans))


if __name__ == '__main__':
    get_ans(5)

