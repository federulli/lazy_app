from models import Configuration as db_config
import os


class Configuration:

    """def __init__(self):
        self._value_by_name = {
            config.name: config.value
            for config in db_config.objects.all()
        }"""

    @property
    def yts_url(self):
        return 'https://yts.am/api/v2'
        #return self._value_by_name['yts_url']

    @property
    def tpb_url(self):
        pass
        #return self._value_by_name['tpb_url']

    @property
    def base_download_path(self):
        return "/tmp/"
        #return self._value_by_name['base_download_path']

    @property
    def movie_download_path(self):
        return "/tmp/"
        """return os.path.join(self.base_download_path,
                            self._value_by_name['movies_sub_path'])"""

    @property
    def tv_show_download_path(self):
        return "/tmp/"
        """return os.path.join(self.base_download_path,
                            self._value_by_name['tv_shows_sub_path'])
        """
