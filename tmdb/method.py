import requests

HEADERS = {
        'User-Agent': 'Kodi Movie scraper by Team Kodi',
        'Accept': 'application/json'
        }
URL_BASE = 'https://api.themoviedb.org/3/'

PARAMS_BASE = {'api_key': 'f090bb54758cabf231fb605d3e3e0468'}
LANG = 'zh-CN'

def results_handler(result, type=None):
    result_list = []
    for i in result['results']:
        if not type:
            type = i['media_type']
        id = i['id']
        name = i.get('title') or i.get('name')
        date = i.get('release_date') or i.get('first_air_date') or ''
        img = i.get('poster_path') or i.get('profile_path')
        des = i.get('overview')
        result_list.append({'type': type, 'id': id, 'name': name, 'year': date[:4], 'img': img, 'des': des})
    return result_list

def discover(type='movie'):
    url = f'{URL_BASE}discover/{type}'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    result = requests.get(url, headers=HEADERS, params=params).json()
    return results_handler(result, type)

def multi_search(query):
    url = f'{URL_BASE}search/multi'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    params.update({'query': query, 'include_adult': 'true'})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return results_handler(result)

def search_movie(query, year=None):
    url = f'{URL_BASE}search/movie'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    params.update({'query': query, 'primary_release_year': year, 'include_adult': 'true'})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return results_handler(result, 'movie')

def search_tv(query, year=None):
    url = f'{URL_BASE}search/tv'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    params.update({'query': query, 'first_air_date_year': year})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return results_handler(result, 'tv')

def search_person(query):
    url = f'{URL_BASE}search/person'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
    params.update({'query': query})
    result = requests.get(url, headers=HEADERS, params=params).json()
    return results_handler(result, 'person')

def movie_info(id):
    url = f'{URL_BASE}movie/{id}'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
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

def movie_release(id):
    url = f'{URL_BASE}movie/{id}/release_dates'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result["results"]

def movie_translation(id):
    url = f'{URL_BASE}movie/{id}/translations'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result["translations"]

def tv_info(id):
    url = f'{URL_BASE}tv/{id}'
    params = PARAMS_BASE.copy()
    params['language'] = LANG
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
    params['language'] = LANG
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result

def person_external_ids(id):
    url = f'{URL_BASE}person/{id}/external_ids'
    params = PARAMS_BASE.copy()
    result = requests.get(url, headers=HEADERS, params=params).json()
    return result
