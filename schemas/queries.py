import graphene
from schemas.types import (
    Torrent,
    Movie,
)


class TorrentQuery:
    torrents = graphene.List(
        Torrent,
        id=graphene.ID(required=False)
    )

    def resolve_torrents(self, info, id=None):
        query = Torrent.get_query(info)
        if id:
            query = query.filter_by(id=id)
        return query.all()


class MovieQuery:
    movies = graphene.List(
        Movie,
        id=graphene.ID(required=False)
    )

    def resolve_movies(self, info, id=None):
        query = Movie.get_query(info)
        if id:
            query = query.filter_by(id=id)
        return query.all()
