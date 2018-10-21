import schedule
import time
import requests


def refresh(entity_type):
    print("Refreshing: {}".format(entity_type))
    requests.post(
        'http://127.0.0.1:8000/refresh/',
        json={"type": entity_type}
    )


schedule.every().hour.do(lambda: refresh('SUBTITLES'))
schedule.every().day.at("1:00").do(lambda: refresh('MOVIE'))
schedule.every().day.at("2:00").do(lambda: refresh('CHAPTER_COUNT'))
schedule.every().day.at("3:00").do(lambda: refresh('TVSHOW'))
schedule.every().hour.do(lambda: refresh('DELETE_COMPLETED'))

while 1:
    schedule.run_pending()
    time.sleep(1)
