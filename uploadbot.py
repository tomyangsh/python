import sys
import ffmpeg
import os

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
            .run()
        )
    return thumbnail


with Client("upload") as app:
    video_path = sys.argv[1]
    try:
        caption = sys.argv[2]
    except:
        caption = ''
    meta = get_metadata(video_path)
    thumbnail = get_thumbnail(video_path)
    app.send_video("me", video_path, caption=caption, thumb=thumbnail, **meta)
    os.unlink(thumbnail)
