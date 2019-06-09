import re
import os
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Enum,
    UniqueConstraint,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, scoped_session

from sqlalchemy import create_engine

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, 'db.sqlite3')

engine = create_engine(f'sqlite:///{db_path}', convert_unicode=True)

S = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine)
)

Base = declarative_base()
Base.query = S.query_property()


class Torrent(Base):
    __tablename__ = 'torrent'
    id = Column(Integer, primary_key=True)
    has_subtitle = Column(Boolean, default=False)
    magnet = Column(String, nullable=False)
    download_path = Column(String, nullable=False)

    @property
    def hash(self):
        return re.search(
            r'^magnet:\?xt=urn:btih:([\w]*)&.*',
            str(self.magnet)
        ).groups()[0]


class Video(Base):
    __tablename__ = 'video'
    TV_SHOW = 'TVSHOW'
    MOVIE = 'MOVIE'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(Enum(*[TV_SHOW, MOVIE]), nullable=False)

    __mapper_args__ = {
        'polymorphic_on': type,
    }


class Movie(Video):
    __mapper_args__ = {
        'polymorphic_identity': Video.MOVIE
    }

    year = Column(Integer, nullable=True)
    torrent_id = Column(Integer, ForeignKey('torrent.id'))
    torrent = relationship("Torrent")


class TVShow(Video):
    __mapper_args__ = {
        'polymorphic_identity': Video.TV_SHOW
    }


class Season(Base):
    __tablename__ = 'season'
    __table_args__ = (
        UniqueConstraint('number', 'tv_show_id'),
    )
    id = Column(Integer, primary_key=True)
    number = Column(Integer, nullable=False)
    tv_show_id = Column(Integer, ForeignKey(TVShow.id))
    tv_show = relationship(TVShow, backref="seasons")
    chapter_count = Column(Integer, nullable=False)
    completed = Column(Boolean, default=False)


class Chapter(Base):
    __tablename__ = 'chapter'
    id = Column(Integer, primary_key=True)
    season_id = Column(Integer, ForeignKey('season.id'), nullable=False)
    season = relationship('Season', backref=backref("chapters", cascade="delete,delete-orphan"))
    number = Column(Integer, nullable=False)
    torrent_id = Column(Integer, ForeignKey(Torrent.id))
    torrent = relationship(Torrent, cascade='delete')


class Configuration(Base):
    __tablename__ = 'configuration'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    value = Column(String, nullable=False)
