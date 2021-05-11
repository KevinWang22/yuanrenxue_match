# -*- coding: utf-8 -*-
# @Time    : 2021-04-11 17:59
# @Author  : Kevin_Wang
# @File    : match5.py

import base64
import time
import execjs
import requests


def get_answer(page_num=1):
    ans = 0
    hot_list = []
    for page in range(1, page_num+1):
        m = int(time.time() * 1000)
        f = int(time.time()) * 1000

        url = f'http://match.yuanrenxue.com/api/match/5?page={page}&m={m}&f={f}'

        headers = {
            'Host': 'match.yuanrenxue.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/89.0.4389.114 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                      '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': 'm=' + get_enc_m(m) + ';RM4hZBv0dDon443M=' + get_RM4hZBv0dDon443M(m),
        }

        if page > 3:
            headers['User-Agent'] = 'yuanrenxue.project'

        res = requests.get(url=url, headers=headers).json()
        print(res)
        hot_list.extend([v['value'] for v in res['data']])
    hot_list.sort()
    print(hot_list)
    ans = sum(hot_list[-5:])
    print(ans)


def get_RM4hZBv0dDon443M(ori_m):

    with open('match5.js', 'r', encoding='utf-8') as f:
        js_code = f.read()

    ctx = execjs.compile(js_code)
    enc_m = base64.b64encode(str(ori_m).encode()).decode()
    # print(enc_m)
    return ctx.call('get_RM4hZBv0dDon443M', ori_m, enc_m)


def get_enc_m(ori_m):
    with open('match5.js', 'r', encoding='utf-8') as f:
        js_code = f.read()

    ctx = execjs.compile(js_code)
    enc_m = ctx.call('get_m', ori_m)

    return enc_m


if __name__ == '__main__':

    get_answer(5)
