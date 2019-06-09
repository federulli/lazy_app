from graphene_sqlalchemy import SQLAlchemyObjectType
from models import Torrent as TorrentModel, Movie as MovieModel


class Torrent(SQLAlchemyObjectType):
    class Meta:
        model = TorrentModel


class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel
