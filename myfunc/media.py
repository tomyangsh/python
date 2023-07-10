import subprocess
import requests
import json

from yt_dlp import YoutubeDL

class Video():
    def __init__(self, file):
        info = json.loads(subprocess.run(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file], capture_output=True).stdout.decode())
        self.title = info['format']['tags'].get('title')
        self.size = round(int(info['format']['size'])/(1024 ** 3), 2)
        self.duration = int(float(info['format']['duration']))
        self.width = int(info['streams'][0]['width'])
        self.height = int(info['streams'][0]['height'])
        self.fps = round(eval(info['streams'][0]['r_frame_rate']), 2)
        self.bitrate = int(int(info['format']['bit_rate']) / 1000)
        self.vcode = info['streams'][0]['codec_name']
        self.acode = info['streams'][1]['codec_name']
        self.ab = int(int(info['streams'][1].get('bit_rate') or 1000) / 1000)
        self.ac = info['streams'][1]['channel_layout']
        self.sublist = tuple(i['tags']['language'] for i in info['streams'] if i['codec_type'] == 'subtitle')
        self.zhsub = 'chi' in self.sublist
        self.ensub = 'eng' in self.sublist

def mediainfo(file_path):
    mediainfo = subprocess.run(['mediainfo', file_path], capture_output=True).stdout.decode()
    return mediainfo

def screenshot(file, time: 'str'='1:00') -> 'bytes':
    return subprocess.run(['ffmpeg', '-ss', time, '-i', file, '-c:v', 'png', '-f', 'image2', '-frames:v', '1', 'pipe:'], capture_output=True).stdout

def upload_image(content: 'bytes', host='ccp'):
    if host == 'imgbb':
        r = requests.post('https://api.imgbb.com/1/upload', data={'key': '314470a578e045760318fd032d9637f7'}, files={'image': content}).json()
        return r['data']['url']
    elif host == 'catbox':
        r = requests.post('https://catbox.moe/user/api.php', data={'reqtype': 'fileupload'}, files={'fileToUpload': ('image.png', content)})
        return r.text
    elif host == 'sda1':
        r = requests.post('https://p.sda1.dev/api/v1/upload_external_noform?filename=image.png', data=content).json()
        return r['data']['url']
    elif host == 'imgur':
        r = requests.post('https://api.imgur.com/3/image', headers={"Authorization": "Client-ID dd32dd3c6aaa9a0"}, files={'image': content}).json()
        return r["data"]["link"]
    elif host == 'telegraph':
        r = requests.post("https://telegra.ph/upload", files={'image': content}).json()
        return f"https://telegra.ph{r[0]['src']}"
    elif host == 'ccp':
        r = requests.post("http://up.ccp.ovh/upload/", files={'image.png': content})
    return r.text

def ytdl(url):
    return YoutubeDL(params={'format': 'mp4', 'quiet': True}).extract_info(url, download=False)['url']
