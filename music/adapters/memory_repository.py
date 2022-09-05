from pathlib import Path
import random
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
from bisect import bisect, bisect_left, insort_left
class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self.__tracks = list()
        self.__track_index = dict()
        self.__tags = list()
        self.__users = list()
        self.__comments = list()
        # t = Track()

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, user_name) -> User:
        return next((user for user in self.__users if user.user_name == user_name), None)
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

def load_tracks(album_path, track_path ,repo:MemoryRepository ):
 
    reader = TrackCSVReader(album_path, track_path)
    for track in reader.read_csv_files():
        repo.add_track(track)
    # print(repo.tracks)
    # print(repo.track_index)
    # print(repo.get_random_track())

def populate(album_path,track_path ,repo:MemoryRepository):
    load_tracks(album_path, track_path,repo)
    



