import os, asyncio, re, time, requests, random, subprocess, feedparser, aiocron

from telethon import TelegramClient, events
from telethon import utils
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeFilename

from FastTelethon.FastTelethon import download_file, upload_file

from datetime import datetime, timedelta
from io import BytesIO

from itertools import permutations

app_id = int(os.getenv("APP_ID"))
app_hash = os.getenv("APP_HASH")
tmdb_key = os.getenv("TMDB_KEY")
deepl_key = os.getenv("DEEPL_KEY")

song_list = []
for item in open('songlist'):
    song_list.append(item.strip("\n"))

titlelist = []
for item in open('titlelist'):
    titlelist.append(item.strip("\n"))

def am_search(query):
    url = 'https://itunes.apple.com/us/search?term='+requests.utils.quote(query)+'&entity=song&limit=1'
    return url

bot = TelegramClient('bot', app_id, app_hash)
bot.start()

def get_translation(text):
    url = 'https://api-free.deepl.com/v2/translate'
    payload = {'auth_key': deepl_key, 'text': text, 'target_lang': 'ZH'}
    result = requests.post(url, data=payload).json()['translations'][0]['text']
    return result

'''
@aiocron.crontab('*/30 * * * *')
async def push_rarbg():
    item_list = get_rarbg()
    for item in item_list:
        await bot.send_message(1195256281, item)
'''
@bot.on(events.NewMessage(outgoing=True, pattern='/ban'))
async def ban_user(event):
#    if not event.from_id.is_admin:
#        return
    msg = await event.get_reply_message()
    user = msg.from_id
    await bot.edit_permissions(event.message.chat_id, user, timedelta(minutes=5), send_messages=False)


@bot.on(events.NewMessage(outgoing=True, pattern='/trans'))
async def translate(event):
    msg = await event.get_reply_message()
    result = get_translation(msg.text)
    await bot.edit_message(event.message.chat_id, event.message, result)

@bot.on(events.NewMessage(from_users=728062910, pattern=r'.*\n.*\n.*\n\n群内发送关键词'))
async def auto_lottery(event):
    msg = event.message.text
    key_word = re.sub(r'.*\n.*\n.*\n\n群内发送关键词\s', '', msg)[:-5]
    await bot.send_message(event.chat_id, key_word)

@bot.on(events.NewMessage(from_users=681532273))
async def sticker(event):
    msg = event.message
    try:
        if event.message.file.sticker_set:
            await event.reply(msg)
    except:
        return

@bot.on(events.NewMessage(from_users=[1046900703, 1058117864]))
async def withdraw_master(event):
    msg = event.message
    msgtext = event.message.text
    await bot.forward_messages(1359252145, msg)
'''
@bot.on(events.NewMessage(from_users=1058117864))
async def shut_up(event):
    await event.reply('闭嘴')
'''
'''
@bot.on(events.NewMessage(from_users=1890475209, pattern='Rocinante 问'))
async def yanshu(event):
    await bot.send_message(event.message.chat_id, '答得出吗?')
    async with bot.conversation(event.message.chat_id, exclusive=False, total_timeout=60) as conv:
        try:
            if await conv.wait_event(events.MessageEdited(from_users=1890475209)):
                await bot.send_message(event.message.chat_id, '又超时 菜鸡')
        except:
            return
'''

@bot.on(events.NewMessage(outgoing=True, pattern=r'/q$|/q@NasaRelayBot$'))
async def auto_qqq(event):
    try:
        async with bot.conversation(event.message.chat_id, exclusive=False, total_timeout=20) as conv:
            question = await conv.wait_event(events.NewMessage(from_users=604039549))
            msg = question.message.text
            key = re.search(r'/q (.*)', msg).group(1)
            keylist = []
            for i in permutations(key):
                keylist.append(''.join(i))
            result = next(iter(set(keylist).intersection(titlelist)))
            await bot.send_message(event.message.chat_id, '/q '+result)
    except Exception as e:
        print(e)
        return

@bot.on(events.NewMessage(outgoing=True, pattern=r'^-re$'))
async def repeat_msg(event):
    source_msg = await event.get_reply_message()
    await bot.forward_messages(event.chat_id, source_msg)
    await bot.delete_messages(event.chat_id, event.message)
'''
@bot.on(events.NewMessage(chats=1058117864, outgoing=True, pattern=r'1$'))
async def flood(event):
    async with bot.conversation(event.message.chat_id) as conv:
        while 1:
            msg = await bot.send_message(event.message.chat_id, '[老刘](tg://user?id=1058117864)')
#            await bot.delete_messages(event.message.chat_id, msg)
            try:
                if await conv.wait_event(events.NewMessage(pattern=r'2$'), timeout=0.01):
                    return
            except:
                continue
'''
@bot.on(events.NewMessage(outgoing=True, pattern=r'/banme$'))
async def banme(event):
    while 1:
        await bot.send_message(event.message.chat_id, '/banme')


'''
@bot.on(events.NewMessage(pattern=r'^猜歌$'))
async def send_song(event):
    song = random.choice(song_list)
    song_name = re.search(r'-\s.*$', song).group()[2:]
    print(song_name)
    song_info = requests.get(am_search(song)).json()
    preview_url = song_info['results'][0]['previewUrl']
    song_file = BytesIO(requests.get(preview_url).content)
    song_file.mime_type = 'audio/mpeg'
    song_file.name = 'preview.mp3'
    question = await bot.send_file(event.chat_id, song_file, attributes=[DocumentAttributeAudio(duration=30)])
    try:
        async with bot.conversation(event.chat_id, exclusive=False, total_timeout=60) as conv:
             while True:
                response = await conv.wait_event(events.NewMessage())
                try:
                    responder_name = response.sender.first_name
                except:
                    responder_name = 'BOSS'
                answer = response.message.text
                if re.match(song_name[:10], answer, re.IGNORECASE):
                    caption2 = responder_name+' 回答正确！\n**'+song+'**'
                    await bot.send_message(event.chat_id, caption2, reply_to=response)
                    break
    except Exception as e:
        print(e)
        await bot.edit_message(question, '答题超时，答案：'+song)
'''
bot.run_until_disconnected()
