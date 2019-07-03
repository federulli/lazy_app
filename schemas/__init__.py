import graphene
from schemas.queries import (
    TorrentQuery,
    MovieQuery,
    TVShowQuery,
)

from schemas.mutations import CreateMovie


class Query(
    graphene.ObjectType,
    TorrentQuery,
    MovieQuery,
    TVShowQuery
):
    pass


class Mutation(graphene.ObjectType):
    create_movie = CreateMovie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
