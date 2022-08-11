import requests

HEADERS = {
        'User-Agent': 'Kodi Movie scraper by Team Kodi',
        'Accept': 'application/json'
        }
URL_BASE = 'https://api.themoviedb.org/3/'

PARAMS_BASE = {'api_key': 'f090bb54758cabf231fb605d3e3e0468'}

def search_movie(query, year=None):
    url = f'{URL_BASE}search/movie'
    params = PARAMS_BASE.copy()
    params.update({'query': query, 'primary_release_year': year, 'include_adult': 'true', 'language': 'zh-CN'})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result['results']

def search_tv(query, year=None):
    url = f'{URL_BASE}search/tv'
    params = PARAMS_BASE.copy()
    params.update({'query': query, 'first_air_date__year': year, 'language': 'zh-CN'})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result['results']

def search_person(query, year=None):
    url = f'{URL_BASE}search/person'
    params = PARAMS_BASE.copy()
    params.update({'query': query, 'primary_release_year': year, 'language': 'zh-CN'})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result['results']

def movie_info(id):
    url = f'{URL_BASE}movie/{id}'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def movie_trailer(id):
    url = f'{URL_BASE}movie/{id}/videos'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    key = next((i["key"] for i in result["results"] if i["site"] == "YouTube" and i["type"] == "Trailer"), None)
    return key

def movie_credits(id):
    url = f'{URL_BASE}movie/{id}/credits'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def movie_backdrops(id):
    url = f'{URL_BASE}movie/{id}/images'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result["backdrops"]

def tv_info(id):
    url = f'{URL_BASE}tv/{id}'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def tv_imdb(id):
    url = f'{URL_BASE}tv/{id}/external_ids'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result.get("imdb_id")

def tv_trailer(id):
    url = f'{URL_BASE}tv/{id}/videos'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    key = next((i["key"] for i in result["results"] if i["site"] == "YouTube" and i["type"] == "Trailer"), None)
    return key

def tv_credits(id):
    url = f'{URL_BASE}tv/{id}/credits'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def tv_backdrops(id):
    url = f'{URL_BASE}tv/{id}/images'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result["backdrops"]

def person_info(id):
    url = f'{URL_BASE}person/{id}'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def person_credits(id):
    url = f'{URL_BASE}person/{id}/combined_credits'
    params = PARAMS_BASE.copy()
    params.update({'language': 'zh-CN'})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result
