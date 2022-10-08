from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship, synonym

# from music.domainmodel import artist, album, track, user, review
from music.domainmodel.model import Track, Genre, Review,Album, User, Artist
metadata = MetaData()

users_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('liked_tracks', ForeignKey('tracks.id'))
)

review_table = Table( 
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('track_id', ForeignKey('tracks.id')), 
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
    Column('title', String(255), nullable=False),
    Column('album_url', String(255), nullable=True),
    Column('album_type', String(255), nullable=True),
    Column('release_year', Integer, nullable=True),
)
track_table = Table(
    'tracks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255)),
    Column('artist_id', ForeignKey('artists.id')),
    Column('album_id', ForeignKey('albums.id')),
    Column('hyperlink', String(255)),
    Column('duration', Integer, nullable=False)
)

user_tracks_table = Table(
    'user_tracks', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('track_id', ForeignKey('tracks.id'))
)

genre_table = Table(
    'genres', metadata,
    Column('genre_id', Integer, primary_key=True),   
    Column('genre_name', String(64), nullable=False)
    )
    
track_genres_table = Table(
    'track_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('track_id', ForeignKey('tracks.id')),
    Column('genre_id', ForeignKey('genres.genre_id'))
)


def map_model_to_tables():

    mapper(User, users_table, properties={
        '_User__user_id': users_table.c.id,
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        # '_User__reviews': relationship(Review),
        '_User__reviews': relationship(Review, backref='_Review__user'),
        # '_User__liked_tracks': relationship(Track, backref='_Track__user')
        '_User__liked_tracks': relationship(Track, secondary=user_tracks_table)
        # '_User__liked_tracks': relationship(Track, secondary=user_tracks_table,
        #                                back_populates='_Track__track_users')
        # '_User__reviews': relationship(Review),
        # '_User__tracks': relationship(Track, secondary=user_tracks_table)
    })
    mapper(Review, review_table, properties={
        '_Review__review_text': review_table.c.review, 
        '_Review__timestamp': review_table.c.timestamp,
        # '_Review__user': relationship(User),
        # '_Review__user': relationship(User)
        # '_Review__user': relationship(User),
        # '_Review__track':  relationship(Track),
    })
    mapper(Artist,artist_table, properties={
        
        '_Artist__artist_id': artist_table.c.id,
        '_Artist__full_name': artist_table.c.full_name
    })
    mapper(Album, album_table,properties={
        '_Album__album_id': album_table.c.id,
        '_Album__title': album_table.c.title,
        '_Album__album_url': album_table.c.album_url,
        '_Album__album_type': album_table.c.album_type,
        '_Album__release_year': album_table.c.release_year,
    })
    mapper(Track, track_table, properties={
        '_Track__track_id': track_table.c.id, 
        '_Track__title': track_table.c.title, 
        '_Track__track_url': track_table.c.hyperlink,
        '_Track__genres': relationship(Genre, secondary=track_genres_table),
        # '_Track__genres': relationship(Genre, secondary=track_genres_table,
        #                                back_populates='_Genre__genre_tracks'),
        '_Track__artist': relationship(Artist),
        '_Track__album': relationship(Album),
        '_Track__track_duration': track_table.c.duration,
        # '_Track__reviews': relationship(Review),
        '_Track__reviews': relationship(Review, backref='_Review__track'),
        '_Track__track_users': relationship(User, secondary=user_tracks_table)
        # '_Track__track_users': relationship(User, secondary=user_tracks_table,
        #                                back_populates='_User__liked_tracks')
       
    })
    
    mapper(Genre, genre_table, properties={
        '_Genre__genre_id': genre_table.c.genre_id, 
        '_Genre__name': genre_table.c.genre_name,
        # '_Genre__genre_tracks': relationship(Track,
        #     secondary=track_genres_table, back_populates="_Track__genres"
        # )
    })
    
