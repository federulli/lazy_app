from rest_framework import generics
from video.serializers import (
    TorrentSerializer,
    VideoSerializer,
    SeasonSerializer,
    ChapterSerializer,
)
from video.models import (
    Torrent,
    Video,
    Season,
    Chapter
)


# ------TORRENT----------
class CreateTorrentView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Torrent.objects.all()
    serializer_class = TorrentSerializer

    def perform_create(self, serializer):
        serializer.save()


class DetailsTorrentView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Torrent.objects.all()
    serializer_class = TorrentSerializer


# ------Video---------
class CreateVideoView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    def perform_create(self, serializer):
        serializer.save()


class DetailsVideoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


# ---------Season--------
class CreateSeasonView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer

    def perform_create(self, serializer):
        serializer.save()


class DetailsSeasonView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer


# ----------Chapter--------
class CreateChapterView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer

    def perform_create(self, serializer):
        serializer.save()


class DetailsChapterView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chapter.objects.all()
    serializer_class = ChapterSerializer
