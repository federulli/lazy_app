from graphene_sqlalchemy import SQLAlchemyObjectType
from models import (
    Torrent as TorrentModel,
    Movie as MovieModel,
    TVShow as TVShowModel,
    Season as SeasonModel,
    Chapter as ChapterModel,
)


class Torrent(SQLAlchemyObjectType):
    class Meta:
        model = TorrentModel


class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel


class TVShow(SQLAlchemyObjectType):
    class Meta:
        model = TVShowModel


class Season(SQLAlchemyObjectType):
    class Meta:
        model = SeasonModel


class Chapter(SQLAlchemyObjectType):
    class Meta:
        model = ChapterModel
