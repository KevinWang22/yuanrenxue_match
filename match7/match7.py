# -*- coding: utf-8 -*-
# @Time    : 2021-04-19 14:04
# @Author  : Kevin_Wang
# @File    : match7.py
import base64
import re
import requests
from fontTools.ttLib import TTFont


num_dict = {
    26: '0',
    10: '1',
    30: '2',
    44: '3',
    15: '4',
    37: '5',
    41: {
        13: '6',
        12: '9',
    },
    7: '7',
    57: '8',
}
names = ['极镀ギ紬荕', '爷灬霸气傀儡', '梦战苍穹', '傲世哥', 'мaη肆風聲', '一刀メ隔世', '横刀メ绝杀', 'Q不死你R死你',
         '魔帝殤邪', '封刀不再战', '倾城孤狼', '戎马江湖', '狂得像风', '影之哀伤', '謸氕づ独尊', '傲视狂杀', '追风之梦',
         '枭雄在世', '傲视之巅', '黑夜刺客', '占你心为王', '爷来取你狗命', '御风踏血', '凫矢暮城', '孤影メ残刀', '野区霸王',
         '噬血啸月', '风逝无迹', '帅的睡不着', '血色杀戮者', '冷视天下', '帅出新高度', '風狆瑬蒗', '灵魂禁锢', 'ヤ地狱篮枫ゞ',
         '溅血メ破天', '剑尊メ杀戮', '塞外う飛龍', '哥‘K纯帅', '逆風祈雨', '恣意踏江山', '望断、天涯路', '地獄惡灵', '疯狂メ孽杀',
         '寂月灭影', '骚年霸称帝王', '狂杀メ无赦', '死灵的哀伤', '撩妹界扛把子', '霸刀☆藐视天下', '潇洒又能打', '狂卩龙灬巅丷峰',
         '羁旅天涯.', '南宫沐风', '风恋绝尘', '剑下孤魂', '一蓑烟雨', '领域★倾战', '威龙丶断魂神狙', '辉煌战绩', '屎来运赚',
         '伱、Bu够档次', '九音引魂箫', '骨子里的傲气', '霸海断长空', '没枪也很狂', '死魂★之灵']


def get_font_info(res, page):
    woff = res['woff']
    b_ttf = base64.b64decode(woff)
    with open(f'{page}.ttf', 'wb') as f:
        f.write(b_ttf)

    font = TTFont(f'{page}.ttf')
    # print(font)
    font.saveXML(f'{page}.xml')
    with open(f'{page}.xml', 'r') as f:
        font_data = f.read()
    # print(font_data)
    glyphs = re.findall(r'(<TTGlyph name="uni.*?</TTGlyph>)', font_data, re.S)
    cmap_main_pattern = r'<cmap_format_4 platformID="0" platEncID="3" language="0">(.*?)</cmap_format_4>'
    maps = re.findall(cmap_main_pattern, font_data, re.S)[0]
    maps = re.findall(r'(<map.*?/>)', maps, re.S)

    return glyphs, maps


def parse_glyphs(glyphs):

    glyph_dict = {}

    for glyph in glyphs:
        glyph_name = re.findall(r'<TTGlyph name="(.*?)" xMin', glyph, re.S)[0]
        contours = re.findall(r'(<contour>.*?</contour>)', glyph, re.S)
        pts = len(re.findall(r'(<pt.*?/>)', glyph, re.S))
        num = num_dict[pts]
        # print("before")
        # print(num)
        if isinstance(num, dict):
            contour2_pts = len(re.findall(r'(<pt.*?/>)', contours[-1], re.S))
            num = num[contour2_pts]
            # print('after')
            # print(num)
        glyph_dict[glyph_name] = num

    return glyph_dict


def parse_maps(maps):

    map_dict = {}

    for cmap in maps:
        code = re.findall(r'code="0x([a-z]\d{3})" name', cmap, re.S)[0]
        name = re.findall(r'name="(uni[a-z]\d{3})"/>', cmap, re.S)[0]
        map_dict[name] = code

    return map_dict


def parse_code_num_dict(glyph_dict, map_dict):
    code_num_dict = {}

    for name, num in glyph_dict.items():
        code_num_dict[map_dict[name]] = num

    return code_num_dict


def parse_name_num(page, data, code_num):
    name_num_list = []
    yyd = 1
    for val in data:
        name = names[yyd+(page-1)*10]
        val = val['value'].replace('&#x', '')
        codes = val.split(' ')[:-1]
        num = int(''.join([code_num[code] for code in codes]))
        name_num_list.append((name, num))
        yyd += 1

    return name_num_list


def get_ans(page_num):

    headers = {
        'Host': 'match.yuanrenxue.com',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/89.0.4389.114 Safari/537.36',
        'Referer': 'http://match.yuanrenxue.com/match/7',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,'
                  '*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }
    ans = []

    for page in range(1, page_num+1):
        url = f'http://match.yuanrenxue.com/api/match/7?page={page}'

        if page > 3:
            headers['User-Agent'] = 'yuanrenxue.project'

        res = requests.get(url=url, headers=headers).json()
        datas = res['data']

        glyphs, cmaps = get_font_info(res, page)
        glyph_dict = parse_glyphs(glyphs)
        map_dict = parse_maps(cmaps)
        code_num = parse_code_num_dict(glyph_dict, map_dict)
        name_nums = parse_name_num(page, datas, code_num)
        # print(name_nums)
        ans.extend(name_nums)

    ans.sort(key=lambda x: x[1], reverse=True)

    print(ans[0])


if __name__ == '__main__':
    get_ans(5)



