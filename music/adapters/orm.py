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
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('full_name', String(255), nullable=False)
)

track_table = Table(
    'track', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('artist_id', ForeignKey('artists.id')),
    Column('album_id', ForeignKey('albums.id')),
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
    Column('track_id', ForeignKey('track.id')),
    Column('genre_id', ForeignKey('genres.id'))
)


def map_model_to_tables():

    mapper(user.User, users_table, properties={
        '_User__user_name': users_table.c.user_name,
        '_User__password': users_table.c.password,
        '_User__reviews': relationship(track.Review, backref='_Review__user')
    })
    mapper(track.Review, review_table, properties={
        '_Review__user_name': review_table.c.user_name
        '_Review__track': review_table.c.track_id,
        '_Review__review_text': review_table.c.review, 
        '_Review__timestamp': review_table.c.timestamp
    })

    mapper(track.Track, track_table, properties={
        '_Track__id': track_table.c.id,
        '_Track__date': track_table.c.date,
        '_Track__title': track_table.c.title,
        '_Track__hyperlink': track_table.c.hyperlink,
        '_Track__image_hyperlink': track_table.c.image_hyperlink,
        '_Track__comments': relationship(track.Review, backref='_Comment__track'),
        '_Track__tags': relationship(track.Genre, secondary=track_tags_table,
                                       back_populates='_Tag__tagged_track')
    })
    mapper(model.Tag, tags_table, properties={
        '_Tag__tag_name': tags_table.c.tag_name,
        '_Tag__tagged_track': relationship(
            model.Track,
            secondary=track_tags_table,
            back_populates="_Track__tags"
        )
    })