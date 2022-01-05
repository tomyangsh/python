import sys
import os
import ffmpeg

from pyrogram import Client

video_path = os.path.dirname(__file__)+'/downloads/temp.mp4'

def get_metadata():
    width, height, duration = 1920, 1080, 0
    try:
        video_streams = ffmpeg.probe(video_path, select_streams="v")["streams"][0]
        height = video_streams["height"]
        width = video_streams["width"]
        duration = int(float(video_streams["duration"]))
    except Exception as e:
        print(e)
    return dict(height=height, width=width, duration=duration)

def get_thumbnail():
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
    msg = app.get_messages(int('-100'+str(sys.argv[1])), int(sys.argv[2]))
    file_id = msg.video.file_id
    app.download_media(file_id, "temp.mp4")
    caption = msg.caption or ''
    meta = get_metadata()
    thumbnail = get_thumbnail()
    app.send_video("me", video_path, caption=caption, thumb=thumbnail, **meta)
    os.unlink(thumbnail)
    os.unlink(video_path)

