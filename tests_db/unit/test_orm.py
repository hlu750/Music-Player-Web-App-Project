import pytest

import datetime

from sqlalchemy.exc import IntegrityError

# from music.domainmodel import User, track, Comment, Tag, make_comment, make_tag_association
from music.domainmodel.user import User
from music.domainmodel.track import Track, Review
from music.domainmodel.genre import Genre
from music.domainmodel.artist import Artist  

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
        '("A title", 3, 3, "https://en.wikipedia.org/wiki/Hyperlink", 168'
    )
    row = empty_session.execute('SELECT id from tracks').fetchone()
    return row[0]


# def insert_tags(empty_session):
#     empty_session.execute(
#         'INSERT INTO tags (tag_name) VALUES ("News"), ("New Zealand")'
#     )
#     rows = list(empty_session.execute('SELECT id from tags'))
#     keys = tuple(row[0] for row in rows)
#     return keys


# def insert_track_tag_associations(empty_session, track_key, tag_keys):
#     stmt = 'INSERT INTO track_tags (track_id, tag_id) VALUES (:track_id, :tag_id)'
#     for tag_key in tag_keys:
#         empty_session.execute(stmt, {'track_id': track_key, 'tag_id': tag_key})


# def insert_commented_track(empty_session):
#     track_key = insert_track(empty_session)
#     user_key = insert_user(empty_session)

#     timestamp_1 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#     timestamp_2 = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#     empty_session.execute(
#         'INSERT INTO comments (user_id, track_id, comment, timestamp) VALUES '
#         '(:user_id, :track_id, "Comment 1", :timestamp_1),'
#         '(:user_id, :track_id, "Comment 2", :timestamp_2)',
#         {'user_id': user_key, 'track_id': track_key, 'timestamp_1': timestamp_1, 'timestamp_2': timestamp_2}
#     )

#     row = empty_session.execute('SELECT id from tracks').fetchone()
#     return row[0]


# def make_track():
#     track = track(
#         track_date,
#         "Coronavirus: First case of virus in New Zealand",
#         "The first case of coronavirus has been confirmed in New Zealand  and authorities are now scrambling to track down people who may have come into contact with the patient.",
#         "https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus",
#         "https://resources.stuff.co.nz/content/dam/images/1/z/e/3/w/n/image.related.StuffLandscapeSixteenByNine.1240x700.1zduvk.png/1583369866749.jpg"
#     )
#     return track


def make_user():
    user = User("Andrew", "111")
    return user


# def make_tag():
#     tag = Tag("News")
#     return tag


# def test_loading_of_users(empty_session):
#     users = list()
#     users.append(("Andrew", "1234"))
#     users.append(("Cindy", "1111"))
#     insert_users(empty_session, users)

#     expected = [
#         User("Andrew", "1234"),
#         User("Cindy", "999")
#     ]
#     assert empty_session.query(User).all() == expected

# def test_saving_of_users(empty_session):
#     user = make_user()
#     empty_session.add(user)
#     empty_session.commit()

#     rows = list(empty_session.execute('SELECT user_name, password FROM users'))
#     assert rows == [("Andrew", "111")]


# def test_saving_of_users_with_common_user_name(empty_session):
#     insert_user(empty_session, ("Andrew", "1234"))
#     empty_session.commit()

#     with pytest.raises(IntegrityError):
#         user = User("Andrew", "111")
#         empty_session.add(user)
#         empty_session.commit()


# def test_loading_of_track(empty_session):
#     track_key = insert_track(empty_session)
#     expected_track = make_track()
#     fetched_track = empty_session.query(track).one()

#     assert expected_track == fetched_track
#     assert track_key == fetched_track.id


# def test_loading_of_tagged_track(empty_session):
#     track_key = insert_track(empty_session)
#     tag_keys = insert_tags(empty_session)
#     insert_track_tag_associations(empty_session, track_key, tag_keys)

#     track = empty_session.query(track).get(track_key)
#     tags = [empty_session.query(Tag).get(key) for key in tag_keys]

#     for tag in tags:
#         assert track.is_tagged_by(tag)
#         assert tag.is_applied_to(track)


# def test_loading_of_commented_track(empty_session):
#     insert_commented_track(empty_session)

#     rows = empty_session.query(track).all()
#     track = rows[0]

#     for comment in track.comments:
#         assert comment.track is track


# def test_saving_of_comment(empty_session):
#     track_key = insert_track(empty_session)
#     user_key = insert_user(empty_session, ("Andrew", "1234"))

#     rows = empty_session.query(track).all()
#     track = rows[0]
#     user = empty_session.query(User).filter(User._User__user_name == "Andrew").one()

#     # Create a new Comment that is bidirectionally linked with the User and track.
#     comment_text = "Some comment text."
#     comment = make_comment(comment_text, user, track)

#     # Note: if the bidirectional links between the new Comment and the User and
#     # track objects hadn't been established in memory, they would exist following
#     # committing the addition of the Comment to the database.
#     empty_session.add(comment)
#     empty_session.commit()

#     rows = list(empty_session.execute('SELECT user_id, track_id, comment FROM comments'))

#     assert rows == [(user_key, track_key, comment_text)]


# def test_saving_of_track(empty_session):
#     track = make_track()
#     empty_session.add(track)
#     empty_session.commit()

#     rows = list(empty_session.execute('SELECT date, title, first_paragraph, hyperlink, image_hyperlink FROM tracks'))
#     date = track_date.isoformat()
#     assert rows == [(date,
#                      "Coronavirus: First case of virus in New Zealand",
#                      "The first case of coronavirus has been confirmed in New Zealand  and authorities are now scrambling to track down people who may have come into contact with the patient.",
#                      "https://www.stuff.co.nz/national/health/119899280/ministry-of-health-gives-latest-update-on-novel-coronavirus",
#                      "https://resources.stuff.co.nz/content/dam/images/1/z/e/3/w/n/image.related.StuffLandscapeSixteenByNine.1240x700.1zduvk.png/1583369866749.jpg"
#                      )]


# def test_saving_tagged_track(empty_session):
#     track = make_track()
#     tag = make_tag()

#     # Establish the bidirectional relationship between the track and the Tag.
#     make_tag_association(track, tag)

#     # Persist the track (and Tag).
#     # Note: it doesn't matter whether we add the Tag or the track. They are connected
#     # bidirectionally, so persisting either one will persist the other.
#     empty_session.add(track)
#     empty_session.commit()

#     # Test test_saving_of_track() checks for insertion into the tracks table.
#     rows = list(empty_session.execute('SELECT id FROM tracks'))
#     track_key = rows[0][0]

#     # Check that the tags table has a new record.
#     rows = list(empty_session.execute('SELECT id, tag_name FROM tags'))
#     tag_key = rows[0][0]
#     assert rows[0][1] == "News"

#     # Check that the track_tags table has a new record.
#     rows = list(empty_session.execute('SELECT track_id, tag_id from track_tags'))
#     track_foreign_key = rows[0][0]
#     tag_foreign_key = rows[0][1]

#     assert track_key == track_foreign_key
#     assert tag_key == tag_foreign_key


# def test_save_commented_track(empty_session):
#     # Create track User objects.
#     track = make_track()
#     user = make_user()

#     # Create a new Comment that is bidirectionally linked with the User and track.
#     comment_text = "Some comment text."
#     comment = make_comment(comment_text, user, track)

#     # Save the new track.
#     empty_session.add(track)
#     empty_session.commit()

#     # Test test_saving_of_track() checks for insertion into the tracks table.
#     rows = list(empty_session.execute('SELECT id FROM tracks'))
#     track_key = rows[0][0]

#     # Test test_saving_of_users() checks for insertion into the users table.
#     rows = list(empty_session.execute('SELECT id FROM users'))
#     user_key = rows[0][0]

#     # Check that the comments table has a new record that links to the tracks and users
#     # tables.
#     rows = list(empty_session.execute('SELECT user_id, track_id, comment FROM comments'))
#     assert rows == [(user_key, track_key, comment_text)]