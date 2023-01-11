import subprocess
import requests
import ffmpeg
import json

from yt_dlp import YoutubeDL

from io import BytesIO

class Video():
    def __init__(self, file):
        info = json.loads(subprocess.Popen(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file], stdout=subprocess.PIPE).communicate()[0].decode())
        self.title = info['format']['tags'].get('title')
        self.size = round(int(info['format']['size'])/(1024 ** 3), 2)
        self.duration = int(float(info['format']['duration']) / 60)
        self.width = int(info['streams'][0]['width'])
        self.height = int(info['streams'][0]['height'])
        self.fps = round(eval(info['streams'][0]['r_frame_rate']), 2)
        self.bitrate = int(int(info['format']['bit_rate']) / 1000)
        self.vcode = info['streams'][0]['codec_name']
        self.acode = info['streams'][1]['codec_name']
        self.ab = int(int(info['streams'][1]['bit_rate']) / 1000)
        self.ac = info['streams'][1]['channel_layout']
        self.sublist = tuple(i['tags']['language'] for i in info['streams'] if i['codec_type'] == 'subtitle')
        self.zhsub = 'chi' in self.sublist
        self.ensub = 'eng' in self.sublist

def bytesio(content: 'bytes', ext='mp4'):
    f = BytesIO(content)
    f.name = f'file.{ext}'
    return f

def mediainfo(file_path):
    mediainfo = subprocess.Popen(['mediainfo', file_path], stdout=subprocess.PIPE).communicate()[0].decode()
    return mediainfo

def ss(file, time: 'str'=None) -> 'bytes':
    ss = ffmpeg.input(file, ss=time or '1:00').output('pipe:', vcodec='png', format='image2', vframes=1, vf='scale=w=iw*sar:h=ih').run_async(pipe_stdout=True, quiet=True).communicate()[0]
    return ss

def upload(content: 'bytes'):
    r = requests.post('https://api.imgbb.com/1/upload', data={'key': '314470a578e045760318fd032d9637f7'}, files={'image': content}).json()
    return r['data']['url']

def ytdl(url):
    return YoutubeDL(params={'format': 'mp4', 'quiet': True}).extract_info(url, download=False)['url']
