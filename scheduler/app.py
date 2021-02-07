import time
import schedule
import structlog

from queries import (
    client,
    SEARCH_MOVIES_MUTATION,
    SEARCH_EPISODES_MUTATION,
    DELETE_COMPLETED_TORRENTS_MUTATION,
    RELOAD_CHAPTER_COUNT_MUTATION,
    DELETE_ALL_TORRENTS_MUTATION,
) 

logger = structlog.get_logger()


def refresh(action):
    try:
        client.execute(action)
    except Exception as e:
        message = str(e)
        logger.exception('ERROR refreshing',
                         exc_info=True)
    else:
        logger.info("OK")

#schedule.every().hour.do(lambda: refresh('SUBTITLES'))
schedule.every().day.at("01:00").do(lambda: refresh(SEARCH_MOVIES_MUTATION))
schedule.every().day.at("02:00").do(lambda: refresh(RELOAD_CHAPTER_COUNT_MUTATION))
schedule.every().day.at("03:00").do(lambda: refresh(SEARCH_EPISODES_MUTATION))
schedule.every().hour.do(lambda: refresh(DELETE_COMPLETED_TORRENTS_MUTATION))

while 1:
    schedule.run_pending()
    time.sleep(1)
