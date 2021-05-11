# -*- coding: utf-8 -*-
# @Time    : 2021-04-05 22:01
# @Author  : Kevin_Wang
# @File    : match12.py
import base64
import requests


def get_m(page):

    before_encrypt = 'yuanrenxue' + str(page)

    after_encrypt = base64.b64encode(before_encrypt.encode())

    return after_encrypt.decode()


def get_answer(page_num):

    headers = {
        'Host': 'match.yuanrenxue.com',
        'Referer': 'http://match.yuanrenxue.com/match/12',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/88.0.4324.96 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'sessionid=qfjpavurh5h10clupk6v0er201k0ikfi',
    }

    url = 'http://match.yuanrenxue.com/api/match/12?page={}&m={}'

    ans = 0

    for page in range(1, page_num+1):
        if page > 3:
            headers['User-Agent'] = 'yuanrenxue.project'
        m = get_m(page)
        resp = requests.get(url=url.format(str(page), m), headers=headers).json()
        if resp['status'] == '1':
            for value in resp['data']:
                ans += value['value']
        else:
            print('requests error: ')
            print(resp)
            exit()

    print('success')
    return ans


if __name__ == '__main__':
    print(get_answer(5))



