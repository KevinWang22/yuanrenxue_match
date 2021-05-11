# -*- coding: utf-8 -*-
# @Time    : 2021-04-07 17:18
# @Author  : Kevin_Wang
# @File    : match2.py

import time
import requests


def get_m(timestamp):

    res = requests.post(url='http://localhost:2229/encrypt', data={'timestamp': timestamp})
    m = res.text

    return m


def get_ans(page_num):

    headers = {
        'Host': 'match.yuanrenxue.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.96 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    ans = 0

    timestamp = int(time.time()) * 1000
    m = get_m(timestamp)
    headers['Cookie'] = "m=" + m

    for page in range(1, page_num+1):

        if page > 3:
            headers['User-Agent'] = 'yuanrenxue.project'
        url = f'http://match.yuanrenxue.com/api/match/2?page={str(page)}'

        resp = requests.get(url=url, headers=headers).json()

        for value in resp['data']:
            ans += value['value']

    return ans


if __name__ == '__main__':

    print(get_ans(5))
