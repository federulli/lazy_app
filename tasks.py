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
from torrent_searcher.api import Searcher, Movie as SMovie, Series as SSeries
from configuration import Configuration
from models.db_events import load_listeners
import structlog

logger = structlog.get_logger()

REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")

celery_app = Celery("task", broker=f"redis://{REDIS_HOST}:6379/0")
searcher = Searcher()

load_listeners()


@celery_app.task
def new_movie_task(movie_id):
    config = Configuration()
    movie = Movie.query.get(movie_id)
    logger.msg("Searching for", movie=movie.name)

    movies = [
        SMovie(
            name=movie.name,
            quality=quality,
            year=movie.year,
        )
        for quality in ['1080p', '720p']
    ]
    searcher.search(movies)
    try:
        m = next(m for m in movies if m.magnet is not None)
    except StopIteration:
        logger.msg("not found", movie=movie.name, year=movie.year)
    else:
        torrent = Torrent(
            download_path=config.movie_download_path,
            magnet=m.magnet
        )
        S.add(torrent)
        movie.torrent = torrent
        S.commit()


@celery_app.task
def search_for_not_found_movies():
    config = Configuration()
    movies = Movie.query.filter_by(torrent=None)
    movies_dict = {movie: SMovie(name=movie.name, year=movie.year, quality='1080p') for movie in movies}
    searcher.search(list(movies_dict.values()))
    for movie_orm_instance, movie in movies_dict.items():
        if movie.magnet:
            torrent = Torrent(
                download_path=config.movie_download_path,
                magnet=movie.magnet
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
    series = SSeries(
        name=season.tv_show.name,
        season=season.number,
        episode_count=season.chapter_count,
        quality='720p'
    )

    searcher.search([series])
    for episode, magnet in series.episodes.items():
        if magnet:
            logger.msg("episode found", show_name=season.tv_show.name, season=season.number, number=episode)
            torrent_instance = Torrent(
                magnet=magnet,
                download_path=os.path.join(
                    config.tv_show_download_path,
                    season.tv_show.name,
                    str(season.number)
                )
            )
            chapter = Chapter(
                number=episode,
                torrent=torrent_instance,
                season=season
            )
            S.add(torrent_instance)
            S.add(chapter)
    S.commit()


@celery_app.task
def search_for_not_found_chapters():
    logger.msg("Searching for new chapters")
    config = Configuration()
    not_completed = Season.query.filter_by(completed=False)
    
    seasons_dict = {
        season: SSeries(
            name=season.tv_show.name,
            season=season.number,
            episode_count=season.chapter_count,
            quality='720p'
        ) for season in not_completed
    }

    searcher.search(list(seasons_dict.values()))
    for season, series in seasons_dict.items():
        episode_numbers = set(
            chapter.number
            for chapter in season.chapters
        )
        for episode_number, magnet in series.episodes.items():
            if episode_number in episode_numbers or not magnet:
                continue
            logger.msg(season.tv_show.name, number=episode_number, magnet=magnet)
            torrent_instance = Torrent(
                magnet=magnet,
                download_path=os.path.join(
                    config.tv_show_download_path,
                    season.tv_show.name,
                    str(season.number),
                )
            )
            S.add(torrent_instance)
            chapter = Chapter(
                number=episode_number,
                torrent=torrent_instance,
                season=season
            )
            S.add(chapter)
    S.commit()


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
    for season in Season.query:
        logger.msg("Refreshing chapter count", show=season.tv_show.name, season=season.number)
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
                logger.msg("finished!", show=season.tv_show.name, season=season.number)
                season.completed = True
            else:
                season.completed = False
    S.commit()



@celery_app.task
def test_task():
    print("test task")
