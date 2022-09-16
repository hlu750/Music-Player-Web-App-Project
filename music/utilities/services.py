from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track

from typing import Iterable
import random

def get_random_track(repo: AbstractRepository):
    return repo.get_random_track()

def get_random_tracks(quantity, repo: AbstractRepository):
    track_count = repo.get_number_of_tracks()

    if quantity >= track_count:
        # Reduce the quantity of ids to generate if the repository has an insufficient number of articles.
        quantity = track_count - 1

    # Pick distinct and random articles.
    random_ids = random.sample(range(1, track_count), quantity)
    tracks = repo.get_tracks_by_id(random_ids)

    # return tracks_to_dict(tracks)
    return tracks

def track_to_dict(track: Track):
    track_dict = {
        'title': track.title,
        'artist': track.artist
    }
    return track_dict


def tracks_to_dict(tracks: Iterable[Track]):
    return [track_to_dict(track) for track in tracks]

def get_ordered_tracks(startIndex, quantity, repo: AbstractRepository):
    tracks = repo.get_tracks_by_quantity(startIndex, quantity)
    return tracks

def get_number_of_pages(quantity, repo: AbstractRepository):
    number_of_pages = repo.get_number_of_pages(quantity)
    return number_of_pages

    