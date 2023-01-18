import os, re, requests

from io import BytesIO

from pyrogram import Client
from pyrogram.types import InputMediaPhoto

def client(name='dtl', **kwargs):
    _client = Client(name=name, workdir=os.path.dirname(__file__), **kwargs)
    return _client

def send(chat_id, *content, **kwargs):
    text = None
    image = None
    video = None
    image_set = None
    for i in content:
        if isinstance(i, str):
            if re.match('^http.+(jpg|jpeg|png)$', i):
                image = i
            elif re.match('^http.+mp4$', i):
                video = i
            else:
                text = i
        if isinstance(i, list):
            image_set = [InputMediaPhoto(BytesIO(requests.get(j).content)) for j in i]
    with client() as app:
        if image:
            app.send_photo(chat_id, image, caption=text, **kwargs)
        elif video:
            app.send_video(chat_id, video, caption=text, **kwargs)
        elif image_set:
            image_set[0].caption = text
            app.send_media_group(chat_id, image_set, **kwargs)
        else:
            app.send_message(chat_id, text, **kwargs)
