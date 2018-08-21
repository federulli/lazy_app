import os
from videoapp.celery import app
from video.models import Torrent, Video, Season, Chapter
from torrent_searcher.yts_searcher import YTSSearcher
from torrent_searcher.pirate_bay_searcher import PirateBaySearcher


@app.task(bind=True)
def new_movie_task(self, video_id):
    print('Request: {0!r}'.format(self.request))
    video = Video.objects.get(pk=video_id)
    try:
        searcher = YTSSearcher('https://yts.am/api/v2')
        magnet = searcher.search_movie(video.name)
        torrent = Torrent(
            status=Torrent.IN_PROGRESS,
            download_path=video.download_path,
            magnet=magnet
        )
        torrent.save()
        video.torrent = torrent
        video.save()
    except Exception as e:
        print(str(e))


@app.task(bind=True)
def new_season_task(self, season_id):
    season = Season.objects.get(pk=season_id)
    searcher = PirateBaySearcher('https://thepiratebay.org/')
    torrents_data = searcher.search_for_tv_show(
        season.video.name, season.number
    )
    if len(torrents_data.items()) >= season.chapter_count:
        season.completed = True
    for number, torrent in torrents_data.items():
        torrent_instance = Torrent(
            magnet=torrent.magnet_link,
            status=Torrent.IN_PROGRESS,
            download_path=os.path.join(
                season.video.download_path,
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
    searcher = YTSSearcher('https://yts.am/api/v2')
    videos = Video.objects.filter(torrent=None, type='MOVIE')
    for video in videos:
        try:
            magnet = searcher.search_movie(video.name)
            torrent = Torrent(
                status=Torrent.IN_PROGRESS,
                download_path=video.download_path,
                magnet=magnet
            )
            torrent.save()
            video.torrent = torrent
            video.save()
        except Exception as e:
            print(str(e))


@app.task(bind=True)
def search_for_not_found_chapters(self):
    not_completed = Season.objects.filter(completed=False)
    searcher = PirateBaySearcher('https://thepiratebay.org/')
    for season in not_completed:
        chapter_numbers = set(chapter.number
                              for chapter in season.chapters.all())
        torrents_data = searcher.search_for_tv_show(
            season.video.name, season.number
        )
        if len(torrents_data.items()) >= season.chapter_count:
            season.completed = True
        for number, torrent in torrents_data.items():
            if number in chapter_numbers:
                continue
            torrent_instance = Torrent(
                magnet=torrent.magnet_link,
                status=Torrent.IN_PROGRESS,
                download_path=os.path.join(
                    season.video.download_path,
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
