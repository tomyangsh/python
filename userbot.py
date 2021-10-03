import os, asyncio, re, time, requests, random, subprocess, feedparser, aiocron

from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

from pytgcalls import GroupCallFactory

from FastTelethon.FastTelethon import download_file, upload_file

from datetime import datetime, timedelta
from time import time
from io import BytesIO

from itertools import permutations

app_id = int(os.getenv("APP_ID"))
app_hash = os.getenv("APP_HASH")
tmdb_key = os.getenv("TMDB_KEY")
deepl_key = os.getenv("DEEPL_KEY")

titlelist = []
for item in open('titlelist'):
    titlelist.append(item.strip("\n"))
'''
music_list = []
for root, dirs, files in os.walk("music"):
     for file in files:
             if file.endswith(".raw"):
                     music_list.append(os.path.join(root, file))
'''
def am_search(query):
    url = 'https://itunes.apple.com/us/search?term='+requests.utils.quote(query)+'&entity=song&limit=1'
    return url

bot = Client('userbot', app_id, app_hash)

def get_translation(text):
    url = 'https://api-free.deepl.com/v2/translate'
    payload = {'auth_key': deepl_key, 'text': text, 'target_lang': 'ZH'}
    result = requests.post(url, data=payload).json()['translations'][0]['text']
    return result

'''
@bot.on_message(filters.chat([-1001345466016, -522044327]) & filters.command("join"))
async def join_group_call(client, m: Message):
    group_call =

group_call = GroupCallFactory(bot).get_file_group_call(music_list[random.randint(0,len(music_list)-1)], play_on_repeat=False)

@group_call.on_playout_ended
async def switch_song(_, source):
    group_call.input_filename = music_list[random.randint(0,len(music_list)-1)]

@bot.on_message(filters.chat([-1001345466016, -522044327]) & filters.command("live"))
async def live_music(_, message):
    await group_call.start(message.chat.id)
'''
@bot.on_message(filters.chat([-1001345466016, -522044327]) & filters.command("ban"))
def ban_user(client: "Client", message: "types.Message"):
    source_id = message.from_user.id
    if bot.get_chat_member(message.chat.id, source_id).status == "member":
        bot.restrict_chat_member(message.chat.id, source_id, ChatPermissions(), int(time() + 300))
        return
    msg = bot.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
    target_id = msg.from_user.id
    if bot.get_chat_member(message.chat.id, target_id).status == "member":
        bot.restrict_chat_member(message.chat.id, target_id, ChatPermissions(), int(time() + 300))


@bot.on_message(filters.outgoing & filters.command("trans"))
def translate(client: "Client", message: "types.Message"):
    msg = bot.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
    result = get_translation(msg.text or msg.caption)
    bot.edit_message_text(message.chat.id, message.message_id, result)
'''
@bot.on_message(from_users=728062910, pattern=r'.*\n.*\n.*\n\n群内发送关键词'))
def auto_lottery(client: "Client", message: "types.Message"):
    msg = message.text
    key_word = re.sub(r'.*\n.*\n.*\n\n群内发送关键词\s', '', msg)[:-5]
    bot.send_message(message.chat.id, key_word)
'''
@bot.on_message(filters.sticker & filters.user([634261570, 681532273]))
def sticker(client: "Client", message: "types.Message"):
    sticker_id = message.sticker.file_id
    bot.send_sticker(message.chat.id, sticker_id, reply_to_message_id=message.message_id)

@bot.on_message(filters.user([1046900703, 1058117864]))
def withdraw_master(client: "Client", message: "types.Message"):
    bot.forward_messages(1359252145, message.chat.id, message.message_id)

@bot.on_message(filters.reply & filters.user(604039549))
def auto_sign_in(client: "Client", message: "types.Message"):
    if not message.reply_to_message.from_user.is_self:
        return
    msg = message.text
    key = re.search(r'/q (.*)', msg).group(1)
    if len(key) > 6:
        return
    keylist = []
    for i in permutations(key):
        keylist.append(''.join(i))
    result = next(iter(set(keylist).intersection(titlelist)))
    bot.send_message(message.chat.id, '/q '+result)

@bot.on_message(filters.outgoing & filters.regex(r're$'))
def repeat_msg(client: "Client", message: "types.Message"):
    source_msg = bot.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
    bot.forward_messages(message.chat.id, message.chat.id, source_msg.message_id)
    bot.delete_messages(message.chat.id, message.message_id)

bot.run()

