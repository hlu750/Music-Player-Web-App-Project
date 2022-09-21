from typing import List, Iterable

from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Review
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.user import User

class NonExistentTrackException(Exception):
    pass

class UnknownUserException(Exception):
    pass

def add_review(track_id: int, review_text: str, user_name: str, repo: AbstractRepository):
    # Check that the track exists.
    track = repo.get_track(track_id)[1]
    if track is None:
        raise NonExistentTrackException
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = Review(track, review_text, 5)
    print(track, review)
    # Update the repository.
    track.add_review(review)
    repo.add_review(review)


def get_track(track_id: int, repo: AbstractRepository):
    track = repo.get_track(track_id)

    if track is None:
        raise NonExistentTrackException
    return track
    return track_to_dict(track)


def get_tracks_by_id(id_list, repo: AbstractRepository):
    tracks = repo.get_tracks_by_id(id_list)

    # Convert tracks to dictionary form.
    tracks_as_dict = tracks_to_dict(tracks)

    return tracks_as_dict


def get_reviews_for_track(track_id, repo: AbstractRepository):
    track = repo.get_track(track_id)

    if track is None:
        raise NonExistentTrackException

    return reviews_to_dict(track.reviews)

def add_liked_track(track, user_name: str, repo: AbstractRepository):
    # Check that the track exists.
    if track is None:
        raise NonExistentTrackException
    user : User = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException

    # Create review.
    print(track)
    # Update the repository.
    user.add_liked_track(track)

def get_liked_tracks(user_name, repo: AbstractRepository):
    user : User = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    tracks = user.liked_tracks
    if tracks is None:
        raise NonExistentTrackException
    print("over here1")
    print(tracks)
    return tracks_to_dict(tracks)

# def get_liked_tracks(user_name, repo: AbstractRepository):
#     # tracks = repo.get_liked_tracks(user)
#     user : User = repo.get_user(user_name)
#     tracks = user.liked_tracks

#     if tracks is None:
#         raise NonExistentTrackException

#     return tracks

# ============================================
# Functions to convert model entities to dicts
# ============================================

def track_to_dict(track: Track):
    print("over here3")
    print(track)
    track_dict = {
        'id': track.track_id,
        'title': track.title,
        'hyperlink': track.track_url,
    }
    return track_dict


def tracks_to_dict(tracks: Iterable[Track]):
    print("over here2")
    print(tracks)
    return [track_to_dict(track) for track in tracks]


def review_to_dict(review: Review):
    review_dict = {
        'user_name': review.user.user_name,
        'track_id': review.track.track_id,
        'review_text': review.review_text,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]

# ============================================
# Functions to convert dicts to model entities
# ============================================

