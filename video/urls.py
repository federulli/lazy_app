from django.conf.urls import url
from .views.tv_show_views import (
    ListCreateTvShowView,
    ListCreateSeasonsView,
)
from .views.torrents import ListCreateTorrentView

from .views.movies import ListCreateMoviesView
from .views.refresh import RefreshView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = {
    url(r'^torrents/$', ListCreateTorrentView.as_view()),
    url(r'^movies/$', ListCreateMoviesView.as_view()),
    url(
        r'^tv-shows/$',
        ListCreateTvShowView.as_view()
    ),
    url(
        r'^tv-shows/(?P<tv_show_id>\d+)/seasons/$',
        ListCreateSeasonsView.as_view()
    ),
    url(r'^refresh/$', RefreshView.as_view())
}


urlpatterns = format_suffix_patterns(urlpatterns)
