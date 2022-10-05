from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters.csvdatareader import load_reviews, load_users, load_tracks_and_albums


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    # Load articles and tags into the repository.
    load_tracks_and_albums(data_path, repo, database_mode)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    # load_comments(data_path, repo, users)