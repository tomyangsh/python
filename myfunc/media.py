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
        self.duration = int(float(info["media"]["track"][0]['Duration']))
        self.width = int(info["media"]["track"][1]['Width'])
        self.height = int(info["media"]["track"][1]['Height'])
        self.fps = info["media"]["track"][1]['FrameRate']
        self.vcode = info["media"]["track"][1]['Format']
        self.vb = round(int(info["media"]["track"][1]['BitRate'])/1000)
        self.acode = info["media"]["track"][2]['Format']
        self.ab = round(int(info["media"]["track"][2]['BitRate'])/1000)
        self.ac = int(info["media"]["track"][2]['Channels'])
        sublist = [track.get('Language') for track in info["media"]["track"] if track["@type"] == "Text"]
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
    ss = ffmpeg.input(file, ss=time or '1:00').output('pipe:', vcodec='png', format='image2', vframes=1).run_async(pipe_stdout=True, quiet=True).communicate()[0]
    return ss

def upload(content: 'bytes'):
    r = requests.post("https://api.imgbb.com/1/upload", data={'key': '314470a578e045760318fd032d9637f7'}, files={'image': content}).json()
    return r['data']['url']

def ytdl(url):
    info = YoutubeDL().extract_info(url, download=False)
    url = [i['url'] for i in info['formats'] if not i.get('container') and i['ext'] == 'mp4'][-1]
    return url
