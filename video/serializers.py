from rest_framework import serializers
from .models import Torrent, Video, Season, Chapter


class TorrentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torrent
        fields = '__all__'


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        exclude = ('type',)


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'


class SeasonSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)

    class Meta:
        model = Season
        exclude = ('video',)
