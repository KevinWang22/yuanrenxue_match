# -*- coding: utf-8 -*-
# @Time    : 2021-04-30 10:45
# @Author  : Kevin_Wang
# @File    : match14.py
import execjs
import requests
import time


session = requests.session()
session.headers = {
    'Host': 'match.yuanrenxue.com',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/89.0.4389.114 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://match.yuanrenxue.com/match/14',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

session.cookies.update({'sessionid': 'xw9vg0adop0coax5zjxoy53d0p1stzjp',
                        'mz': 'TW96aWxsYSxOZXRzY2FwZSw1LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7'
                              'IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ'
                              '2hyb21lLzg5LjAuNDM4OS4xMTQgU2FmYXJpLzUzNy4zNixbb2JqZWN0IE5ldH'
                              'dvcmtJbmZvcm1hdGlvbl0sdHJ1ZSwsW29iamVjdCBHZW9sb2NhdGlvbl0sOCx6aC'
                              '1DTix6aC1DTix6aCwwLFtvYmplY3QgTWVkaWFDYXBhYmlsaXRpZXNdLFtvYmplY3Q'
                              'gTWVkaWFTZXNzaW9uXSxbb2JqZWN0IE1pbWVUeXBlQXJyYXldLHRydWUsW29iamVjd'
                              'CBQZXJtaXNzaW9uc10sV2luMzIsW29iamVjdCBQbHVnaW5BcnJheV0sR2Vja28sMjAw'
                              'MzAxMDcsW29iamVjdCBVc2VyQWN0aXZhdGlvbl0sTW96aWxsYS81LjAgKFdpbmRvd3Mg'
                              'TlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZ'
                              'SBHZWNrbykgQ2hyb21lLzg5LjAuNDM4OS4xMTQgU2FmYXJpLzUzNy4zNixHb29nbGUgSW5jL'
                              'iwsW29iamVjdCBEZXByZWNhdGVkU3RvcmFnZVF1b3RhXSxbb2JqZWN0IERlcHJlY2F0ZWRTdG9y'
                              'YWdlUXVvdGFdLDEwNDAsMCwwLDE5MjAsMjQsMTA4MCxbb2JqZWN0IFNjcmVlbk9yaWVudGF0aW9uXS'
                              'wyNCwxOTIwLFtvYmplY3QgRE9NU3RyaW5nTGlzdF0sZnVuY3Rpb24gYXNzaWduKCkgeyBbbmF0aX'
                              'ZlIGNvZGVdIH0sLG1hdGNoLnl1YW5yZW54dWUuY29tLG1hdGNoLnl1YW5yZW54dWUuY29tLGh0dH'
                              'A6Ly9tYXRjaC55dWFucmVueHVlLmNvbS9tYXRjaC8xNCxodHRwOi8vbWF0Y2gueXVhbnJlbnh1ZS5j'
                              'b20sL21hdGNoLzE0LCxodHRwOixmdW5jdGlvbiByZWxvYWQoKSB7IFtuYXRpdmUgY29kZV0gfSxmdW'
                              '5jdGlvbiByZXBsYWNlKCkgeyBbbmF0aXZlIGNvZGVdIH0sLGZ1bmN0aW9uIHRvU3RyaW5nKCkgeyBbb'
                              'mF0aXZlIGNvZGVdIH0sZnVuY3Rpb24gdmFsdWVPZigpIHsgW25hdGl2ZSBjb2RlXSB9',
                        })


def get_window_params_code():
    m_code_url = 'http://match.yuanrenxue.com/api/match/14/m'

    res = session.get(m_code_url)

    return "var window = global;\n" + res.text + '\n'


def get_ans(page_num):
    ans = 0
    for page in range(1, page_num+1):
        if page > 3:
            session.headers['User-Agent'] = 'yuanrenxue.project'
        url = f'http://match.yuanrenxue.com/api/match/14?page={page}'
        pre_js_code = get_window_params_code()
        with open('match14_get_m.js', 'r', encoding='utf-8') as f:
            js_code = f.read()
        js_code = pre_js_code + js_code
        ctx = execjs.compile(js_code)
        m = ctx.call('get_cookie', 2).replace('m=', '').replace(';path=/', '')
        # print(m)
        # m_params = {
        #     'timestamp_a': 12959728784000,# timestamp_a,
        #     'timestamp_b': 1619966098000, # timestamp_b,
        #     'click_time': 1, # page,
        #     'v14': "h7ja1vfb8",# v14,
        #     'v142': "443329492",# v142
        # }
        # m = requests.post('http://localhost:2229/encrypt', data=m_params).text
        # print(m)
        session.cookies.update({'m': m})
        # print(session.cookies)
        # print(session.headers)
        res = session.get(url=url)
        print(res.json())
        for data in res.json()['data']:
            ans += data['value']

    print(ans)


if __name__ == '__main__':
    get_ans(5)
    # with open('match14_get_m.js', 'r', encoding='utf-8') as f:
    #     js_code = f.read()
    # ctx = execjs.compile(js_code)
    # print(ctx.call('sp', 12959728784000, 1619966098000, 1, "h7ja1vfb8", "443329492"))
