from rest_framework import generics
from ..models import Video
from ..serializers import VideoSerializer
from ..tasks import new_movie_task


class ListCreateMoviesView(generics.ListCreateAPIView):
    queryset = Video.objects.filter(type='MOVIE')
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        serializer.save(type='MOVIE')
        new_movie_task.delay(serializer.instance.id)


class RetrieveUpdateDestroyMoviesView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VideoSerializer
    queryset = Video.objects.filter(type='MOVIE')
