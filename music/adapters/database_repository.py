from datetime import date
import math
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from  sqlalchemy.sql.expression import func, select

# from music.domainmodel.user import User
# from music.domainmodel.track import Track, Review, Genre
# from music.domainmodel.artist import Artist
# from music.domainmodel.album import Album
# from music.domainmodel.genre import Genre
from music.domainmodel.model import Track, Genre, Review,Album, User, Artist
from music.adapters.repository import AbstractRepository

class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()
    
    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, user_name: str) -> User: #works
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def get_number_of_users(self):
        number_of_users = self._session_cm.session.query(User).count()
        return number_of_users
    
    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.merge(track)
            scm.commit()

    def add_many_genres(self, genres: List[Genre]):
        with self._session_cm as scm:
            scm.session.add_all(genres)
            scm.commit()
    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.merge(genre)
            scm.commit()
    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.merge(album)
            scm.commit()
    def get_track(self, id: int) -> Track: #works
        track = None
        prev_track = None
        next_track = None
        try:
            
            track = self._session_cm.session.query(Track).filter(Track._Track__track_id == id).one()
            
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        try:
            prev_track = self._session_cm.session.query(Track).order_by(Track._Track__track_id.desc()).filter(Track._Track__track_id < id).first()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        try: 
            next_track = self._session_cm.session.query(Track).order_by(Track._Track__track_id.asc()).filter(Track._Track__track_id > id).first()
        except NoResultFound:
            pass
        return prev_track,track,next_track

    @property
    def tracks(self) -> List[Track]:
        return self._session_cm.session.query(Track).all()

    @property
    def track_index(self) -> dict:
    #     track_index = self._session_cm.session.query(INDEX(Track))
    #     return [dict(index) for index in track_index]
        pass

    def get_random_track(self): # session.query(MyModel).order_by(func.rand()).first()
        track = None
        try:
            track = self._session_cm.session.query(Track).order_by(func.random()).first()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return track
        
    def get_track_by_genre(self, genre) -> List[Track]:
        genres = self._session_cm.session.query(Genre).filter(Genre._Genre__name.contains(genre)).all() 
        if len(genres) == 0:
            return genres
        tracks = self._session_cm.session.query(Track).filter(Track._Track__genres.contains(genres[0])).all() 
        return tracks

    def get_track_by_title(self, title) -> List[Track]:
        tracks = self._session_cm.session.query(Track).filter(Track._Track__title.contains(title)).all() 
        return tracks

    def get_track_by_artist(self, artist) -> List[Track]:
        artists = self._session_cm.session.query(Artist).filter(Artist._Artist__full_name.contains(artist)).all() 
        if len(artists) ==0:
            return artists
        
        tracks = self._session_cm.session.query(Track).filter(Track._Track__artist == artists[0]).all() 
        return tracks

    def get_track_by_album(self, album) -> List[Track]:
        albums = self._session_cm.session.query(Album).filter(Album._Album__title.contains(album)).all() 
        if len(albums) ==0:
            return albums
        tracks = self._session_cm.session.query(Track).filter(Track._Track__album == (albums[0])).all() 
        return tracks

    def get_filtered_tracks(self, title, type) -> List[Track]:
        title = title.lower()
        filtered_tracks =[]
        if type == 'track':
            filtered_tracks = self.get_track_by_title(title)
        elif type == 'artist': 
            filtered_tracks = self.get_track_by_artist(title)
        elif type == 'album':
            filtered_tracks = self.get_track_by_album(title)
        elif type == 'genre': 
            filtered_tracks = self.get_track_by_genre(title)
        else:                           
            filtered_tracks = self.get_track_by_title(title)
            filtered_tracks += self.get_track_by_artist(title)
            filtered_tracks += self.get_track_by_album(title)
            filtered_tracks += self.get_track_by_genre(title)

        return filtered_tracks 

    def get_number_of_tracks(self) -> int:
        number_of_tracks = self._session_cm.session.query(Track).count()
        return number_of_tracks

    def get_tracks_by_id(self, id):
        tracks = self._session_cm.session.query(Track).filter(Track._Track__track_id == id).first()
        return tracks

    def get_tracks_by_quantity(self, startIndex, quantity): #works
        number_of_tracks = self._session_cm.session.query(Track).count()
        tracks = self._session_cm.session.query(Track).all()
        if startIndex >= 0 and startIndex + quantity < number_of_tracks:
            return tracks[startIndex: startIndex + quantity]
        elif startIndex >= 0:
            return tracks[startIndex:]
        else:
            return None

    def get_number_of_pages(self, quantity): #works
        number_of_tracks = self._session_cm.session.query(Track).count()
        number_of_pages = math.ceil(number_of_tracks / quantity)
        return number_of_pages

    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_review(self, review: Review): #works
        # super().add_review(review)
        if review.user != None:
            with self._session_cm as scm:
                scm.session.merge(review)
                scm.commit()

    def get_number_of_reviews(self) -> int:
        number_of_reviews = self._session_cm.session.query(Review).count()
        return number_of_reviews

    def add_liked_track(self, track: Track): #works
        super().add_liked_track(track)
        with self._session_cm as scm:
            scm.session.merge(track)
            scm.commit()

    def get_liked_tracks(self, user: User): #works 
        liked_tracks = self._session_cm.session.query(Track).filter(Track._Track__track_id.in_(User._User__liked_tracks)).all()
        return liked_tracks


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()