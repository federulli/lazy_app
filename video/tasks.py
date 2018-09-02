import os
from videoapp.celery import app
from video.models import (
    Torrent,
    Video,
    Season,
    Chapter,
)
from torrent_searcher.yts_searcher import YTSSearcher
from torrent_searcher.pirate_bay_searcher import PirateBaySearcher
from .configuration import Configuration


@app.task(bind=True)
def new_movie_task(self, video_id):
    config = Configuration()
    print('Request: {0!r}'.format(self.request))
    video = Video.objects.get(pk=video_id)
    try:
        searcher = YTSSearcher(config.yts_url)
        magnet = searcher.search_movie(video.name)
        torrent = Torrent(
            status=Torrent.IN_PROGRESS,
            download_path=config.movie_download_path,
            magnet=magnet
        )
        torrent.save()
        video.torrent = torrent
        video.save()
    except Exception as e:
        print(str(e))


@app.task(bind=True)
def new_season_task(self, season_id):
    config = Configuration()
    season = Season.objects.get(pk=season_id)
    searcher = PirateBaySearcher(config.tpb_url)
    torrents_data = searcher.search_for_tv_show(
        season.video.name, season.number
    )
    print("Torrents found {}".format(len(torrents_data.items())))
    if len(torrents_data.items()) >= season.chapter_count:
        print("Completed")
        season.completed = True
        season.save()
    for number, torrent in torrents_data.items():
        torrent_instance = Torrent(
            magnet=torrent.magnet_link,
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
def search_for_not_found_movies(self):
    config = Configuration()
    searcher = YTSSearcher(config.yts_url)
    videos = Video.objects.filter(torrent=None, type='MOVIE')
    for video in videos:
        try:
            magnet = searcher.search_movie(video.name)
            torrent = Torrent(
                status=Torrent.IN_PROGRESS,
                download_path=config.movie_download_path,
                magnet=magnet
            )
            torrent.save()
            video.torrent = torrent
            video.save()
        except Exception as e:
            print(str(e))


@app.task(bind=True)
def search_for_not_found_chapters(self):
    config = Configuration()
    not_completed = Season.objects.filter(completed=False)
    searcher = PirateBaySearcher(config.tpb_url)
    for season in not_completed:
        chapter_numbers = set(chapter.number
                              for chapter in season.chapters.all())
        torrents_data = searcher.search_for_tv_show(
            season.video.name, season.number
        )
        if len(torrents_data.items()) >= season.chapter_count:
            season.completed = True
            season.save()
        for number, torrent in torrents_data.items():
            if number in chapter_numbers:
                continue
            torrent_instance = Torrent(
                magnet=torrent.magnet_link,
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
def download_subtitles(self):
    from datetime import timedelta

    from babelfish import Language
    from subliminal import download_best_subtitles, region, save_subtitles, scan_videos
    config = Configuration()
    # configure the cache
    region.configure('dogpile.cache.dbm', arguments={'filename': 'cachefile.dbm'})

    # scan for videos newer than 2 weeks and their existing subtitles in a folder
    videos = scan_videos(config.base_download_path, age=timedelta(weeks=2))

    # download best subtitles
    subtitles = download_best_subtitles(videos,
                                        {Language('spa')},
                                        only_one=True)

    # save them to disk, next to the video
    for v in videos:
        save_subtitles(v, subtitles[v], single=True)
