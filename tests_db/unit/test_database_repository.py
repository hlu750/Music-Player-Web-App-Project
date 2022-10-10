from datetime import date, datetime

import pytest

import music.adapters.repository as repo
from music.adapters.database_repository import SqlAlchemyRepository
from music.domainmodel.model import User, Track, Genre, Review, Artist, make_comment
# # from music.domainmodel.user import User
# # from music.domainmodel.track import Track, Review
# # from music.domainmodel.genre import Genre
# # from music.domainmodel.artist import Artist  

from music.adapters.repository import RepositoryException

def test_repository_can_add_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    user_id = repo.get_number_of_users() + 1
    user = User(user_id, 'Dave', '123456789')
    repo.add_user(user)
    user_id = repo.get_number_of_users() + 1
    repo.add_user(User(user_id, 'Martin', '123456789'))
    user2 = repo.get_user('dave')
    assert user2 == user and user2 is user

def test_repository_can_retrieve_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('fmercury')
    assert user == User(2, 'fmercury', '8734gfe2058v')

def test_repository_does_not_retrieve_a_non_existent_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    user = repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_user_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_users = repo.get_number_of_users()

    assert number_of_users == 3

def test_repository_can_retrieve_track_count(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    number_of_tracks = repo.get_number_of_tracks()

    assert number_of_tracks == 2000

def test_repository_can_add_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    # number_of_tracks = repo.get_number_of_tracks()

    new_track_id = 3662

    track = Track(
        new_track_id,
        'Testing Track'
    )
    repo.add_track(track)
    prev, track2, next = repo.get_track(new_track_id)
    assert track2 == track

def test_repository_can_retrieve_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    prev, track, next = repo.get_track(2)

    assert track.title == 'Food'

    # Check that the track is reviewed as expected.
    # review_one = [review for review in track.reviews if review.review == 'Oh no, COVID-19 has hit New Zealand'][
    #     0]
    # review_two = [review for review in track.reviews if review.review == 'Yeah Freddie, bad news'][0]

    # assert review_one.user.user_name == 'fmercury'
    # assert review_two.user.user_name == "thorke"

    # # Check that the track is tagged as expected.
    # assert track.is_tagged_by(Genre('Health'))
    # assert track.is_tagged_by(Genre('New Zealand'))

def test_repository_does_not_retrieve_a_non_existent_track(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    prev, track, next = repo.get_track(1)
    assert track is None

def test_repository_can_retrieve_tracks_by_genre(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_track_by_genre('Jazz')

    assert len(tracks) == 31

def test_repository_can_retrieve_tracks_by_artist(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_filtered_tracks('AWOL', 'artist')

    assert len(tracks) == 4

def test_repository_can_retrieve_tracks_by_album(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_filtered_tracks('Niris', 'album')

    assert len(tracks) == 5

def test_repository_can_retrieve_tracks_by_title(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    tracks = repo.get_filtered_tracks('Untitled', 'track')

    assert len(tracks) == 37

def test_repository_returns_none_when_there_are_no_previous_tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    prev, track, next = repo.get_track(2)

    assert prev is None


def test_repository_returns_none_when_there_are_no_subsequent_tracks(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    prev, track, next = repo.get_track(3661)
    assert next is None

# def test_repository_can_add_genre(session_factory):
#     repo = SqlAlchemyRepository(session_factory)
    
#     repo.add_genre(Genre(1, 'New'))

#     assert repo.ge()


def test_repository_can_add_a_review(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    
    user = repo.get_user('thorke')
    prev, track, next = repo.get_track(2)
    review = make_comment("Love this!", user, track, datetime.today())
    repo.add_review(review)

    assert review in repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    prev, track, next = repo.get_track(2)
    review = Review(track, "Love this!", 5, None)
    repo.add_review(review)
    assert repo.get_number_of_reviews() == 3

    # with pytest.raises(RepositoryException):
    #     repo.add_review(review)


def test_repository_can_retrieve_reviews(session_factory):
    repo = SqlAlchemyRepository(session_factory)

    assert len(repo.get_reviews()) == 3


def make_track():
    track = Track(
        3662, 'A track'
    )
    return track

def test_can_retrieve_a_track_and_add_a_review_to_it(session_factory):
    repo = SqlAlchemyRepository(session_factory)
    
    # Fetch track and User.
    prev, track, next = repo.get_track(2)
    user = repo.get_user('thorke')

    # Create a new review, connecting it to the track and User.
    review = make_comment('Yuck', user, track)

    prev, track_fetched, next = repo.get_track(5)
    user_fetched = repo.get_user('thorke')
    
    assert review in repo.get_reviews()
    # assert review in track_fetched.reviews
    # assert review in user_fetched.reviews

