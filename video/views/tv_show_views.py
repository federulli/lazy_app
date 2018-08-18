from rest_framework import generics
from ..models import (
    Video,
    Season,
    Torrent,
    Chapter,
)
from ..serializers import (
    VideoSerializer,
    SeasonSerializer,
)
from torrent_searcher.pirate_bay_searcher import PirateBaySearcher
import os


class ListCreateTvShowView(generics.ListCreateAPIView):
    queryset = Video.objects.filter(type='TVSHOW')
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        serializer.save(type='TVSHOW')


class ListCreateSeasonsView(generics.ListCreateAPIView):
    model = Season
    serializer_class = SeasonSerializer

    def get_queryset(self):
        return Season.objects.filter(
            video=Video.objects.get(
                pk=self.kwargs['tv_show_id']
            )
        )

    def perform_create(self, serializer):
        video = Video.objects.get(pk=self.kwargs['tv_show_id'])
        serializer.save(
            video=video
        )
        searcher = PirateBaySearcher('https://thepiratebay.org/')
        torrents_data = searcher.search_for_tv_show(
            video.name, serializer.data['number']
        )
        for number, torrent in torrents_data.items():
            torrent_instance = Torrent(
                        magnet=torrent.magnet_link,
                        status=Torrent.IN_PROGRESS,
                        download_path=os.path.join(
                            video.download_path,
                            video.name
                        )
                    )
            torrent_instance.save()
            chapter = Chapter(
                number=number,
                torrent=torrent_instance,
                season=serializer.instance
            )
            chapter.save()
