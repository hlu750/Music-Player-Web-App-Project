# from music.domainmodel.artist import Artist
# # from music.domainmodel.genre import Genre
# from music.domainmodel.album import Album
# from typing import List
# # from music.domainmodel.user import User

# # from music.domainmodel.review import Review
# from datetime import datetime
# class Track:
#     def __init__(self, track_id: int, track_title: str):
#         if type(track_id) is not int or track_id < 0:
#             raise ValueError
#         self.__track_id = track_id
       
#         self.__title = None
#         if type(track_title) is str:
#             self.__title = track_title.strip()

#         self.__artist = None
#         self.__album: Album | None = None
#         self.__track_url: str | None = None
#         # duration in seconds
#         self.__track_duration: int | None = None
#         self.__genres: List[Genre] = list()
        
#         self.__reviews: list = []

#     @property
#     def track_id(self) -> int:
#         return self.__track_id

#     @property
#     def title(self) -> str:
#         return self.__title

#     @title.setter
#     def title(self, book_title: str):
#         self.__title = None
#         if type(book_title) is str and book_title.strip() != '':
#             self.__title = book_title.strip()

#     @property
#     def artist(self) -> Artist:
#         return self.__artist

#     @artist.setter
#     def artist(self, new_artist):
#         if isinstance(new_artist, Artist):
#             self.__artist = new_artist
#         else:
#             self.__artist = None

#     @property
#     def album(self) -> Album:
#         return self.__album

#     @album.setter
#     def album(self, new_album):
#         if isinstance(new_album, Album):
#             self.__album = new_album
#         else:
#             self.__album = None

#     @property
#     def track_url(self) -> str:
#         return self.__track_url

#     @track_url.setter
#     def track_url(self, new_track_url: str):
#         if type(new_track_url) is str:
#             self.__track_url = new_track_url.strip()
#         else:
#             self.__track_url = None

#     @property
#     def track_duration(self) -> int:
#         return self.__track_duration

#     @track_duration.setter
#     def track_duration(self, new_duration: int):
#         self.__track_duration = None
#         if type(new_duration) is int and new_duration >= 0:
#             self.__track_duration = new_duration
#         else:
#             raise ValueError

#     @property
#     def genres(self) -> list:
#         return iter(self.__genres)
#     @property 
#     def reviews(self) -> list:
#         return self.__reviews
#     def add_review(self, review):
#         if type(review) is Review and review not in self.__reviews:
#             self.__reviews.append(review)
#         else:
#             print("error when adding review to track") 
#     def add_genre(self, new_genre):
#         if not isinstance(new_genre, Genre) or new_genre in self.__genres:
#             return
#         self.__genres.append(new_genre)

#     def __repr__(self):
#         return f"<Track {self.title}, track id = {self.track_id}>"

#     def __eq__(self, other):
#         if not isinstance(other, self.__class__):
#             return False
#         return self.track_id == other.track_id

#     def __lt__(self, other):
#         if not isinstance(other, self.__class__):
#             return True
#         return self.track_id < other.track_id

#     def __hash__(self):
#         return hash(self.track_id)
# class Review:

#     def __init__(self, track: Track, review_text: str, rating: int, user_name:str):
#         self.__track = None
#         if (isinstance(user_name, str)):
#             self.__user_name = user_name
#         else:
#             self.__user_name = None
#         if isinstance(track, Track):
#             self.__track = track

#         self.__review_text = 'N/A'
#         if isinstance(review_text, str):
#             self.__review_text = review_text.strip()

#         if isinstance(rating, int) and 1 <= rating <= 5:
#             self.__rating = rating
#         else:
#             raise ValueError('Invalid value for the rating.')

#         self.__timestamp = datetime.now()
#     @property
#     def username(self):
#         return self.__user_name
        
#     @property
#     def track(self) -> Track:
#         return self.__track

#     @property
#     def review_text(self) -> str:
#         return self.__review_text

#     @review_text.setter
#     def review_text(self, new_text):
#         if type(new_text) is str:
#             self.__review_text = new_text.strip()
#         else:
#             self.__review_text = None

#     @property
#     def rating(self) -> int:
#         return self.__rating

#     @rating.setter
#     def rating(self, new_rating: int):
#         if isinstance(new_rating, int) and 1 <= new_rating <= 5:
#             self.__rating = new_rating
#         else:
#             self.__rating = None
#             raise ValueError("Wrong value for the rating")

#     @property
#     def timestamp(self) -> datetime:
#         return self.__timestamp

#     def __eq__(self, other):
#         if not isinstance(other, self.__class__):
#             return False
#         return other.track == self.track and other.review_text == self.review_text and other.rating == self.rating and other.timestamp == self.timestamp

#     def __repr__(self):
#         return f'<Review of track {self.track}, rating = {self.rating}, review_text = {self.review_text}>'
# class Genre:

#     def __init__(self, genre_id: int, genre_name: str):
        
#         if type(genre_id) is not int or genre_id < 0:
#             raise ValueError('Genre ID should be an integer!')
#         self.__genre_id = genre_id
#         self.__tracks : List[Track.Track] = list()
#         if type(genre_name) is str:
#             self.__name = genre_name.strip()
#         else:
#             self.__name = None

#     @property
#     def genre_id(self) -> int:
#         return self.__genre_id

#     @property
#     def name(self) -> str:
#         return self.__name

#     @name.setter
#     def name(self, name: str):
#         self.__name = None
#         if type(name) is str:
#             name = name.strip()
#             if name != '':
#                 self.__name = name
#     @property
#     def tracks(self):
#         return iter(self.__tracks)
    
#     def is_applied_to(self, track: Track) -> bool:
#         return track in self.__tracks
    
#     def add_track(self, track: Track):
#         self.__tracks.append(track)
#     def __repr__(self) -> str:
#         return f'<Genre {self.name}, genre id = {self.genre_id}>'

#     def __eq__(self, other) -> bool:
#         if not isinstance(other, self.__class__):
#             return False
#         return self.genre_id == other.genre_id

#     def __lt__(self, other):
#         if not isinstance(other, self.__class__):
#             return True
#         return self.genre_id < other.genre_id

#     def __hash__(self):
#         return hash(self.genre_id)

# class ModelException(Exception):
#     pass

# def make_tag_association(track: Track, genre: Genre):
#     if genre.is_applied_to(track):
#         raise ModelException(f'Tag {genre.name} already applied to Article "{track.title}"')
#     track.add_genre(genre)
#     genre.add_track(track)