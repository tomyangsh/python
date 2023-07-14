import tomllib
import os

from requests import Session

from io import BytesIO

from hashlib import md5

TR_RPC = 'http://127.0.0.1:9092/transmission/rpc/'

s = Session()

def randomhex():
    with open('/dev/urandom', 'rb') as f:
        random_bytes = f.read(64)
    return md5(random_bytes).hexdigest()

def bytesio(content: 'bytes', ext='mp4'):
    file = BytesIO(content)
    file.name = f'file.{ext}'
    return file

def tr_update_headers():
    res = s.get(TR_RPC)
    s.headers.update({'X-Transmission-Session-Id': res.headers['X-Transmission-Session-Id']})

def tr_add_torrent(url):
    res = s.post(TR_RPC, json={"arguments": {"filename": url}, "method": "torrent-add"})
    if res.status_code == 409:
        tr_update_headers()
        tr_add_torrent(url)
    else:
        print(res.json())

def get_apikey(name):
    with open(os.path.expanduser('~/.apikeys'), 'rb') as f:
        data = tomllib.load(f)
        return data.get(name)
