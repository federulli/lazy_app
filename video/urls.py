from django.conf.urls import url
from .views.tv_show_views import (
    ListCreateTvShowView,
    ListCreateSeasonsView,
    RetrieveUpdateDestroyTvShowView,
    RetrieveUpdateDestroySeasonView,
)
from .views.torrents import ListCreateTorrentView
from .views.configuration import ConfigurationView
from .views.movies import (
    ListCreateMoviesView,
    RetrieveUpdateDestroyMoviesView,
)
from .views.refresh import RefreshView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = {
    url(r'^configurations/$', ConfigurationView.as_view()),
    url(r'^torrents/$', ListCreateTorrentView.as_view()),
    url(r'^movies/$', ListCreateMoviesView.as_view()),
    url(
        r'^movies/(?P<pk>\d+)/$',
        RetrieveUpdateDestroyMoviesView.as_view()
    ),
    url(
        r'^tv-shows/$',
        ListCreateTvShowView.as_view()
    ),
    url(
        r'^tv-shows/(?P<pk>\d+)/$',
        RetrieveUpdateDestroyTvShowView.as_view()
    ),
    url(
        r'^tv-shows/(?P<tv_show_id>\d+)/seasons/$',
        ListCreateSeasonsView.as_view()
    ),
    url(
        r'^tv-shows/(?P<tv_show_id>\d+)/seasons/(?P<pk>\d+)/$',
        RetrieveUpdateDestroySeasonView.as_view()
    ),
    url(r'^refresh/$', RefreshView.as_view())
}


urlpatterns = format_suffix_patterns(urlpatterns)
