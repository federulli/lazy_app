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


class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        exclude = ('video', 'chapter_count')


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = '__all__'
