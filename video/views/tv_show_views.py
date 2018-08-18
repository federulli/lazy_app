from rest_framework import generics
from ..models import (
    Video,
    Season,
)
from ..serializers import (
    VideoSerializer,
    SeasonSerializer,
)


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
        serializer.save(
            video=Video.objects.get(
                pk=self.kwargs['tv_show_id']
            )
        )
