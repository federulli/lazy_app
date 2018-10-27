from rest_framework import generics
from ..models import (
    Video,
    Season,
)
from ..serializers import (
    VideoSerializer,
    SeasonSerializer,
)
from ..tasks import new_season_task
from ..tmdb_api import get_chapter_count


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
            video=video,
            chapter_count=get_chapter_count(
                video.name,
                self.request.data['number']
            )
        )
        new_season_task.delay(serializer.instance.id)
