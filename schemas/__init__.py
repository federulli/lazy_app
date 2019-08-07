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
    DeleteCompleted,
    SearchChapters,
    ReloadChapterCount,
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
    search_chapters = SearchChapters.Field()
    delete_completed = DeleteCompleted.Field()
    reload_chapter_count = ReloadChapterCount.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
