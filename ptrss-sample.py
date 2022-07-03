import requests, feedparser, datetime, json, os

old_list = json.load(open(os.path.dirname(__file__)+'/ptrss.db', "r")) #请先在同一目录下执行'touch ptrss.db'以确保该文件存在
new_list = []
link = ''

def update(sitename, url):
    r = feedparser.parse(url)
    if not r.entries[0].guid in old_list:
        link = r.entries[0].enclosures[0].href
    new_list.extend(list(i.guid for i in r.entries))

update("site3", "https://site3.com/torrentrss.php?xxxx")

update("site2", "https://site2.com/torrentrss.php?xxxx")

update("site1", "https://site1.com/torrentrss.php?xxxx") #站点越靠下，优先级越高

json.dump(new_list, open(os.path.dirname(__file__)+'/ptrss.db', "w"))

url = "http://localhost:9091/transmission/rpc" #注意端口是否为9091
r = requests.get(url)
headers = {"X-Transmission-Session-Id": r.headers['X-Transmission-Session-Id']}

data = '{"arguments": {"fields": ["id", "status", "doneDate"]}, "method": "torrent-get"}'
r = requests.post(url, data=data, headers=headers).json()
ids = []
for i in r['arguments']['torrents']:
    if i['status'] == 4:
        exit()
    if i['status'] == 0:
        continue
    if (datetime.datetime.now().timestamp() - i["doneDate"]) > 3600 * 24 * 7: #保种天数
        ids.append(i['id'])
if ids:
    data = '{"arguments": {"ids": '+str(ids)+', "delete-local-data": true}, "method": "torrent-remove"}'
    r = requests.post(url, data=data, headers=headers).json()

data = '{"arguments": {"path": "/path/to/download/directory/"}, "method": "free-space"}' #path改成下载目录路径
r = requests.post(url, data=data, headers=headers).json()
if r['arguments']['size-bytes']/1024/1024/1024 <= 200:
    exit()

if link:
    torrentAdd =  '{"arguments": {"filename": "'+link+'"}, "method": "torrent-add"}'
    r = requests.post(url, data=torrentAdd, headers=headers).json()
