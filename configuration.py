from models import Configuration as db_config
import os
YTS_URL_DEFAULT = 'https://yts.am/api/v2'
TPB_URL_DEFAULT = ''
BASE_PATH_DEFAULT = '/downloads'
MOVIE_SUB_PATH_DEFAULT = 'movies'
TV_SHOWS_SUB_PATH_DEFAULT = 'tv_shows'


class Configuration:

    def __init__(self):
        self._value_by_name = {
            config.name: config.value
            for config in db_config.query
        }

    @property
    def yts_url(self):
        return self._value_by_name.get('yts_url', YTS_URL_DEFAULT)

    @property
    def tpb_url(self):
        return self._value_by_name.get('tpb_url', TPB_URL_DEFAULT)

    @property
    def base_download_path(self):
        return self._value_by_name.get('base_download_path', BASE_PATH_DEFAULT)

    @property
    def movie_download_path(self):
        return os.path.join(
            self.base_download_path,
            self._value_by_name.get('movies_sub_path', MOVIE_SUB_PATH_DEFAULT)
        )

    @property
    def tv_show_download_path(self):
        return os.path.join(
            self.base_download_path,
            self._value_by_name.get('tv_shows_sub_path', TV_SHOWS_SUB_PATH_DEFAULT)
        )
