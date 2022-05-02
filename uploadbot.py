import sys
import ffmpeg
import os
import requests
import re

from pyrogram import Client

def get_metadata(video_path):
    width, height, duration = 1920, 1080, 0
    try:
        video_streams = ffmpeg.probe(video_path, select_streams="v")["streams"][0]
        height = video_streams["height"]
        width = video_streams["width"]
        duration = int(float(video_streams["duration"]))
    except Exception as e:
        print(e)
    return dict(height=height, width=width, duration=duration)


def get_thumbnail(video_path):
    thumbnail = os.path.dirname(__file__)+'/thumbnail.png'
    ff =    (
            ffmpeg
            .input(video_path, ss='1')
            .output(thumbnail, vframes=1)
            .overwrite_output()
            .run(quiet=True)
        )
    return thumbnail

def progress(current, total):
    sys.stdout.write(f"\r{current * 100 / total:.1f}%")
    sys.stdout.flush()

with Client("upload") as app:
    video_path = sys.argv[1]
    video_name = os.path.basename(video_path)
    try:
        ep_no = re.search('\w\d\d\w\d\d', video_name).group().upper()
        query = re.sub('\.', ' ', re.match('(\S+)\.\w\d\d\w\d\d', video_name).group(1))
        res = requests.get('https://api.themoviedb.org/3/search/tv/?language=zh-CN&api_key=&query='+query).json()['results'][0]
        name_chi = re.sub('：', '_', res.get('name'))
        name_org = re.sub('：', '_', res.get('original_name'))
        caption = '#'+name_chi+' '+name_org+' '+ep_no
        print(caption)
    except:
        caption = ''
    meta = get_metadata(video_path)
    thumbnail = get_thumbnail(video_path)
    app.send_video("me", video_path, caption=caption, thumb=thumbnail, **meta, progress=progress)
    os.unlink(thumbnail)
