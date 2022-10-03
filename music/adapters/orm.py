from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

from music.domainmodel import artist, album, track, genre, user, review

metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

review_table = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.id')), 
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)
artist_table = Table(
    'artists', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column()
)

track_table = Table(
    'tracks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('artist_id', Integer, ForeignKey('artists.id')),
    Column('album_id', Integer, ForeignKey('albums.id')),
    Column('hyperlinke', String(255)),
    Column('duration', Integer, nullable=False),
    Column('genre', String(255))
)

genre_table = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),   
    Column('genre_name', String(64), nullable=False)
    )
track_genres_table = Table(
    'track_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.id')),
    Column('genre_id', ForeignKey('genres.id'))
)
