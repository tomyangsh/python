import os, re, time, requests, random, asyncio, aiocron, psycopg2

from pyrogram import Client, filters, enums
from pyrogram.types import ChatPermissions
from pyrogram.raw import functions, types
from pyrogram.raw.functions.messages import GetFullChat

from io import BytesIO

from itertools import permutations

from random import randint, sample

from datetime import datetime, timedelta

deepl_key = os.getenv("DEEPL_KEY")

bot = Client('userbot')

def get_translation(text):
    url = 'https://api-free.deepl.com/v2/translate'
    payload = {'auth_key': deepl_key, 'text': text, 'target_lang': 'ZH'}
    result = requests.post(url, data=payload).json()['translations'][0]['text']
    return result

@aiocron.crontab('0 14 * * *')
async def clean():
    msg_list = bot.search_messages(-1001345466016, query="回答正确", from_user=1890475209)
    async for message in msg_list:
        await bot.delete_messages(-1001345466016, message.id)
    msg_list = bot.search_messages(-1001345466016, from_user=1788219924)
    async for message in msg_list:
        await bot.delete_messages(-1001345466016, message.id)

@bot.on_message(filters.chat("flower2048") & filters.new_chat_members)
async def welcome(client, message):
    await message.reply_text("欢迎新王晶")

@bot.on_message(filters.user(1890475209) & filters.regex("这部影片的标题是:"))
def auto_answer(client: "Client", message: "types.Message"):
    time.sleep(60)
    msg = bot.get_messages(message.chat.id, message.id)
    if not msg.reply_markup:
        return
    list = msg.reply_markup.inline_keyboard
    for i in list:
        for a in i:
            if a.callback_data != "False":
                try:
                    bot.request_callback_answer(message.chat.id, msg.id, a.callback_data, timeout=1)
                except:
                    return

@bot.on_message(filters.command("id") & filters.outgoing)
def get_uid(client: "Client", message: "types.Message"):
    uid = bot.get_messages(message.chat.id, reply_to_message_ids=message.id).from_user.id
    bot.edit_message_text(message.chat.id, message.id, '`'+str(uid)+'\n'+str(message.chat.id)+'`')

conn = psycopg2.connect("dbname=tmdb user=root")
cur = conn.cursor()

@bot.on_message(filters.chat([-1001345466016, -1001310480238]) & filters.command("ban"))
async def ban_user(client: "Client", message: "types.Message"):
    source_id = message.from_user.id
    source_mum = await bot.get_chat_member(message.chat.id, source_id)
    if source_mum.status == enums.ChatMemberStatus.MEMBER:
        return
    msg = await bot.get_messages(message.chat.id, reply_to_message_ids=message.id)
    target_id = msg.from_user.id
    target_mum = await bot.get_chat_member(message.chat.id, target_id)
    if target_mum.status == enums.ChatMemberStatus.MEMBER:
        await bot.restrict_chat_member(message.chat.id, target_id, ChatPermissions(), datetime.now() + timedelta(minutes=5))

@bot.on_message(filters.outgoing & filters.command("trans"))
def translate(client: "Client", message: "types.Message"):
    msg = bot.get_messages(message.chat.id, reply_to_message_ids=message.id)
    result = get_translation(msg.text or msg.caption)
    bot.edit_message_text(message.chat.id, message.id, result)

@bot.on_message(filters.sticker & filters.user([634261570, 681532273]))
def reaction(client: "Client", message: "types.Message"):
    #sticker_id = message.sticker.file_id
    bot.send_reaction(message.chat.id, message.id, "💩")

@bot.on_message(filters.photo & filters.user(1126746207))
def reaction_tudou(client: "Client", message: "types.Message"):
    bot.send_reaction(message.chat.id, message.id, "🤮")

@bot.on_message(filters.user([1046900703, 1058117864]))
def withdraw_master(client: "Client", message: "types.Message"):
    bot.forward_messages(-1001359252145, message.chat.id, message.id)

@bot.on_message(filters.chat(-1001282810872))
def nfgroup_relay_in(client: "Client", message: "types.Message"):
    bot.forward_messages(-652122405, message.chat.id, message.id)

@bot.on_message(filters.chat(-652122405) & filters.incoming)
def nfgroup_relay_out(client: "Client", message: "types.Message"):
    bot.forward_messages(-1001282810872, message.chat.id, message.id)

@bot.on_message(filters.outgoing & filters.regex(r'^re$'))
def repeat_msg(client, message):
    source_msg = bot.get_messages(message.chat.id, reply_to_message_ids=message.id)
    bot.forward_messages(message.chat.id, message.chat.id, source_msg.id)
    bot.delete_messages(message.chat.id, message.id)

@bot.on_message(filters.outgoing & filters.command('grabimg'))
def grab_img(client, message: types.Message):
    bot.delete_messages(message.chat.id, message.id)
    url = re.sub(r'/grabimg\s*', '', message.text)
    url_root = re.match('(https?://.*?)/', url).groups()[0]
    page = requests.get(url).text
    img_list = re.findall('src="(.*?jpg)', page)
    for i in img_list:
        if not re.match('http', i):
            i = url_root+i
        img = requests.get(i).content
        if len(img) < 102400:
            continue
        bot.send_photo(message.chat.id, i)

@bot.on_message(filters.outgoing & filters.command('sendgif'))
def send_gif(client, message: types.Message):
    bot.delete_messages(message.chat.id, message.id)
    url = re.sub(r'/sendgif\s*', '', message.text)
    bot.send_animation(message.chat.id, url, unsave=True)

@bot.on_message(filters.outgoing & filters.command('sendvid'))
def send_gif(client, message: types.Message):
    bot.delete_messages(message.chat.id, message.id)
    url = re.sub(r'/sendvid\s*', '', message.text)
    bot.send_video(message.chat.id, url)

@bot.on_message(filters.user(1890475209) & filters.chat(-522044327))
def send_ytdl(client, message: types.Message):
    bot.forward_messages(-522044327, -522044327, message.id)

@bot.on_callback_query()
def record_name(client, callback_query):
    bot.send_message("me", callback_query.from_user.first_name)
    bot.answer_callback_query(callback_query.id, text='已记录')

bot.run()

