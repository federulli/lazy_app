from django.conf.urls import url, include
from .views.tv_show_views import (
    ListCreateTvShowView,
    ListCreateSeasonsView,
)
from .views.movies import ListCreateMoviesView
from .views.views import (
    CreateTorrentView,
    DetailsTorrentView,
    CreateVideoView,
    CreateChapterView,
    CreateSeasonView,
    DetailsChapterView,
    DetailsSeasonView,
    DetailsVideoView,
)
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = {
    url(r'^torrents/$', CreateTorrentView.as_view()),
    url(
        r'^torrents/(?P<pk>\d+)/$',
        DetailsTorrentView.as_view()
    ),
    url(r'^movies/$', ListCreateMoviesView.as_view()),
    url(
        r'^tv-shows/$',
        ListCreateTvShowView.as_view()
    ),
    url(
        r'^tv-shows/(?P<tv_show_id>\d+)/seasons/$',
        ListCreateSeasonsView.as_view()
    ),
}


urlpatterns = format_suffix_patterns(urlpatterns)
