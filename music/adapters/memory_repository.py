import imp
from pathlib import Path
import random
from re import T
from music.adapters.repository import AbstractRepository, RepositoryException
# from music.domainmodel.track import Track,Review,Genre
# from music.domainmodel.album import  Album
# from music.domainmodel.artist import Artist
# # from music.domainmodel.genre  import Genre
# from music.domainmodel.playlist  import PlayList
# # from music.domainmodel.track import Review
# from music.domainmodel.user import User

from .csvdatareader import TrackCSVReader, read_csv_file
from music.domainmodel.model import Track, Genre, Review,Album, User, Artist
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
        self.__liked_tracks = list()
        self.__albums = list()
        self.__album_index = dict()
        
    def add_user(self, user: User):
        # print(user.user_name)
        self.__users.append(user)
        # print(self.__users)

    def get_user(self, user_name) -> User:
        if type(user_name) == str:
            return next((user for user in self.__users if user.user_name == user_name), None)

    def get_number_of_users(self):
        return len(self.__users)

    def add_track(self, track: Track):
        insort_left(self.__tracks, track)
        self.__track_index[track.track_id] = track 
    
    def add_album(self, album: Album):
        insort_left(self.__albums, album)
        self.__album_index[album.album_id] = album

    def get_track(self, id:int) -> tuple():
        track = None
        prev_track = None
        next_track =None
       
        try:
            track = self.__track_index[id]
            track_index = self.tracks.index(track)
            prev_track = self.tracks[track_index-1] if track_index - 1 >= 0 else None 
            next_track = self.tracks[track_index + 1] if track_index + 1 < len(self.__tracks) else None
        except KeyError:
            
            pass
        return prev_track, track, next_track

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
            print(id_list)
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
        # print(type, title)
        title = title.lower()
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
        # super().add_review(review)
        if review.user != None:
            self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews

    def get_number_of_reviews(self):
        return len(self.__reviews)

    def add_liked_track(self, track):
        # call parent class first, add_review relies on implementation of code common to all derived classes
        # super().add_liked_track(track)
        self.__liked_tracks.append(track)

    def get_liked_tracks(self, user: User):
        return self.__liked_tracks

