# -*- coding: utf-8 -*-
# @Time    : 2021-04-06 13:55
# @Author  : Kevin_Wang
# @File    : match3.py
import requests


def get_ans(page_num=5):
    session = requests.session()
    headers = {
        'Host': 'match.yuanrenxue.com',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.96 Safari/537.36',
        'Accept': '*/*',
        'Origin': 'http://match.yuanrenxue.com',
        'Referer': 'http://match.yuanrenxue.com/match/3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    session.headers = headers
    url = 'http://match.yuanrenxue.com/api/match/3?page={}'
    before_url = 'http://match.yuanrenxue.com/logo'

    num_counter = {}

    for page in range(1, page_num+1):

        if page > 3:
            session.headers['User-Agent'] = 'yuanrenxue.project'
        session.post(url=before_url)
        resp = session.get(url=url).json()
        for value in resp['data']:
            num_counter[value['value']] = num_counter.get(value['value'], 0) + 1

    ans = 0
    max_count = 0

    for value, count in num_counter.items():
        if count > max_count:
            ans = value
            max_count = count

    return ans


if __name__ == '__main__':

    print(get_ans())
