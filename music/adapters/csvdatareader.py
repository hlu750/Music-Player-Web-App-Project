from cgi import print_form
from math import frexp
import os
import csv
import ast
from tokenize import String

# from music.domainmodel.model import make_genre_association, make_review, ModelException
# from music.domainmodel.artist import Artist
# from music.domainmodel.album import Album
# from music.domainmodel.track import Track ,make_tag_association, Genre
# # from music.domainmodel.genre import Genre
# from music.domainmodel.user import User
from music.domainmodel.model import Track, Genre,Album, User, Artist, Review, make_comment
from pathlib import Path
from utils import get_project_root
from datetime import date, datetime
from werkzeug.security import generate_password_hash

from music.adapters.repository import AbstractRepository
class TrackCSVReader:

    def __init__(self, albums_csv_file: str, tracks_csv_file: str):
        
        current_path = os.path.dirname(__file__)
        
        # print(type(albums_csv_file))
        if type(albums_csv_file) is str:
           
            self.__albums_csv_file = str(get_project_root() / "tests" / "data" / albums_csv_file)
            self.__albums_csv_file = albums_csv_file
          
        else:
            raise TypeError('albums_csv_file should be a type of string')

        if type(tracks_csv_file) is str:
            self.__tracks_csv_file = str(get_project_root() / "tests" / "data" / tracks_csv_file)
            self.__tracks_csv_file = tracks_csv_file
            # self.__tracks_csv_file = str(Path('covid' / 'adapters' / 'data') / tracks_csv_file)
        else:
            raise TypeError('tracks_csv_file should be a type of string')

        # List of unique tracks
        self.__dataset_of_tracks = []
        # Set of unique artists
        self.__dataset_of_artists = set()
        # Set of unique albums
        self.__dataset_of_albums = set()
        # Set of unique genres
        self.__dataset_of_genres = set()

    @property
    def dataset_of_tracks(self) -> list:
        return self.__dataset_of_tracks

    @property
    def dataset_of_albums(self) -> set:
        return self.__dataset_of_albums

    @property
    def dataset_of_artists(self) -> set:
        return self.__dataset_of_artists

    @property
    def dataset_of_genres(self) -> dict:
        return self.__dataset_of_genres

    def read_albums_file_as_dict(self) -> dict:
        
        album_dict = dict()
        # encoding of unicode_escape is required to decode successfully
        with open(self.__albums_csv_file, encoding="unicode_escape") as album_csv:
           
            reader = csv.DictReader(album_csv)
            for row in reader:
                album_id = int(row['album_id']) if row['album_id'].isdigit() else row['album_id']
                if type(album_id) is not int:
                    print(f'Invalid album_id: {album_id}')
                    continue
                
                album = create_album_object(row)
                album_dict[album_id] = album
        print("2")
        return album_dict
    def read_artist_file_as_dict(self) -> dict:
        artist_dict = dict()
        # encoding of unicode_escape is required to decode successfully
        with open(self.__tracks_csv_file, encoding="unicode_escape") as artist_csv:
            reader = csv.DictReader(artist_csv)
            for row in reader:
                artist_id = int(row['artist_id']) if row['artist_id'].isdigit() else row['artist_id']
                if type(artist_id) is not int:
                    print(f'Invalid artist_id: {artist_id}')
                    continue
                artist = create_artist_object(row)
                artist_dict[artist_id] = artist
        # print("2")
        return artist_dict
    def read_tracks_file(self):
        
        track_rows = []
        # encoding of unicode_escape is required to decode successfully
        with open(self.__tracks_csv_file, encoding='unicode_escape') as track_csv:
            reader = csv.DictReader(track_csv)
            for track_row in reader:
                track_rows.append(track_row)
        # print(track_rows)
        return track_rows

    def read_csv_files(self):
        
        # key is album_id
        track_rows: list = self.read_tracks_file()

        albums_dict: dict = self.read_albums_file_as_dict()
        
        # list of track csv rows, not track objects
        
        artist_dict: dict = self.read_artist_file_as_dict()
        # Make sure re-initialize to empty list, so that calling this function multiple times does not create
        # duplicated dataset.
        genre_dict: dict = {}
        self.__dataset_of_tracks = []
        
        for track_row in track_rows:
            track = create_track_object(track_row)
            
            artist = create_artist_object(track_row) 
            artist_id = int(
                track_row['artist_id']) if track_row['artist_id'].isdigit() else None
            artist = artist_dict[artist_id] if artist_id in artist_dict else None
            track.artist = artist
            album_id = int(
                track_row['album_id']) if track_row['album_id'].isdigit() else None

            album = albums_dict[album_id] if album_id in albums_dict else None
            track.album = album
            # Extract track_genres attributes and assign genres to the track.
            track_genres = extract_genres(track_row)

            # print(track_genres)
            # print(track_genres)
            for genre in track_genres:
                track.add_genre(genre)
                if genre.name not in [genre.name for genre in genre_dict.keys()]:
                    
                    genre_dict[genre] = list()
                    
                genre_dict[genre].append(track.track_id)
    
            # Populate datasets for Artist and Genre
            if artist not in self.__dataset_of_artists:
                self.__dataset_of_artists.add(artist)

            if album is not None and album not in self.__dataset_of_albums:
                self.__dataset_of_albums.add(album)

            for genre in track_genres:
                if genre not in self.__dataset_of_genres:
                    self.__dataset_of_genres.add(genre)

            self.__dataset_of_tracks.append(track)
        # print(reader.__albums_csv_file)
        


        return self.__dataset_of_tracks, self.__dataset_of_albums,genre_dict
        
    def read_csv_file(filename: str):
        with open(filename, encoding='utf-8-sig') as infile:
            reader = csv.reader(infile)

            # Read first line of the the CSV file.
            headers = next(reader)

            # Read remaining rows from the CSV file.
            for row in reader:
                # Strip any leading/trailing white space from data read.
                row = [item.strip() for item in row]
                yield row

def create_track_object(track_row):
 
    track = Track(int(track_row['track_id']), track_row['track_title'])
    # print("Here")
    track.track_url = track_row['track_url']
    track_duration = round(float(
        track_row['track_duration'])) if track_row['track_duration'] is not None else None
    if type(track_duration) is int:
        track.track_duration = track_duration
    track.album = track_row['album_title']
    return track


def create_artist_object(track_row):

    artist_id = int(track_row['artist_id'])

    artist = Artist(artist_id, track_row['artist_name'])
    return artist


def create_album_object(row):
    album_id = int(row['album_id'])
    album = Album(album_id, row['album_title'])
    album.album_url = row['album_url']
    album.album_type = row['album_type']
    
    album.release_year = int(
        row['album_year_released']) if row['album_year_released'].isdigit() else None

    return album


def extract_genres(track_row: dict):
    # List of dictionaries inside the string.
    track_genres_raw = track_row['track_genres']
    # Populate genres. track_genres can be empty (None)
    # genres_dictionary ={}
    genres = []
    if track_genres_raw:
        try:
            genre_dicts = ast.literal_eval(
                track_genres_raw) if track_genres_raw != "" else []

            for genre_dict in genre_dicts:

                genre = Genre(
                    int(genre_dict['genre_id']), genre_dict['genre_title'])
                genres.append(genre)

        except Exception as e:
            print(f'Exception occurred while parsing genres: {e}')
    # print(genres)
    return genres

def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)
        # Read first line of the the CSV file.
        headers = next(reader)
        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row

    if not os.path.exists(filename):
        print(f"path {filename} does not exist!")
        return
    users_rows = []
    # encoding of unicode_escape is required to decode successfully
    with open(filename, encoding='unicode_escape') as users_csv:
        reader = csv.DictReader(users_csv)
        for user_row in reader:
            users_rows.append(users_rows)
    return users_rows


def load_tracks_and_albums(data_path:Path,repo:AbstractRepository, database_mode = bool ):
    # album_path = str(data_path /"raw_albums_excerptTest.csv")
    # track_path = str(data_path /"raw_tracks_excerptTest.csv")
    album_path = str(data_path /"raw_albums_excerpt.csv")
    track_path = str(data_path /"raw_tracks_excerpt.csv")
    # print(album_path)
    reader = TrackCSVReader(album_path, track_path)
    tracks, albums, genres = reader.read_csv_files()
    
    
    for track in tracks:
        
        repo.add_track(track)
    for genre in genres.keys():
        repo.add_genre(genre)

def load_users(data_path: Path, repo: AbstractRepository):
    users = dict()

    users_filename = str(Path(data_path) / "users.csv")

    for data_row in read_csv_file(users_filename):
        user_num  = repo.get_number_of_users()
        user = User(
            user_id=user_num + 1,
            user_name=data_row[1],
            password=generate_password_hash(data_row[2])
           
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users        


def load_reviews(data_path: Path, repo: AbstractRepository, users):
    reviews_filename = str(Path(data_path) / "reviews.csv")
    
    for data_row in read_csv_file(reviews_filename):
        # print(data_row[1])
        # print(users[data_row[1]])
        review = make_comment(
            review_text=data_row[3],
            user=users[data_row[1]],
            track=repo.get_track(int(data_row[2]))[1],
            timestamp=datetime.fromisoformat(data_row[4])
            
        )
        repo.add_review(review)

# def populate(data_path, album_path,track_path ,repo:AbstractRepository):
#     load_tracks_and_albums(album_path, track_path,repo)
#     # print (data_path )
#     # Load users into the repository.
#     users = load_users(data_path, repo) 
#     # print(users)
#     # # Load comments into the repository.
#     # load_reviews(track_path, repo, users)
