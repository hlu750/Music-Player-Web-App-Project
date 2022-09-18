import imp
from pathlib import Path
import random
from re import T
from music.adapters.repository import AbstractRepository, RepositoryException
from music.domainmodel.track import Track
from music.domainmodel.album import  Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre  import Genre
from music.domainmodel.playlist  import PlayList
from music.domainmodel.review import Review
from music.domainmodel.user import User
from .csvdatareader import TrackCSVReader
# from csvdatareader import TrackCSVReader
from typing import List
import math 
from bisect import bisect, bisect_left, insort_left

import csv
from datetime import date, datetime
from werkzeug.security import generate_password_hash


class MemoryRepository(AbstractRepository):
    # tracks ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__tracks = list()
        self.__track_index = dict()
        self.__genres = list()
        self.__users = list()
        self.__reviews = list()

    def add_user(self, user: User):
        print(user.user_name)
        self.__users.append(user)
        print(self.__users)

    def get_user(self, user_name) -> User:
        print("username :",user_name)
        if type(user_name) == str:
            return next((user for user in self.__users if user.user_name == user_name.lower()), None)

    def get_number_of_users(self):
        return len(self.__users)

    def add_track(self, track: Track):
        insort_left(self.__tracks, track)
        self.__track_index[track.track_id] = track 

    
    def get_track(self, id:int) -> Track:
        track = None

        try:
            track = self.__track_index[id]
        except KeyError:
            pass
        return track
    @property
    def tracks(self) -> List[Track]:
        return self.__tracks
    @property
    def track_index(self) -> dict:
        return self.__track_index
    def get_random_track(self):
        return random.choice(self.__tracks)
    def get_track_by_genre(self, target_genre: Genre) -> List[Track]:

        pass
        #TODO needs to be implemented
        
    def get_number_of_tracks(self):
            return len(self.__tracks)

    def get_tracks_by_id(self, id_list):
            # Strip out any ids in id_list that don't represent track ids in the repository.
            existing_ids = [id for id in id_list if id in self.__track_index]

            # Fetch the tracks.
            tracks = [self.__track_index[id] for id in existing_ids]
            return tracks

    def get_tracks_by_quantity(self,startIndex, quantity):
        if startIndex >= 0 and startIndex + quantity < len(self.__tracks):
            return self.__tracks[startIndex: startIndex + quantity]
        elif startIndex >= 0:
            return self.__tracks[startIndex:]
        else:
            return None
    def get_number_of_pages(self, quantity):
        number_of_pages = math.ceil(len(self.__tracks) / quantity)
        # print(number_of_pages, len(self.__tracks))
        return math.ceil(len(self.__tracks) / quantity)

    def get_filtered_tracks(self, title, type):
        # print(type)
        filtered_tracks =[]
        album = False
        track_bool = False
        artist= False
        genre = False
        if type == 'track':
            track = True
        elif type == 'artist':
            artist = True
        elif type == 'album':
            album = True
        elif type == 'genre':
            genre = True    
        else:
            album = True
            track_bool = True
            artist= True
        for track in self.__tracks:
            if album and track.album and title in track.album.title.lower():
                filtered_tracks.append(track)
            elif artist and track.artist and title in track.artist.full_name.lower():
                filtered_tracks.append(track)
            elif track_bool and title in track.title.lower():
                filtered_tracks.append(track)
            elif genre and title in [genre.name.lower() for genre in track.genres]:
                filtered_tracks.append(track)
        return filtered_tracks 

    def add_review(self, review: Review):
        # call parent class first, add_review relies on implementation of code common to all derived classes
        super().add_review(review)
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

def load_tracks(album_path, track_path ,repo:MemoryRepository ):
    reader = TrackCSVReader(album_path, track_path)
    for track in reader.read_csv_files():
        repo.add_track(track)

def populate(album_path,track_path ,repo:MemoryRepository):
    load_tracks(album_path, track_path,repo)

def load_users(data_path: Path, repo: MemoryRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")
    for data_row in TrackCSVReader.read_csv_files(users_filename):
        user = User(
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_reviews(data_path: Path, repo: MemoryRepository, users):
    reviews_filename = str(Path(data_path) / "reviews.csv")
    for data_row in TrackCSVReader.read_csv_files(reviews_filename):
        review = User.add_review(
            review_text=data_row[3],
            user=users[data_row[1]],
            track=repo.get_track(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4])
        )
        repo.add_review(review)