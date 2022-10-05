from re import M
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
    Column('user_name', String(255), nullable=False),
    Column('track_id', ForeignKey('track.id')), 
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)
artist_table = Table(
    'artists', metadata,
    Column('id', Integer, primary_key=True,autoincrement=True),
    Column('full_name', String(255), nullable=False)
)
album_table = Table(
    'albums', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False)
)
track_table = Table(
    'track', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255)),
    Column('artist_id', ForeignKey('artists.id')),
    Column('album_id', ForeignKey('albums.id')),
    Column('hyperlink', String(255)),
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
    Column('track_id', ForeignKey('track.id')),
    Column('genre_id', ForeignKey('genres.id'))
)


def map_model_to_tables():

    mapper(user.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        # '_User__reviews': relationship(track.Review, backref='_Review__user'),
        # '_User__liked_tracks': relationship(track.Track)
    })
    mapper(track.Review, review_table, properties={
        '_Review__review_text': review_table.c.review, 
        '_Review__timestamp': review_table.c.timestamp
    })

    mapper(track.Track, track_table, properties={
        '_Track__track_id': track_table.c.id, 
        '_Track__title': track_table.c.title, 
        '_Track__artist': relationship(artist.Artist),
        '_Track__album': relationship(album.Album),
        '_Track__track_duration': track_table.c.duration,
        '_Track__genres:': relationship(genre.Genre, secondary=track_genres_table),
        '_Track__reviews': relationship(track.Review)
    })
    
    mapper(genre.Genre, genre_table, properties={
        '_Genre__genre_id': genre_table.c.id, 
        '_Genre__name': genre_table.c.id,

    })
    mapper(artist.Artist,artist_table, properties={
        
        '_Artist__artist_id': artist_table.c.id,
        '_Artist__full_name': artist_table.c.full_name
    })
    mapper(album.Album, album_table,properties={
        '_Album__album_id': album_table.c.id,
        '_Album__title': album_table.c.title
    })
