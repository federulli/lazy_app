import graphene
from schemas.queries import (
    TorrentQuery,
    MovieQuery,
    TVShowQuery,
)

from schemas.mutations import (
    CreateMovie,
    CreateTVShow,
    CreateSeason,
    SearchMovies,
)


class Query(
    graphene.ObjectType,
    TorrentQuery,
    MovieQuery,
    TVShowQuery
):
    pass


class Mutation(graphene.ObjectType):
    create_movie = CreateMovie.Field()
    create_tv_show = CreateTVShow.Field()
    create_season = CreateSeason.Field()
    search_movies = SearchMovies.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
