import subprocess
import requests
import ffmpeg
import json

from yt_dlp import YoutubeDL

from io import BytesIO

class Video():
    def __init__(self, file):
        info = json.loads(subprocess.Popen(["mediainfo", "--Output=JSON", file], stdout=subprocess.PIPE).communicate()[0].decode())
        self.size = round(int(info["media"]["track"][0]['FileSize'])/(1024 ** 3), 2)
        self.duration = round(float(info["media"]["track"][0]['Duration'])/60)
        self.vcode = info["media"]["track"][1]['Format']
        self.vb = round(int(info["media"]["track"][1]['BitRate'])/1000)
        self.acode = info["media"]["track"][2]['Format']
        self.ab = round(int(info["media"]["track"][2]['BitRate'])/1000)
        sublist = [track['Language'] for track in info["media"]["track"] if track["@type"] == "Text"]
        self.zhsub = 'zh' in sublist
        self.ensub = 'en' in sublist

def bytesio(content: 'bytes', ext='mp4'):
    f = BytesIO(content)
    f.name = f'file.{ext}'
    return f

def mediainfo(file_path):
    mediainfo = subprocess.Popen(["mediainfo", file_path], stdout=subprocess.PIPE).communicate()[0].decode()
    return mediainfo

def ss(file, time: 'str'=None) -> 'bytes':
    ss = ffmpeg.input(file, ss=time or '1:00').output('pipe:', format='image2', vframes=1).run_async(pipe_stdout=True, quiet=True).communicate()[0]
    return ss

def upload(content: 'bytes', name='img.png'):
    r = requests.post("http://up.ccp.ovh/upload/", files={name: content})
    return r.text

def ytdl_audio(url):
    info = YoutubeDL().extract_info(url, download=False)
    url = [i['url'] for i in info['formats'] if i['ext'] == 'm4a'][-1]
    return url

def ytdl(url):
    info = YoutubeDL().extract_info(url, download=False)
    url = [i['url'] for i in info['formats'] if i['ext'] == 'mp4'][-1]
    return url
