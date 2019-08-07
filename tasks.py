import os
from celery import Celery

from tmdb_api import get_chapter_count
from models import (
    S,
    Movie,
    Torrent,
    Season,
    Chapter,
)
from qbittorrent_api import delete_completed_torrent
from torrent_searcher.api import Searcher
from configuration import Configuration
from models.db_events import load_listeners
import structlog

logger = structlog.get_logger()

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")

celery_app = Celery("task", broker=f"redis://{REDIS_HOST}:6379/0")


load_listeners()


@celery_app.task
def new_movie_task(movie_id):
    config = Configuration()
    movie = Movie.query.get(movie_id)
    logger.msg("Searching for", movie=movie.name)
    searcher = Searcher(yts_url=config.yts_url)
    magnet = None
    for quality in ['1080p', '720p']:
        logger.msg(
            "searching",
            movie=movie.name,
            quality=quality,
            year=movie.year
        )
        try:
            magnet = searcher.search_movie(
                movie.name, quality, movie.year
            )
            logger.msg(
                "found!",
                movie=movie.name,
                magnet=magnet,
                quality=quality,
                year=movie.year
            )
            break
        except Exception:
            logger.msg(
                "not found",
                movie=movie.name,
                quality=quality,
                year=movie.year
            )
    if not magnet:
        raise Exception("not found {}".format(movie.name))

    torrent = Torrent(
        download_path=config.movie_download_path,
        magnet=magnet
    )
    S.add(torrent)
    movie.torrent = torrent
    S.commit()


@celery_app.task
def new_season_task(season_id):
    config = Configuration()
    season = Season.query.get(season_id)
    season.chapter_count = get_chapter_count(
        season.tv_show.name,
        season.number
    )
    searcher = Searcher()
    logger.msg(
        "Searching chapters",
        show=season.tv_show.name,
        season=season.number
    )
    torrents_data = searcher.search_for_series(
        season.tv_show.name, season.number, season.chapter_count
    )
    logger.msg(
        "chapters found!",
        show=season.tv_show.name,
        season=season.number,
        total=len(torrents_data.items())
    )
    for number, torrent in torrents_data.items():
        if torrent:
            logger.msg(
                "chapter info",
                show_name=season.tv_show.name,
                season=season.number,
                number=number,
                magnet=torrent
            )
            torrent_instance = Torrent(
                magnet=torrent,
                download_path=os.path.join(
                    config.tv_show_download_path,
                    season.tv_show.name,
                    str(season.number)
                )
            )
            chapter = Chapter(
                number=number,
                torrent=torrent_instance,
                season=season
            )
            S.add(torrent_instance)
            S.add(chapter)
            S.commit()


@celery_app.task
def search_for_not_found_movies():
    config = Configuration()
    searcher = Searcher(yts_url=config.yts_url)
    movies = Movie.query.filter_by(torrent=None)
    for movie in movies:
        magnet = None
        for quality in ('1080p', '720p'):
            logger.msg(
                "searching",
                movie=movie.name,
                quality=quality,
                year=movie.year
            )
            try:
                magnet = searcher.search_movie(
                    movie.name, quality, movie.year)
                logger.msg(
                    "found!",
                    movie=movie.name,
                    magnet=magnet,
                    quality=quality,
                    year=movie.year
                )
                break
            except Exception:
                logger.msg(
                    "not found",
                    movie=movie.name,
                    quality=quality,
                    year=movie.year
                )

        if not magnet:
            continue

        torrent = Torrent(
            download_path=config.movie_download_path,
            magnet=magnet
        )
        S.add(torrent)
        movie.torrent = torrent
        S.commit()


@celery_app.task
def search_for_not_found_chapters():
    logger.msg("Searching for new chapters")
    config = Configuration()
    not_completed = Season.query.filter_by(completed=False)
    searcher = Searcher()
    for season in not_completed:
        try:
            logger.msg(
                "Searching",
                show=season.tv_show.name,
                season=season.number
            )
            if not season.chapter_count:
                continue
            chapter_numbers = set(
                chapter.number
                for chapter in season.chapters
            )
            torrents_data = searcher.search_for_series(
                season.tv_show.name, season.number, season.chapter_count
            )
            for number, torrent in torrents_data.items():
                if not torrent or number in chapter_numbers:
                    continue
                logger.msg(season.tv_show.name, number=number, magnet=torrent)
                torrent_instance = Torrent(
                    magnet=torrent,
                    download_path=os.path.join(
                        config.tv_show_download_path,
                        season.tv_show.name,
                        str(season.number),
                    )
                )
                S.add(torrent_instance)
                chapter = Chapter(
                    number=number,
                    torrent=torrent_instance,
                    season=season
                )
                S.add(chapter)
                S.commit()
        except Exception as e:
            logger.error(str(e))


@celery_app.task
def download_subtitles():
    logger.msg("Searching for subtitles")
    from datetime import timedelta

    from babelfish import Language
    from subliminal import download_best_subtitles, region, save_subtitles, scan_videos
    config = Configuration()
    # configure the cache
    region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})

    # scan for videos newer than 2 weeks and their existing subtitles in a folder
    videos = scan_videos(config.base_download_path, age=timedelta(days=1))

    # download best subtitles
    subtitles = download_best_subtitles(videos,
                                        {Language('spa')},
                                        only_one=True)

    # save them to disk, next to the video
    for v in videos:
        save_subtitles(v, subtitles[v], single=True)


@celery_app.task
def refresh_chapter_count():
    not_completed = Season.query.all()
    for season in not_completed:
        try:
            logger.msg(
                "Refreshing chapter count",
                show=season.tv_show.name,
                season=season.number
            )
            chapter_numbers = len(season.chapters)
            count = get_chapter_count(season.tv_show.name, season.number)
            if count:
                season.chapter_count = count
                logger.msg(
                    "season status",
                    show=season.tv_show.name,
                    season=season.number,
                    downloaded=chapter_numbers,
                    total=count
                )
                if chapter_numbers == count:
                    logger.msg(
                        "finished!",
                        show=season.video.name,
                        season=season.number
                    )
                    season.completed = True
                else:
                    season.completed = False
                S.commit()
        except Exception as e:
            logger.msg(str(e))


@celery_app.task
def delete_torrents():
    logger.msg("deleting completed torrents")
    delete_completed_torrent()


@celery_app.task
def test_task():
    print("test task")
