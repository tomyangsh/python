import os

from pyrogram import Client

def client(name='dtl', **kwargs):
    _client = Client(name=name, workdir=os.path.dirname(__file__), **kwargs)
    return _client

def msg(msg: str, chat_id=None):
    with client('dtl') as bot:
        bot.send_message(chat_id or 'me', msg)

def img(img, chat_id=None):
    with client('dtl') as bot:
        bot.send_photo(chat_id or 'me', img)

def audio(audio, chat_id=None):
    with client('dtl') as bot:
        bot.send_audio(chat_id or 'me', audio)

def video(video, chat_id=None, caption=None):
    with client('dtl') as bot:
        bot.send_video(chat_id or 'me', video, caption=caption)
