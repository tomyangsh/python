import json
import os
import re

from . import method

from country_list import countries_for_language

IMG_BASE = 'https://image.tmdb.org/t/p/original'
YT_BASE = 'https://www.youtube.com/watch?v='
GENRE_DIC = json.load(open(os.path.dirname(__file__)+'/genre.json'))
LANG = json.load(open(os.path.dirname(__file__)+'/lang.json'))
GENDER_DIC = {0: None, 1: '女', 2: '男', 3: 'Non-binary'}
STATUS_DIC = {
        'Returning Series': '在播',
        'Ended': '完结',
        'Canceled': '被砍',
        'In Production': '拍摄中'
        }

def get_year(dic):
    return dic["year"]

def img(path):
    if not path:
        return None
    return f'{IMG_BASE}{path}'

class Movie():
    def __init__(self, id):
        info = method.movie_info(id)
        if info.get('success') == False:
            self.ok = False
            return
        else:
            self.ok = True
        self.id = id
        self.name = info["title"]
        self.ori_name = info["original_title"]
        self.year = info["release_date"][:4]
        self.date = info["release_date"]
        self.des = info["overview"]
        if not self.des:
            trans = method.movie_translation(id)
            trans = (i["data"]["overview"] for i in trans if i["name"] == "English")
            self.des = next(trans, '')
        self.poster = img(info["poster_path"])
        self.backdrop = img(info["backdrop_path"])
        self.score = round(info["vote_average"], 1)
        self.genres = [GENRE_DIC.get(str(g["id"])) for g in info["genres"]]
        self.lang = LANG.get(info["original_language"])
        self.country = [dict(countries_for_language('zh_CN')).get(k) for k in (i.get("iso_3166_1") for i in info.get('production_countries'))]
        self.runtime = info["runtime"]
        self.imdb = info["imdb_id"]
        credits = method.movie_credits(id)
        self.director = [p.get("name") for p in credits['crew'] if p.get('job') == 'Director']
        self.cast = [{'id': p.get('id'), 'name': p.get('name'), 'character': p.get('character'), 'img': img(p["profile_path"])} for p in credits['cast']]
        trailer = method.movie_trailer(id)
        if trailer:
            self.trailer = f'{YT_BASE}{trailer}'
        else:
            self.trailer = None
        self.release = method.movie_release(id)

class TV():
    def __init__(self, id):
        info = method.tv_info(id)
        self.id = id
        self.name = info["name"]
        self.ori_name = info["original_name"]
        self.year = info["first_air_date"][:4]
        self.date = info["first_air_date"]
        self.des = info["overview"]
        self.network = [n.get("name") for n in info["networks"]]
        self.poster = img(info["poster_path"])
        self.seasons = [{'season': s["season_number"], 'eps': s["episode_count"], 'date': s["air_date"], 'poster': img(s["poster_path"])} for s in info["seasons"]]
        if self.seasons:
            postlist = [s['poster'] for s in self.seasons if s['poster']]
            if postlist:
                self.poster_latest = postlist[-1]
            else:
                self.poster_latest = None
        self.backdrop = img(info["backdrop_path"])
        self.score = round(info["vote_average"], 1)
        self.genres = [GENRE_DIC.get(str(g["id"])) for g in info["genres"]]
        self.lang = LANG.get(info["original_language"])
        self.country = [dict(countries_for_language('zh_CN')).get(k) for k in info["origin_country"]]
        self.runtime = info["episode_run_time"]
        self.imdb = method.tv_imdb(self.id)
        credits = method.tv_credits(self.id)
        self.creator = [p.get("name") for p in info["created_by"]]
        self.cast = [{'id': p.get('id'), 'name': p.get('name'), 'character': p.get('character'), 'img': img(p["profile_path"])} for p in credits['cast']]
        if info['next_episode_to_air']:
            self.next = {'season': info['next_episode_to_air']['season_number'], 'episode': info['next_episode_to_air']['episode_number'], 'date': info['next_episode_to_air']['air_date']}
        else:
            self.next = None
        self.status = STATUS_DIC.get(info["status"])
        self.season = info["number_of_seasons"]
        trailer = method.tv_trailer(id)
        if trailer:
            self.trailer = f'{YT_BASE}{method.tv_trailer(id)}'
        else:
            self.trailer = None

class Person():
    def __init__(self, id):
        info = method.person_info(id)
        self.id = id
        self.name = info["name"]
        self.img = img(info["profile_path"])
        self.birthday = info["birthday"]
        self.deathday = info["deathday"]
        self.gender = GENDER_DIC.get(info["gender"])
        self.place_of_birth = info["place_of_birth"]
        self.known_for_department = info["known_for_department"]

    def rworks(self):
        if self.known_for_department == "Acting":
            wlist = method.person_credits(self.id)["cast"]
        else:
            wlist = [w for w in method.person_credits(self.id)["crew"] if w["department"] == self.known_for_department]
        rworks = []
        for w in wlist:
            if w["media_type"] == "movie":
                rworks.append({'type': 'movie', 'id': w['id'], 'name': w['title'], 'year': w['release_date'][:4], 'poster': img(w['poster_path'])})
            else:
                rworks.append({'type': 'tv', 'id': w['id'], 'name': w['name'], 'year': w['first_air_date'][:4], 'poster': img(w['poster_path'])})
        rworks = [dict(t) for t in {tuple(d.items()) for d in rworks}]
        rworks.sort(reverse=True, key=get_year)
        return rworks

    def __str__(self):
        return f'{self.name}'
