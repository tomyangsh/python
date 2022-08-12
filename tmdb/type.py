import json
import os

from . import method

from country_list import countries_for_language

IMG_BASE = 'https://www.themoviedb.org/t/p/original'
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
    def __init__(self, name, year=None):
        search = method.search_movie(name, year)
        if not search:
            return
        result = search[0]
        self.id = result["id"]
        self.name = result["title"]
        self.ori_name = result["original_title"]
        self.year = result["release_date"][:4]
        self.date = result["release_date"]
        info = method.movie_info(self.id)
        self.des = result["overview"] or info["overview"]
        self.poster = img(result["poster_path"])
        self.backdrop = img(result["backdrop_path"])
        self.score = round(result["vote_average"], 1)
        self.genres = [GENRE_DIC.get(str(k)) for k in result["genre_ids"]]
        self.lang = LANG.get(result["original_language"])
        self.country = [dict(countries_for_language('zh_CN')).get(k) for k in (i.get("iso_3166_1") for i in info.get('production_countries'))]
        self.runtime = info["runtime"]
        self.imdb = info["imdb_id"]
        credits = method.movie_credits(self.id)
        self.director = [p.get("name") for p in credits['crew'] if p.get('job') == 'Director']
        self.cast = [{'id': p.get('id'), 'name': p.get('name'), 'character': p.get('character'), 'img': img(p["profile_path"])} for p in credits['cast']]

    def trailer(self):
        return f'{YT_BASE}{method.movie_trailer(self.id)}'

    def __str__(self):
        return f'{self.name} ({self.year})'

class TV():
    def __init__(self, name, year=None):
        search = method.search_tv(name, year)
        if not search:
            return
        result = search[0]
        self.id = result["id"]
        self.name = result["name"]
        self.ori_name = result["original_name"]
        self.year = result["first_air_date"][:4]
        self.date = result["first_air_date"]
        info = method.tv_info(self.id)
        self.des = result["overview"] or info["overview"]
        self.network = [n.get("name") for n in info["networks"]]
        self.poster = img(result["poster_path"])
        self.seasons = [{'season': s["season_number"], 'eps': s["episode_count"], 'date': s["air_date"], 'poster': img(s["poster_path"])} for s in info["seasons"]]
        if self.seasons:
            self.poster_latest = [s['poster'] for s in self.seasons if s['poster']][-1]
        self.backdrop = img(result["backdrop_path"])
        self.score = round(result["vote_average"], 1)
        self.genres = [GENRE_DIC.get(str(k)) for k in result["genre_ids"]]
        self.lang = LANG.get(result["original_language"])
        self.country = [dict(countries_for_language('zh_CN')).get(k) for k in result["origin_country"]]
        self.runtime = info["episode_run_time"]
        self.imdb = method.tv_imdb(self.id)
        credits = method.tv_credits(self.id)
        self.creator = [p.get("name") for p in info["created_by"]]
        self.cast = [{'id': p.get('id'), 'name': p.get('name'), 'character': p.get('character'), 'img': img(p["profile_path"])} for p in credits['cast']]
        if info['next_episode_to_air']:
            self.next = {'season': info['next_episode_to_air']['season_number'], 'episode': info['next_episode_to_air']['episode_number'], 'date': info['next_episode_to_air']['air_date']}
        self.satus = STATUS_DIC.get(info["status"])
        self.season = info["number_of_seasons"]

    def trailer(self):
        return f'{YT_BASE}{method.tv_trailer(self.id)}'

    def __str__(self):
        return f'{self.name} ({self.year})'

class Person():
    def __init__(self, name):
        search = method.search_person(name)
        if not search:
            return
        result = search[0]
        self.id = result["id"]
        self.name = result["name"]
        self.img = img(result["profile_path"])
        self.aworks = []
        for w in result["known_for"]:
            if w["media_type"] == "movie":
                self.aworks.append({'type': 'movie', 'id': w['id'], 'name': w['title'], 'year': w['release_date'][:4], 'poster': img(w['poster_path'])})
            else:
                self.aworks.append({'type': 'tv', 'id': w['id'], 'name': w['name'], 'year': w['first_air_date'][:4], 'poster': img(w['poster_path'])})
        info = method.person_info(self.id)
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
        rworks.sort(reverse=True, key=get_year)
        return rworks

    def __str__(self):
        return f'{self.name}'
