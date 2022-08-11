import os

from pyrogram import Client

def client(name='dtl', **kwargs):
    _client = Client(name=name, workdir=os.path.dirname(__file__), **kwargs)
    return _client

def msg(msg: str, chat_id='me'):
    with client('dtl') as bot:
        bot.send_message(chat_id, msg)

def img(img, chat_id='me'):
    with client('dtl') as bot:
        bot.send_photo(chat_id, img)

def audio(audio, chat_id='me'):
    with client('dtl') as bot:
        bot.send_audio(chat_id, audio)

def video(video, chat_id='me', caption=None):
    with client('dtl') as bot:
        bot.send_video(chat_id, video, caption=caption, width=1920, height=1080)
