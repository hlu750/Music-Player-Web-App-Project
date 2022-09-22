from datetime import date, datetime
from typing import List

import pytest

# from music.domainmodel import User, Article, genre, review, make_review

from music.domainmodel.artist import Artist
from music.domainmodel.track import Track, Review
from music.domainmodel.genre import Genre
# from music.domainmodel.review import Review
from music.domainmodel.album import Album
from music.domainmodel.user import User
from music.adapters.repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('5', 'dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('2', 'fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


# def test_repository_can_retrieve_track_count(in_memory_repo):
#     number_of_tracks = in_memory_repo.get_number_of_tracks()

#     # Check that the query returned 6 tracks.
#     assert number_of_tracks == 6


def test_repository_can_add_track(in_memory_repo):
    track = Track(
        2001,
        'Song for testing'
    )  
    assert in_memory_repo.get_track(7) is track


def test_repository_can_retrieve_track(in_memory_repo):
    track = in_memory_repo.get_track(2)

    # Check that the track has the expected title.
    assert track.title == 'Test Song'

    # Check that the track is reviewed as expected.
    review_one = [review for review in track.reviews if review.review == 'Oh no, this song is weird.'][
        0]
    review_two = [review for review in track.reviews if review.review == 'Yikes, tragic.'][0]

    assert review_one.user.user_name == 'fmercury'
    assert review_two.user.user_name == "thorke"

    # Check that the track is genreged as expected.
    assert track.add_genre(Genre('Rock'))
    assert track.add_genre(Genre('Pop'))


def test_repository_does_not_retrieve_a_non_existent_track(in_memory_repo):
    track = in_memory_repo.get_track(3000)
    assert track is None


# def test_repository_can_retrieve_tracks_by_date(in_memory_repo):
#     tracks = in_memory_repo.get_tracks_by_date(date(2020, 3, 1))

#     # Check that the query returned 3 tracks.
#     assert len(tracks) == 3


# def test_repository_does_not_retrieve_an_track_when_there_are_no_tracks_for_a_given_date(in_memory_repo):
#     tracks = in_memory_repo.get_tracks_by_date(date(2020, 3, 8))
#     assert len(tracks) == 0


def test_repository_can_retrieve_genres(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()

    assert len(genres) == 4

    genre_one = [genre for genre in genres if genre.genre_name == 'Rock'][0]
    genre_two = [genre for genre in genres if genre.genre_name == 'Pop'][0]
    genre_three = [genre for genre in genres if genre.genre_name == 'Hip-Hop'][0]
    genre_four = [genre for genre in genres if genre.genre_name == 'Jazz'][0]

    assert genre_one.number_of_genreged_tracks == 3
    assert genre_two.number_of_genreged_tracks == 2
    assert genre_three.number_of_genreged_tracks == 3
    assert genre_four.number_of_genreged_tracks == 1


# def test_repository_can_get_first_track(in_memory_repo):
#     track = in_memory_repo.get_first_track()
#     assert track.title == 'Coronavirus: First case of virus in New Zealand'


# def test_repository_can_get_last_track(in_memory_repo):
#     track = in_memory_repo.get_last_track()
#     assert track.title == 'Coronavirus: Death confirmed as six more test positive in NSW'


def test_repository_can_get_tracks_by_ids(in_memory_repo):
    tracks = in_memory_repo.get_tracks_by_id([2, 3, 5])

    assert len(tracks) == 3
    assert tracks[
               0].title == 'Food'
    assert tracks[1].title == "Electric Ave"
    assert tracks[2].title == 'This World'


def test_repository_does_not_retrieve_track_for_non_existent_id(in_memory_repo):
    tracks = in_memory_repo.get_tracks_by_id([2, 30001])

    assert len(tracks) == 1
    assert tracks[
               0].title == 'Food'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    tracks = in_memory_repo.get_tracks_by_id([3001, 3002])

    assert len(tracks) == 0


def test_repository_returns_track_ids_for_existing_genre(in_memory_repo):
    track_ids = in_memory_repo.get_track_ids_for_genre('Hip-Hop')

    assert track_ids == [2, 3, 5]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    track_ids = in_memory_repo.get_track_ids_for_genre('Does-not-exist')

    assert len(track_ids) == 0


# def test_repository_returns_date_of_previous_track(in_memory_repo):
#     track = in_memory_repo.get_track(6)
#     previous_date = in_memory_repo.get_date_of_previous_track(track)

#     assert previous_date.isoformat() == '2020-03-01'


def test_repository_returns_none_when_there_are_no_previous_tracks(in_memory_repo):
    track = in_memory_repo.get_track(1)
    previous_date = in_memory_repo.get_previous_tracks(track)

    assert previous_date is None


# def test_repository_returns_date_of_next_track(in_memory_repo):
#     track = in_memory_repo.get_track(3)
#     next_date = in_memory_repo.get_date_of_next_track(track)

#     assert next_date.isoformat() == '2020-03-05'


def test_repository_returns_none_when_there_are_no_subsequent_tracks(in_memory_repo):
    track = in_memory_repo.get_track(6)
    next_date = in_memory_repo.get_next_tracks(track)

    assert next_date is None


def test_repository_can_add_a_genre(in_memory_repo):
    genre = genre('New-genre')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    track = in_memory_repo.get_track(2)
    review = make_review("Woohoo!", user, track)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    track = in_memory_repo.get_track(2)
    review = review(None, track, "Woohoo!", datetime.today())

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


# def test_repository_does_not_add_a_review_without_a_track_properly_attached(in_memory_repo):
#     user = in_memory_repo.get_user('thorke')
#     track = in_memory_repo.get_track(2)
#     review = review(None, track, "Trump's onto it!", datetime.today())

#     user.add_review(review)

#     with pytest.raises(RepositoryException):
#         # Exception expected because the track doesn't refer to the review.
#         in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 2



