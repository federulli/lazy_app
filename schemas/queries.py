import graphene
from schemas.types import (
    Torrent,
    Movie,
    TVShow,
    Season,
    Chapter,
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


class TVShowQuery:
    tv_shows = graphene.List(
        TVShow,
        id=graphene.ID(required=False)
    )
    seasons = graphene.List(
        Season,
        tv_show_id=graphene.ID(required=False),
        id=graphene.ID(required=False)
    )
    chapters = graphene.List(
        Chapter,
        season_id=graphene.ID(required=False),
        id=graphene.ID(required=False)
    )

    def resolve_tv_shows(self, info, id=None):
        query = TVShow.get_query(info)
        if id:
            query = query.filter_by(id=id)
        return query.all()

    def resolve_seasons(self, info, tv_show_id=None, id=None):
        query = Season.get_query(info)
        if id:
            query = query.filter_by(id=id)
        if tv_show_id:
            query = query.filter_by(tv_show_id=tv_show_id)
        return query.all()

    def resolve_chapters(self, info, season_id=None, id=None):
        query = Chapter.get_query(info)
        if id:
            query = query.filter_by(id=id)
        if season_id:
            query = query.filter_by(tv_show_id=season_id)
        return query.all()
