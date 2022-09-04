from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track


def get_random_track(repo: AbstractRepository):
    return repo.get_random_track()