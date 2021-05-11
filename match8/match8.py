# -*- coding: utf-8 -*-
# @Time    : 2021-04-27 16:04
# @Author  : Kevin_Wang
# @File    : match8.py

import base64
import re
import requests
from collections import Counter
from PIL import Image

session = requests.session()
session.headers = {
    'Host': 'match.yuanrenxue.com',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Referer': 'http://match.yuanrenxue.com/list',
}
session.cookies.set('m', '3HLOKFMxDhNrLO%2FIBOjSG4%2Byjd0x0%2BWsRX8lyw6eIoRK2Q8wORTLDjrPtsKWolY4OsS4czgzpDx3aumcI'
                         '%2FU8kDdIuwUiUAlelLfpc%2Bhm8nMQLuxJPHnWcE6F'
                         '%2B5X0thhgWWiwq1L9dYmKK3dTerpXUEKsGDXfdaTGmtPkla1ZZrljbuSodnIn4N%2BdRwq'
                         '%2Byey3XIpxxl4nhKRl6AD6RTSoBwtnXx0fesqzfzBS5dzyfUHY6lZpY'
                         '%2BYmA2rcSXMmsM2siC6j88KRonwRLoeVYXC4x%2FRcP1lKoZTNthqTNMjbDqXOhOI2iKbqWHf%2BSeRv5j0YpiE3'
                         '%2Fikzf2JlfL7NdektS4w%3D%3Dr;')


def get_verify_img():
    verify_url = 'http://match.yuanrenxue.com/api/match/8_verify'

    res = session.get(verify_url).json()
    # print(session.cookies)
    # print(res['html'])
    verify_word = re.findall(r'<p>(.*?)</p>', res['html'], re.S)
    b64_img = re.findall(r'<img src="(.*?)"', res['html'], re.S)[0].replace('data:image/jpeg;base64,', '')

    return verify_word, b64_img


def show_img(b64_image):
    img = base64.b64decode(b64_image)
    with open('captcha.jpg', 'wb') as f:
        f.write(img)

    img = Image.open('captcha.jpg')
    img.show()


def idx_to_img_idx(indexes):
    img_idx_list = []
    for index in indexes:
        row = (index + 2) // 3
        col = index % 3
        if col == 0:
            col = 3
        img_idx_list.append(str(col + (col - 1) * 10 + (row-1) * 300))

    return img_idx_list


def get_ans(page_num):
    counter = Counter()
    for page in range(1, page_num+1):
        if page > 3:
            session.headers['User-Agent'] = 'yuanrenxue.project'
        verify_word, b64_img = get_verify_img()
        print(verify_word)
        show_img(b64_img)
        indexes = map(int, input('请输入依次序号，空格隔开，序号从1开始，从左到右，从上到下').split(' '))
        img_idx = idx_to_img_idx(indexes)
        answer = '|'.join(img_idx) + '|'
        url = f'http://match.yuanrenxue.com/api/match/8?page={page}&answer={answer}'
        res = session.get(url).json()
        print(res)
        for data in res['data']:
            counter[data['value']] += 1

    ans = 0
    max_count = 0
    # print(counter)
    for num, count in counter.items():
        if count > max_count:
            ans = num
            max_count = count

    print(ans)


if __name__ == '__main__':
    get_ans(5)

