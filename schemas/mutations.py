import graphene
from schemas.types import (
    Movie,
    TVShow,
    Season,
)

from models import (
    S,
    Movie as MovieModel,
    TVShow as TVShowModel,
    Season as SeasonModel,
)
from tasks import (
    new_movie_task,
    new_season_task,
    search_for_not_found_chapters,
    refresh_chapter_count,
    download_subtitles,

)

from qbittorrent_api import (
    delete_completed_torrent,
    delete_all_torrents,
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
        new_movie_task.delay(movie.id)
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
        search_for_not_found_chapters.delay()


class DeleteCompleted(graphene.Mutation):
    msg = graphene.String()

    def mutate(self, info):
        delete_completed_torrent()


class DeleteAllTorrents(graphene.Mutation):
    msg = graphene.String()

    def mutate(self, info):
        delete_all_torrents()


class DownloadSubtitles(graphene.Mutation):
    msg = graphene.String()

    def mutate(self, info):
        download_subtitles.delay()


class ReloadChapterCount(graphene.Mutation):
    msg = graphene.String()

    def mutate(self, info):
        refresh_chapter_count.delay()

