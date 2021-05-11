# -*- coding: utf-8 -*-
# @Time    : 2021-04-05 23:08
# @Author  : Kevin_Wang
# @File    : match13.py
import re
import requests


class Match13:

    def __init__(self):
        self.session_id = 'qfjpavurh5h10clupk6v0er201k0ikfi;'
        self.headers = {
            'Host': 'match.yuanrenxue.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/88.0.4324.96 Safari/537.36',
            'Cookie': 'sessionid=' + self.session_id,
            }
        self.headers['Cookie'] += self.get_cookie()

    def get_cookie(self):

        index_url = 'http://match.yuanrenxue.com/match/13'

        resp = requests.get(url=index_url, headers=self.headers)

        yuanrenxue_cookie_char = re.findall(r"\('(.*?)'\)", resp.text, re.S)
        yuanrenxue_cookie = ''.join(yuanrenxue_cookie_char)

        return yuanrenxue_cookie

    def get_answer(self, page_num):

        url = 'http://match.yuanrenxue.com/api/match/13?page={}'

        ans_headers = self.headers.copy()
        ans_headers['Referer'] = 'http://match.yuanrenxue.com/match/13'

        ans = 0
        page = 1
        while page <= page_num:
            if page > 3:
                ans_headers['User-Agent'] = 'yuanrenxue.project'

            resp = requests.get(url=url.format(str(page)), headers=ans_headers).json()

            if resp['status'] == '1':
                for value in resp['data']:
                    ans += value['value']
                page += 1
            else:
                ans_headers['Cookie'] = 'sessionid=' + self.session_id + ';' + self.get_cookie()

        return ans


if __name__ == '__main__':
    match = Match13()

    print(match.get_answer(5))





