import graphene
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
        S.commit()
        return CreateMovie(movie=movie)


class CreateTVShow(graphene.Mutation):
    tv_show = graphene.Field(lambda: TVShow)

    class Arguments:
        name = graphene.String(required=True)

    def mutate(self, info, name):
        tv_show = TVShowModel(name=name)
        S.add(tv_show)
        S.commit()
        return CreateTVShow(tv_show=tv_show)


class CreateSeason(graphene.Mutation):
    season = graphene.Field(lambda: Season)

    class Arguments:
        number = graphene.Int(required=True)
        tv_show_id = graphene.ID(required=True)

    def mutate(self, info, number, tv_show_id):
        from tasks import new_season_task
        season = SeasonModel(
            number=number,
            tv_show_id=tv_show_id,
            chapter_count=0,
            completed=False
        )
        S.add(season)
        S.commit()
        new_season_task.delay(season.id)
        return CreateSeason(season=season)


class SearchMovies(graphene.Mutation):
    msg = graphene.String()

    def mutate(self, info):
        from tasks import search_for_not_found_movies
        search_for_not_found_movies.delay()


class SearchChapters(graphene.Mutation):
    msg = graphene.String()

    def mutate(self, info):
        from tasks import search_for_not_found_chapters
        search_for_not_found_chapters.delay()


class DeleteCompleted(graphene.Mutation):
    msg = graphene.String()

    def mutate(self, info):
        from tasks import delete_torrents
        delete_torrents.delay()


class DownloadSubtitles(graphene.Mutation):
    msg = graphene.String()

    def mutate(self, info):
        from tasks import download_subtitles
        download_subtitles.delay()


class ReloadChapterCount(graphene.Mutation):
    msg = graphene.String()

    def mutate(self, info):
        from tasks import download_subtitles
        download_subtitles.delay()

