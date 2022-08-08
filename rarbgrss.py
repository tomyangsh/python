import feedparser, re, requests, os

try:
    guid = open(os.path.dirname(__file__)+'/lastfetch', "r").read()
except IOError:
    guid = ''

feed = feedparser.parse('https://rarbg.to/rssdd.php?category=4')

for post in feed.entries:
    if post.guid == guid:
        break
    if re.search('(SexArt|VivThomas|FrolicMe|Hegre|MassageRooms).*1080p', post.title):
        payload = {'jsonrpc': '2.0', 'id': 'qwer', 'method': 'aria2.addUri', 'params': [[post.link]]}
        r = requests.post('http://localhost:6800/jsonrpc', json=payload)

open(os.path.dirname(__file__)+'/lastfetch', "w").write(feed.entries[0].guid)
