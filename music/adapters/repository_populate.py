from pathlib import Path

from music.adapters.repository import AbstractRepository
from music.adapters.memory_repository import load_reviews, load_tracks, load_users


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):
    # Load articles and tags into the repository.
    load_tracks(data_path, repo, database_mode)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_reviews(data_path, repo, users)