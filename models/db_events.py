from sqlalchemy import event
from models import Torrent
from qbittorrent_api import post_torrent


def after_torrent_insert(mapper, connection, target):
    post_torrent(target.magnet, target.download_path)


def load_listeners():
    event.listen(Torrent, 'after_insert', after_torrent_insert)
