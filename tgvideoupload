#!/usr/bin/python

import sys
import os
import requests
import re

from myfunc import tg, media
from tmdb import method

def get_metadata(video_path):
    width, height, duration = 1920, 1080, 0
    try:
        video = media.Video(video_path)
        height = video.height
        width = video.width
        duration = video.duration
    except Exception as e:
        print(e)
    return dict(height=height, width=width, duration=duration)

def progress(current, total):
    sys.stdout.write(f"\r{current * 100 / total:.1f}%")
    sys.stdout.flush()

with tg.client() as app:
    video_path = sys.argv[1]
    video_name = os.path.basename(video_path)
    try:
        ep_no = re.search('\w\d\d\w\d\d', video_name).group().upper()
        query = re.sub('\.', ' ', re.match('(\S+)\.\w\d\d\w\d\d', video_name).group(1))
        res = method.search_tv(query)[0]
        name_chi = re.sub('：', '_', res.get('name'))
        name_org = re.sub('：', '_', res.get('original_name'))
        caption = '#'+name_chi+' '+name_org+' '+ep_no
        print(caption)
    except Exception as e:
        caption = ''
    meta = get_metadata(video_path)
    thumbnail = media.bytesio(media.ss(video_path), 'png')
    app.send_video("me", video_path, caption=caption, thumb=thumbnail, **meta, progress=progress)
