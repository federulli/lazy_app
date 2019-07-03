import graphene
from models import Movie
from schemas.types import (
    Movie,
    TVShow,
    Season,
    Chapter,
)

from models import (
    S,
    Movie as MovieModel,
    TVShow as TVShowModel,
    Season as SeasonModel,
    Chapter as ChapterModel,
)


class CreateMovie(graphene.Mutation):
    movie = graphene.Field(lambda: Movie)

    class Arguments:
        name = graphene.String(required=True)
        year = graphene.Int(required=False)

    def mutate(self, info, name, year=None):
        movie = MovieModel(name=name, year=year)
        S.add(movie)
        S.flush()
        return CreateMovie(movie=movie)


class CreateTVShow(graphene.Mutation):
    tv_show = graphene.Field(lambda: TVShow)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        tv_show = TVShowModel(name=name)
        S.add(tv_show)
        S.flush()
        return CreateTVShow(tv_show=tv_show)
