import os
from videoapp.celery import app
from video.models import (
    Torrent,
    Video,
    Season,
    Chapter,
)

from torrent_searcher.api import Searcher
from qbittorrent_api import delete_completed_torrent
from .tmdb_api import get_chapter_count
from .configuration import Configuration
import structlog

logger = structlog.get_logger()


@app.task(bind=True)
def new_movie_task(self, video_id):
    config = Configuration()
    video = Video.objects.get(pk=video_id)
    logger.msg("Searching for", movie=video.name)
    searcher = Searcher(yts_url=config.yts_url)
    magnet = None
    for quality in ['1080p', '720p']:
        logger.msg(
            "searching",
            movie=video.name,
            quality=quality,
            year=video.year
        )
        try:
            magnet = searcher.search_movie(video.name, quality, video.year)
            logger.msg(
                "found!",
                movie=video.name,
                magnet=magnet,
                quality=quality,
                year=video.year1
            )
            break
        except Exception:
            logger.msg("not found",
                       movie=video.name, quality=quality, year=video.year)
    if not magnet:
        raise Exception("not found {}".format(video.name))

    torrent = Torrent(
        status=Torrent.IN_PROGRESS,
        download_path=config.movie_download_path,
        magnet=magnet
    )
    torrent.save()
    video.torrent = torrent
    video.save()


@app.task(bind=True)
def new_season_task(self, season_id):
    config = Configuration()
    season = Season.objects.get(pk=season_id)
    searcher = Searcher()
    logger.msg(
        "Searching chapters",
        show=season.video.name,
        season=season.number
    )
    torrents_data = searcher.search_for_series(
        season.video.name, season.number, season.chapter_count
    )
    logger.msg(
        "chapters found!",
        show=season.video.name,
        season=season.number,
        total=len(torrents_data.items())
    )
    for number, torrent in torrents_data.items():
        if torrent:
            logger.msg(
                "chapter info",
                show_name=season.video.name,
                season=season.number,
                number=number,
                magnet=torrent
            )
            torrent_instance = Torrent(
                magnet=torrent,
                status=Torrent.IN_PROGRESS,
                download_path=os.path.join(
                    config.tv_show_download_path,
                    season.video.name
                )
            )
            torrent_instance.save()
            chapter = Chapter(
                number=number,
                torrent=torrent_instance,
                season=season
            )
            chapter.save()


@app.task(bind=True)
def search_for_not_found_movies(self=None):
    config = Configuration()
    searcher = Searcher(yts_url=config.yts_url)
    videos = Video.objects.filter(torrent=None, type='MOVIE')
    for video in videos:
        magnet = None
        for quality in ['1080p', '720p']:
            logger.msg(
                "searching",
                movie=video.name,
                quality=quality,
                year=video.year
            )
            try:
                magnet = searcher.search_movie(video.name, quality, video.year)
                logger.msg(
                    "found!",
                    movie=video.name,
                    magnet=magnet,
                    quality=quality,
                    year=video.year
                )
                break
            except Exception:
                logger.msg("not found",
                           movie=video.name, quality=quality, year=video.year)

        if not magnet:
            continue

        torrent = Torrent(
            status=Torrent.IN_PROGRESS,
            download_path=config.movie_download_path,
            magnet=magnet
        )
        torrent.save()
        video.torrent = torrent
        video.save()


@app.task(bind=True)
def search_for_not_found_chapters(self=None):
    logger.msg("Searching for new chapters")
    config = Configuration()
    not_completed = Season.objects.filter(completed=False)
    searcher = Searcher()
    for season in not_completed:
        try:
            logger.msg(
                "Searching",
                show=season.video.name,
                season=season.number
            )
            if not season.chapter_count:
                continue
            chapter_numbers = set(chapter.number
                                  for chapter in season.chapters.all())
            torrents_data = searcher.search_for_series(
                season.video.name, season.number, season.chapter_count
            )
            for number, torrent in torrents_data.items():
                if not torrent or number in chapter_numbers:
                    continue
                logger.msg(season.video.name, number=number, magnet=torrent)
                torrent_instance = Torrent(
                    magnet=torrent,
                    status=Torrent.IN_PROGRESS,
                    download_path=os.path.join(
                        config.tv_show_download_path,
                        season.video.name
                    )
                )
                torrent_instance.save()
                chapter = Chapter(
                    number=number,
                    torrent=torrent_instance,
                    season=season
                )
                chapter.save()
        except Exception as e:
            logger.error(str(e))


@app.task(bind=True)
def download_subtitles(self=None):
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


@app.task(bind=True)
def refresh_chapter_count(self=None):
    not_completed = Season.objects.filter()
    for season in not_completed:
        try:
            logger.msg(
                "Refreshing chapter count",
                show=season.video.name,
                season=season.number
            )
            chapter_numbers = season.chapters.count()
            count = get_chapter_count(season.video.name, season.number)
            if count:
                season.chapter_count = count
                logger.msg(
                    "season status",
                    show=season.video.name,
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
                season.save()
        except Exception as e:
            logger.msg(str(e))


@app.task(bind=True)
def delete_torrents(self=None):
    logger.msg("deleting completed torrents")
    delete_completed_torrent()
