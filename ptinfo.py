#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import re
import json
import ffmpeg
import requests

from tmdb import method, type
from myfunc import media

file_path = sys.argv[1]
file_name = os.path.basename(file_path)

mediainfo = media.mediainfo(file_path)

thumb = []

try:
    for i in [3, 6, 9, 12]:
        f = media.ss(file_path, f'{i}:00')
        thumb.append(media.upload(f))
    thumb = '[img]'+'[/img]\n[img]'.join(thumb)+'[/img]'
except Exception as e:
    pass


def zh_name(id):
     request_url = 'https://www.wikidata.org/w/api.php?action=query&format=json&uselang={}&prop=entityterms&generator=search&formatversion=2&gsrsearch=haswbstatement%3A%22P4985%3D{}%22'
     res = requests.get(request_url.format('zh-cn', id)).json().get('query', {}).get('pages', [])
     wiki_id = next((item.get('title') for item in res), '')
     request_url = 'https://www.wikidata.org/w/api.php?action=wbgetentities&format=json&ids={}&languages=zh-cn&languagefallback=1&formatversion=2'.format(wiki_id)
     res = requests.get(request_url).json()
     name = res.get('entities', {}).get(wiki_id, {}).get('labels', {}).get('zh-cn', {}).get('value', '')
     return name

if not re.search('[Ss]\d\d[Ee]\d\d', file_name):
    name = re.sub('\.', ' ', re.match('(\D+)\.\d\d\d\d', file_name).group(1))
    year = re.search('\.(\d\d\d\d)\.', file_name).group(1)
    s = method.search_movie(name, year)
    s = [{'id': i['id'], 'name': i['title'], 'date': i['release_date']} for i in s[:3]]
    print('\n'.join(f"{s.index(i)}. {i['name']} {i['date']}" for i in s), file=sys.stderr)
    c = int(input())
    id = s[c]['id']
    m = type.Movie(id)
    cast = '\n          '.join([zh_name(i['id']) or i['name'] for i in m.cast])
    ptinfo = f"""
[img]{m.poster}[/img]
[size=3]
[b]{m.name} {m.ori_name} ({m.year})[/b]

导演   {'  '.join(m.director)}
类型   {' / '.join(m.genres)}
国家   {' / '.join(m.country)}
语言   {m.lang}
上映   {m.date}
片长   {m.runtime}分钟
IMDb  https://www.imdb.com/title/{m.imdb}/
演员   {cast}

{m.des}
[/size]
{thumb}

[expand]
{mediainfo}
[/expand]
"""

else:
    name = re.sub('\.', ' ', re.match('(\S+)\.[Ss]\d\d[Ee]\d\d', file_name).group(1))
    season = int(re.match('\S+\.[Ss](\d\d)[Ee]\d\d', file_name).group(1))
    s = method.search_tv(name)
    s = [{'id': i['id'], 'name': i['name'], 'date': i['first_air_date']} for i in s[:3]]
    print('\n'.join(f"{s.index(i)}. {i['name']} {i['date']}" for i in s), file=sys.stderr)
    c = int(input())
    id = s[c]['id']
    t = type.TV(id)
    poster = next((s['poster'] for s in t.seasons if s['season'] == season), '')
    cast = '\n          '.join([zh_name(i['id']) or i['name'] for i in t.cast])
    ptinfo = f"""
[img]{poster}[/img]
[size=3]
[b]{t.name} {t.ori_name} ({t.year})[/b]

主创   {'  '.join(t.creator)}
类型   {' / '.join(t.genres)}
国家   {' / '.join(t.country)}
语言   {t.lang}
网络   {'  '.join(t.network)}
首播   {t.date}
IMDb  https://www.imdb.com/title/{t.imdb}/
演员   {cast}

{t.des}
[/size]
{thumb}

[expand]
{mediainfo}
[/expand]
"""


print(ptinfo)

