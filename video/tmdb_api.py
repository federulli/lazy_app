import requests
from distutils.util import strtobool

TMDB_API_KEY = "bab91183b96f933bd5b39f31a64e7164"
OMDB_API_KEY = "8a90e315"


def get_imdb_id(name):
    r = requests.get("http://www.omdbapi.com/?t={}&apikey=8a90e315".format(name))
    r.raise_for_status()
    if not strtobool(r.json()["Response"]):
        raise Exception("{} Doesn't exists")
    return r.json()["imdbID"][2:]


def get_tmdb_id(name):
    imdb_id = get_imdb_id(name)
    url = ("https://api.themoviedb.org/3/find/tt{}?api_key={}"
           "&language=en-US&external_source=imdb_id").format(
        imdb_id, TMDB_API_KEY)
    r = requests.get(url)
    r.raise_for_status()
    return next(iter(r.json()['tv_results']), {}).get('id')


def get_chapter_count(name, season):
    id = get_tmdb_id(name)
    r = requests.get(
        ("https://api.themoviedb.org/3/tv/{}/season/"
         "{}?api_key={}&language=en-US").format(id, season, TMDB_API_KEY)
    )
    r.raise_for_status()
    return len(r.json()['episodes'])
