import requests


def get_chapter_count(show_name, season):
    try:
        url = 'http://www.omdbapi.com/?t={}&season={}&apikey=8a90e315'.format(
            show_name, season
        )
        r = requests.get(url)
        return len(r.json()['Episodes'])
    except:
        return 0
