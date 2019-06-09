import graphene
from schemas.queries import TorrentQuery, MovieQuery


class Query(graphene.ObjectType, TorrentQuery, MovieQuery):
    pass


schema = graphene.Schema(query=Query)
