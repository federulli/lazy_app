import graphene
from schemas.queries import (
    TorrentQuery,
    MovieQuery,
    TVShowQuery,
)


class Query(
    graphene.ObjectType,
    TorrentQuery,
    MovieQuery,
    TVShowQuery
):
    pass


schema = graphene.Schema(query=Query)
