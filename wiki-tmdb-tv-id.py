import requests, time

S = requests.Session()

URL = "https://www.wikidata.org/w/api.php"

PARAMS_0 = {
    'action':"query",
    'meta':"tokens",
    'type':"login",
    'format':"json"
}

R = S.get(url=URL, params=PARAMS_0)
DATA = R.json()

LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

print(LOGIN_TOKEN)

PARAMS_1 = {
    'action':"login",
    'lgname':"tomyang001",
    'lgpassword':"Quzpu1-fotjit-jixcud",
    'lgtoken':LOGIN_TOKEN,
    'format':"json"
}

R = S.post(URL, data=PARAMS_1)
DATA = R.json()

print(DATA)

PARAMS_2 = {
    'action':"query",
    'meta':"tokens",
    'format':"json"
}

R = S.get(url=URL, params=PARAMS_2)
DATA = R.json()

TOKEN = DATA['query']['tokens']['csrftoken']
print(TOKEN)

for tmdb_id in range(126350, 150000):
    imdb_id = requests.get("https://api.themoviedb.org/3/tv/{}/external_ids?api_key=b729fb42b650d53389fb933b99f4b072".format(tmdb_id)).json().get('imdb_id', '')
    if imdb_id:
        value = '"'+str(tmdb_id)+'"'
        result = requests.get('https://www.wikidata.org/w/api.php?action=query&format=json&list=search&srsearch=haswbstatement%3A%22P345%3D{}%22'.format(imdb_id)).json().get('query').get('search')
        if result:
            wiki_id = result[0].get('title')
            check = requests.get('https://www.wikidata.org/w/api.php?action=wbgetclaims&format=json&entity={}&property=P4983'.format(wiki_id)).json().get('claims')
            if not check:
                R = S.post(URL, data={'action':"wbcreateclaim", 'format':"json", 'entity':wiki_id, 'snaktype':"value", 'property':"P4983", 'value':value, 'token':TOKEN})
                print(R.text)
                print(tmdb_id)
#                time.sleep(0.6)

