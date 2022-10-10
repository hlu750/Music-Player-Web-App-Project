import pytest

import datetime

from sqlalchemy.exc import IntegrityError

from music.domainmodel.model import User, Track, Review, Genre, make_comment
# from music.domainmodel.user import User
# from music.domainmodel.track import Track, Review
# from music.domainmodel.genre import Genre
# from music.domainmodel.artist import Artist  

def insert_user(empty_session, values=None):
    new_name = "Andrew"
    new_password = "1234"

    if values is not None:
        new_name = values[0]
        new_password = values[1]

    empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                          {'user_name': new_name, 'password': new_password})
    row = empty_session.execute('SELECT id from users where user_name = :user_name',
                                {'user_name': new_name}).fetchone()
    return row[0]

def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (user_name, password) VALUES (:user_name, :password)',
                              {'user_name': value[0], 'password': value[1]})
    rows = list(empty_session.execute('SELECT id from users'))
    keys = tuple(row[0] for row in rows)
    return keys

def insert_track(empty_session):
    empty_session.execute(
        'INSERT INTO tracks (title, artist_id, album_id, hyperlink, duration) VALUES '
        '("A title", 3, 3, "https://en.wikipedia.org/wiki/Hyperlink", 168)'
    )
    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]


def insert_genres(empty_session):
    empty_session.execute(
        'INSERT INTO genres (genre_name) VALUES ("Soft-Rock"), ("Hard-Rock")'
    )
    rows = list(empty_session.execute('SELECT id from genres'))
    keys = tuple(row[0] for row in rows)
    return keys


def insert_track_genre_associations(empty_session, track_key, genre_keys):
    stmt = 'INSERT INTO track_genres (track_id, genre_id) VALUES (:track_id, :genre_id)'
    for genre_key in genre_keys:
        empty_session.execute(stmt, {'track_id': track_key, 'genre_id': genre_key})


def insert_reviewed_track(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session)

    timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    empty_session.execute(
        'INSERT INTO reviews (user_id, track_id, review, timestamp) VALUES '
        '(:user_id, :track_id, "review 1", :timestamp_1),'
        '(:user_id, :track_id, "review 2", :timestamp_2)',
        {'user_id': user_key, 'track_id': track_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
    )

    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]


def make_track():
    track = Track(1, "A title")
    return track


def make_user():
    return User(1, "andrew", "password")


def make_genre():
    return Genre(1, "New")


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User(1, "Andrew", "1234"),
        User(2, "Cindy", "999")
    ]
    assert empty_session.query(User).all() == expected

def test_saving_of_users(empty_session):
    user = make_user()
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_name, password FROM users'))
    assert rows == [("andrew", "password")]


def test_saving_of_users_with_common_user_name(empty_session):
    insert_user(empty_session, ("andrew", "1234"))
    empty_session.commit()

    with pytest.raises(IntegrityError):
        user = User(1, "andrew", "password")
        empty_session.add(user)
        empty_session.commit()


def test_loading_of_track(empty_session):
    track_key = insert_track(empty_session)
    expected_track = make_track()
    fetched_track = empty_session.query(Track).one()

    assert expected_track == fetched_track
    assert track_key == fetched_track.track_id


# def test_loading_of_genred_track(empty_session):
#     track_key = insert_track(empty_session)
#     genre_keys = insert_genres(empty_session)
#     insert_track_genre_associations(empty_session, track_key, genre_keys)

#     track = empty_session.query(Track).get(track_key)
#     genres = [empty_session.query(Genre).get(key) for key in genre_keys]

#     for genre in genres:
#         assert track.is_genred_by(genre)
#         assert genre.is_applied_to(track)


def test_loading_of_reviewed_track(empty_session):
    insert_reviewed_track(empty_session)

    rows = empty_session.query(Track).all()
    track = rows[0]

    for review in track.reviews:
        assert review.track is track


def test_saving_of_review(empty_session):
    track_key = insert_track(empty_session)
    user_key = insert_user(empty_session, ("andrew", "1234"))

    rows = empty_session.query(Track).all()
    track = rows[0]
    user = empty_session.query(User).filter(User._User__user_name == "andrew").one()

    # Create a new Comment that is bidirectionally linked with the User and track.
    review_text = "Some review text."
    review = make_comment(review_text, user, track)

    # Note: if the bidirectional links between the new Comment and the User and
    # track objects hadn't been established in memory, they would exist following
    # committing the addition of the Comment to the database.
    empty_session.add(review)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT user_id, track_id, review FROM reviews'))

    assert rows == [(user_key, track_key, review_text)]


def test_saving_of_track(empty_session):
    track = make_track()
    empty_session.add(track)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT id, title FROM tracks'))
    assert rows == [(1, "A title")]


# def test_saving_genred_track(empty_session):
#     track = make_track()
#     genre = make_genre()

#     # Establish the bidirectional relationship between the track and the genre.
#     make_genre_association(track, genre)

#     # Persist the track (and genre).
#     # Note: it doesn't matter whether we add the genre or the track. They are connected
#     # bidirectionally, so persisting either one will persist the other.
#     empty_session.add(track)
#     empty_session.commit()

#     # Test test_saving_of_track() checks for insertion into the tracks table.
#     rows = list(empty_session.execute('SELECT id FROM tracks'))
#     track_key = rows[0][0]

#     # Check that the genres table has a new record.
#     rows = list(empty_session.execute('SELECT id, genre_name FROM genres'))
#     genre_key = rows[0][0]
#     assert rows[0][1] == "New"

#     # Check that the track_genres table has a new record.
#     rows = list(empty_session.execute('SELECT track_id, genre_id from track_genres'))
#     track_foreign_key = rows[0][0]
#     genre_foreign_key = rows[0][1]

#     assert track_key == track_foreign_key
#     assert genre_key == genre_foreign_key


def test_save_reviewed_track(empty_session):
    # Create track User objects.
    track = make_track()
    user = make_user()

    # Create a new Comment that is bidirectionally linked with the User and track.
    review_text = "Some review text."
    review = make_comment(review_text, user, track)
    # Save the new track.
    empty_session.add(track)
    empty_session.commit()

    # Test test_saving_of_track() checks for insertion into the tracks table.
    rows = list(empty_session.execute('SELECT id FROM tracks'))
    track_key = rows[0][0]

    # Test test_saving_of_users() checks for insertion into the users table.
    rows = list(empty_session.execute('SELECT id FROM users'))
    user_key = rows[0][0]

    # Check that the comments table has a new record that links to the tracks and users
    # tables.
    rows = list(empty_session.execute('SELECT user_id, track_id, review FROM reviews'))
    assert rows == [(user_key, track_key, review_text)]