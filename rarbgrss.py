import feedparser, re, requests, os

guid = open('/opt/dev/guid', "r").read()

feed = feedparser.parse('https://rarbg.to/rssdd.php?category=4')

for post in feed.entries:
    if post.guid == guid:
        break
    if re.search('(SexArt|VivThomas|FrolicMe|Hegre).*1080p', post.title):
        print(post.title)
        print(post.link)
        payload = {'jsonrpc': '2.0', 'id': 'qwer', 'method': 'aria2.addUri', 'params': [[post.link]]}
        r = requests.post('http://localhost:6800/jsonrpc', json=payload)
        print(r.text)

open('/opt/dev/guid', "w").write(feed.entries[0].guid)
