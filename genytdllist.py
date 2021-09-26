import requests, os, re

from bs4 import BeautifulSoup

cookies = {
  "bSession": "6b270150-b078-4181-90c0-41c3ab385f1e|2",
  "hs": "-1462575320",
  "smSession": "JWS.eyJraWQiOiJQSXpvZGJiQiIsImFsZyI6IkhTMjU2In0.eyJkYXRhIjoie1wiaWRcIjpcIjg5MWJjOWNhLTMyMjgtNDczNC05YjAzLWViMThlZWYzMWQ5ZFwiLFwiY29sbGVjdGlvbklkXCI6XCJjYmM1Yjg5OC1lY2QzLTQ0MmEtYTZhNC0wOTVmM2M1ZGQ0ZmVcIixcIm1ldGFTaXRlSWRcIjpcImQ1MjM3NTRhLWYwN2QtNDUxZi05ODhlLTJlZTkxMDA4M2RjOFwiLFwib3duZXJcIjpmYWxzZSxcImNyZWF0aW9uVGltZVwiOjE2MzAxNTg0MDQ2MTAsXCJleHBpcmVzSW5cIjoxMjA5NjAwMDAwLFwiZXhwaXJhdGlvblRpbWVcIjoxNjMxMzY4MDA0NzExLFwibGFzdFJlZnJlc2hlZFwiOjE2MzAyMzYxNDgxNzUsXCJhZG1pblwiOmZhbHNlfSIsImlhdCI6MTYzMDIzNjE0OH0.t0pPudEH3HDhPeqrY1Y5nUiy4Zpmv89LvrD44NKFfLY",
  "svSession": "f5fc02235844f557c89c109f07eec39521741d651c838a04d46fc69146cfc999725cd9bb5b4a5f869feca27d026109641e60994d53964e647acf431e4f798bcda80c8ca0d8c9ff647a7cf3e1585233188a50816aeb72d248f8314c664185a255f26d870b1c634b8c19a1cbb509d4dff010db6760e18b0a88da77fd1e59b1a81c216f254ea2a5b07a763211fe572726b6",
  "XSRF-TOKEN": "1630158386|RtMC1Mnfp7ow"
}
for S in range(3, 4):
    for E in range(35, 50):
        try:
            html = requests.get("https://www.youlucky.biz/video-xtfy/xtfy_"+str(S)+"_"+"%.2d" % E, cookies=cookies).text
            img_link = BeautifulSoup(html, 'html.parser').find(property="og:image")["content"]
            playlist_link = re.sub("thumbnail.*jpg", "playlist.m3u8", img_link)
            print("youtube-dl "+playlist_link+" -o S0"+str(S)+"E"+"%.2d" % E+".mp4")
        except Exception as e:
            print(e)
            break
