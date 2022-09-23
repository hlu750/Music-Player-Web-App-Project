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
from music.adapters.repository import repo_instance, AbstractRepository
import music.adapters.repository as repo


#cool feature
def test_can_add_liked_song(in_memory_repo):
    print("hello?")
    track = Track(7, 'Song for testing')
    print("hello? track")
    user = in_memory_repo.get_user('fmercury')
    print("hello? user")
    in_memory_repo.add_liked_track(track)
    print("hello? repo")

    assert track in in_memory_repo.get_liked_tracks(user)

def test_repository_can_add_a_review(in_memory_repo):
    prev_track, track, next_track = in_memory_repo.get_track(2)
    review = Review(track, "test review", 5, "fmercury")
    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()

#cool feature
def test_can_get_liked_tracks(in_memory_repo):
    prev_track, track, next_track = in_memory_repo.get_track(2)
    print("testt")
    in_memory_repo.add_liked_track(track)
    print("testtt")
    user = in_memory_repo.get_user('fmercury')
    print("testtt")
    assert len(in_memory_repo.get_liked_tracks(user)) == 1

def test_repository_can_retrieve_reviews(in_memory_repo):
    prev_track, track, next_track = in_memory_repo.get_track(2)
    review = Review(track, "test review", 5, "fmercury")
    in_memory_repo.add_review(review)
    assert len(in_memory_repo.get_reviews()) == 1


def test_repository_can_add_a_user(in_memory_repo):
    user = User(5, 'dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('dave') == user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User(2, 'fmercury', '8734gfe2058v')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None

def test_repository_can_retrieve_user_count(in_memory_repo):
    number_of_users = in_memory_repo.get_number_of_users()

    # Check that the query returned 2 users.
    assert number_of_users == 2

def test_repository_can_retrieve_track_count(in_memory_repo):
    number_of_tracks = in_memory_repo.get_number_of_tracks()

    # Check that the query returned 10 tracks.
    assert number_of_tracks == 10


def test_repository_can_add_track(in_memory_repo):
    track = Track(7, 'Song for testing')  
    in_memory_repo.add_track(track)
    prev_track, track2, next_track = in_memory_repo.get_track(track.track_id)
    assert track2 == track


def test_repository_can_retrieve_track(in_memory_repo):
    prev_track, track, next_track = in_memory_repo.get_track(2)

    # Check that the track has the expected title.
    assert track.title == 'Food'


def test_repository_does_not_retrieve_a_non_existent_track(in_memory_repo):
    prev_track, track, next_track = in_memory_repo.get_track(3000)
    assert track is None


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


def test_repository_returns_none_when_there_are_no_previous_tracks(in_memory_repo):
    prev_track, track, next_track = in_memory_repo.get_track(2)

    assert prev_track is None


def test_repository_returns_none_when_there_are_no_subsequent_tracks(in_memory_repo):
    prev_track, track, next_track = in_memory_repo.get_track(139)

    assert next_track is None


# def test_repository_can_add_a_genre(in_memory_repo):
#     genre = genre(30, 'New-genre')
#     in_memory_repo.add_genre(genre)

#     assert genre in in_memory_repo.get_genres()


def test_repository_can_add_a_review(in_memory_repo):
    prev_track, track, next_track = in_memory_repo.get_track(2)
    review = Review(track, "test review", 5, "fmercury")
    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()

def test_repository_can_retrieve_reviews(in_memory_repo):
    prev_track, track, next_track = in_memory_repo.get_track(2)
    review = Review(track, "test review", 5, "fmercury")
    in_memory_repo.add_review(review)
    assert len(in_memory_repo.get_reviews()) == 1



