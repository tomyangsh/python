import os, re, time, requests, random, aiocron, psycopg2

from pyrogram import Client, filters
from pyrogram.types import ChatPermissions
from pyrogram.raw import functions, types
from pyrogram.raw.functions.messages import GetFullChat

from io import BytesIO

from itertools import permutations

from random import randint, sample

from time import time as now

app_id = int(os.getenv("APP_ID"))
app_hash = os.getenv("APP_HASH")
tmdb_key = os.getenv("TMDB_KEY")
deepl_key = os.getenv("DEEPL_KEY")

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

group_call = GroupCallFactory(bot).get_file_group_call()

@group_call.on_playout_ended
async def switch_song(_, source):
    group_call.input_filename = music_list[random.randint(0,len(music_list)-1)]

@bot.on_message(filters.chat([-1001345466016, -522044327]) & filters.command("live"))
async def live_music(client, message):
    await bot.send(functions.phone.CreateGroupCall(peer=(await bot.resolve_peer(message.chat.id)), random_id=688968644))
    await asyncio.sleep(1)
    await group_call.start(message.chat.id)

@bot.on_message(filters.chat([-1001345466016, -522044327]) & filters.command("stop"))
async def live_music(_, message):
    await group_call.stop_playout()
    the_call = 688968644
    await bot.send(functions.phone.DiscardGroupCall(call=the_call))
'''
@aiocron.crontab('0 14 * * *')
async def clean():
    msg_list = bot.search_messages(-1001345466016, query="回答正确", from_user=1890475209)
    async for message in msg_list:
        await bot.delete_messages(-1001345466016, message.message_id)
    msg_list = bot.search_messages(-1001345466016, from_user=1788219924)
    async for message in msg_list:
        await bot.delete_messages(-1001345466016, message.message_id)

@aiocron.crontab('0 * * * *')
async def kuo():
    await bot.send_message(-1001222510019, '/kuo')
    time.sleep(3)
    await bot.send_message(-1001310480238, '/kuo')

@aiocron.crontab('58 19 * * *')
async def suo():
    await bot.send_message(-1001222510019, '/suo')

@bot.on_message(filters.command("ans") & filters.outgoing)
def get_uid(client: "Client", message: "types.Message"):
    ori_msg = bot.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
    list = ori_msg.reply_markup.inline_keyboard
    for i in list:
        for a in i:
            if a.callback_data != "False":
                try:
                    bot.request_callback_answer(message.chat.id, ori_msg.message_id, a.callback_data, timeout=1)
                except:
                    return

@bot.on_message(filters.command("id") & filters.outgoing)
def get_uid(client: "Client", message: "types.Message"):
    uid = bot.get_messages(message.chat.id, reply_to_message_ids=message.message_id).from_user.id
    bot.edit_message_text(message.chat.id, message.message_id, '`'+str(uid)+'`')

conn = psycopg2.connect("dbname=tmdb user=root")
cur = conn.cursor()

@bot.on_message(filters.chat([-1001345466016, -522044327]) & filters.command("ban"))
def ban_user(client: "Client", message: "types.Message"):
    source_id = message.from_user.id
    if bot.get_chat_member(message.chat.id, source_id).status == "member":
        return
    msg = bot.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
    target_id = msg.from_user.id
    if bot.get_chat_member(message.chat.id, target_id).status == "member":
        bot.restrict_chat_member(message.chat.id, target_id, ChatPermissions(), int(now() + 300))

@bot.on_message(filters.outgoing & filters.command("trans"))
def translate(client: "Client", message: "types.Message"):
    msg = bot.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
    result = get_translation(msg.text or msg.caption)
    bot.edit_message_text(message.chat.id, message.message_id, result)
'''
@bot.on_message(filters.user(604039549) & filters.regex(r'站点扩容进度: 0.999999999999999'))
def suo(client: "Client", message: "types.Message"):
    bot.send_message(-1001222510019, '/suo')
'''
'''
@bot.on_message(from_users=728062910, pattern=r'.*\n.*\n.*\n\n群内发送关键词'))
def auto_lottery(client: "Client", message: "types.Message"):
    msg = message.text
    key_word = re.sub(r'.*\n.*\n.*\n\n群内发送关键词\s', '', msg)[:-5]
    bot.send_message(message.chat.id, key_word)
'''
@bot.on_message(filters.sticker & filters.user([634261570, 681532273]))
def reaction(client: "Client", message: "types.Message"):
    #sticker_id = message.sticker.file_id
    bot.send_reaction(message.chat.id, message.message_id, "💩")

@bot.on_message(filters.regex(r'^/suo'))
def reaction2(client: "Client", message: "types.Message"):
    bot.send_reaction(message.chat.id, message.message_id, "💩")

@bot.on_message(filters.user([1046900703, 1058117864]))
def withdraw_master(client: "Client", message: "types.Message"):
    bot.forward_messages(-1001359252145, message.chat.id, message.message_id)
'''
@bot.on_message(filters.user(5298809748))
def mxz185(client: "Client", message: "types.Message"):
    bot.send_message(message.chat.id, '小M憋开挂了')


@bot.on_message(filters.user(1381329404))
def reply_inzer(client: "Client", message: "types.Message"):
    msg = message.text
    if not re.match(r'\d\dw$', msg):
        return
    time.sleep(3)
    bot.send_message(message.chat.id, 'tomyang001', reply_to_message_id=message.message_id)
    time.sleep(3)
    bot.send_message(message.chat.id, '谢谢')

@bot.on_message(filters.reply & filters.user(604039549))
def auto_sign_in(client: "Client", message: "types.Message"):
    msg = message.text
    if not re.search(r'新的口令\(5.\)', msg):
        return
    key = re.search(r'/q (.*)', msg).group(1)
    if len(key) > 6:
        return
    keylist = []
    for i in permutations(key):
        keylist.append(''.join(i))
    anwser_list = set(keylist).intersection(titlelist)
    if anwser_list:
        result = next(iter(anwser_list))
        bot.send_message(message.chat.id, '/q '+result)
'''
@bot.on_message(filters.outgoing & filters.regex(r'^re$'))
def repeat_msg(client, message):
    source_msg = bot.get_messages(message.chat.id, reply_to_message_ids=message.message_id)
    bot.forward_messages(message.chat.id, message.chat.id, source_msg.message_id)
    bot.delete_messages(message.chat.id, message.message_id)

@bot.on_message(filters.outgoing & filters.command('grabimg'))
def grab_img(client, message: types.Message):
    bot.delete_messages(message.chat.id, message.message_id)
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
    bot.delete_messages(message.chat.id, message.message_id)
    url = re.sub(r'/sendgif\s*', '', message.text)
    bot.send_animation(message.chat.id, url, unsave=True)

@bot.on_message(filters.outgoing & filters.command('sendvid'))
def send_gif(client, message: types.Message):
    bot.delete_messages(message.chat.id, message.message_id)
    url = re.sub(r'/sendvid\s*', '', message.text)
    bot.send_video(message.chat.id, url)

@bot.on_message(filters.user(1890475209) & filters.chat(-522044327))
def send_ytdl(client, message: types.Message):
    bot.forward_messages(-522044327, -522044327, message.message_id)

bot.run()

