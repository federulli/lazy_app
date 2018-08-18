from rest_framework import generics
from ..models import Video, Torrent
from ..serializers import VideoSerializer
from torrent_searcher.yts_searcher import YTSSearcher


class ListCreateMoviesView(generics.ListCreateAPIView):
    queryset = Video.objects.filter(type='MOVIE')
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        torrent = None
        try:
            searcher = YTSSearcher('https://yts.am/api/v2')
            magnet = searcher.search_movie(serializer.data['name'])
            Torrent(
                status=Torrent.IN_PROGRESS,
                download_path=serializer.data['download_path'],
                magnet=magnet
            ).save()
        except Exception:
            pass
        finally:
            serializer.save(type='MOVIE', torrent=torrent)