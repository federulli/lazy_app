from django.db import models
from qbittorrent_api import post_torrent
import re


class Torrent(models.Model):
    FINISHED = 'finished'
    PAUSED = 'paused'
    CANCELLED = 'cancelled'
    IN_PROGRESS = 'in_progress'
    STATUS = (
        (FINISHED, 'finished'),
        (PAUSED, 'paused'),
        (CANCELLED, 'cancelled'),
        (IN_PROGRESS, 'in_progress'),
    )
    has_subtitle = models.BooleanField(default=False)
    status = models.CharField(choices=STATUS, max_length=20)
    magnet = models.TextField()
    download_path = models.TextField()

    def save(self, *args, **kwargs):
        post_torrent(self.magnet, self.download_path)
        return super(Torrent, self).save(*args, **kwargs)

    @property
    def hash(self):
        return re.search(
            r'^magnet:\?xt=urn:btih:([\w]*)&.*',
            str(self.magnet)
        ).groups()[0]


class Video(models.Model):
    TV_SHOW = 'TVSHOW'
    MOVIE = 'MOVIE'
    TYPES = (
        (TV_SHOW, 'TV Show'),
        (MOVIE, 'Movie')
    )
    name = models.TextField()
    type = models.CharField(max_length=6, choices=TYPES)
    torrent = models.ForeignKey(Torrent, on_delete=models.CASCADE,
                                related_name='movie', null=True)


class Season(models.Model):
    number = models.IntegerField()
    video = models.ForeignKey(
        Video,
        related_name='seasons',
        on_delete=models.CASCADE
    )
    chapter_count = models.IntegerField()
    completed = models.BooleanField(default=False)


class Chapter(models.Model):
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name='chapters'
    )
    number = models.IntegerField()
    torrent = models.ForeignKey(
        Torrent,
        on_delete=models.CASCADE,
        related_name='show'
    )


class Configuration(models.Model):
    name = models.TextField(unique=True)
    value = models.TextField()
