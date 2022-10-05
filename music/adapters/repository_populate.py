from pathlib import Path

from music.adapters.repository import AbstractRepository
<<<<<<< HEAD
from music.adapters.csvdatareader import load_reviews, load_users, load_tracks_and_albums
=======
from music.adapters.memory_repository import load_reviews, load_tracks, load_users
>>>>>>> 390d0c6d75386b9c51d94f782580819ad3515f84


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    # Load articles and tags into the repository.
    load_tracks_and_albums(data_path, repo, database_mode)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    # load_comments(data_path, repo, users)
    load_reviews(data_path, repo, users)
