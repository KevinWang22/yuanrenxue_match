# -*- coding: utf-8 -*-
# @Time    : 2021-04-01 16:36
# @Author  : Kevin_Wang
# @File    : match1.py
import requests
import time
import execjs


def get_answer():

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.96 Safari/537.36',
        'host': 'match.yuanrenxue.com',
        'referer': 'http://match.yuanrenxue.com/match/1',
        'X-Requested-With': 'XMLHttpRequest',
        'cookie': 'sessionid=gzd8dgvxxkotl9pfrv9zznawoo62r74e;'
    }

    total_price = 0
    total_flight = 0

    for page in range(1, 6):

        if page > 3:
            headers['user-agent'] = 'yuanrenxue.project'

        timestamp = int(time.time()) * 1000 + 100000000
        m = get_m(str(timestamp)) + '%E4%B8%A8' + str(timestamp // 1000)

        url = f'http://match.yuanrenxue.com/api/match/1?page={str(page)}&m={m}'

        resp = requests.get(url=url, headers=headers).json()

        print(resp)
        prices = [price['value'] for price in resp['data']]

        total_price += sum(prices)
        total_flight += len(prices)

    return total_price / total_flight


def get_m(timestamp):

    with open('match1.js', 'r', encoding='utf-8') as f:
        js_code = f.read()

    ctx = execjs.compile(js_code)

    m = ctx.call('get_f', timestamp)

    return m


if __name__ == '__main__':

   print(get_answer())


