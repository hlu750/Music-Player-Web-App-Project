from datetime import date
import math
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from sqlalchemy.orm import scoped_session
from  sqlalchemy.sql.expression import func, select

from music.domainmodel.user import User
from music.domainmodel.track import Track, Review
from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.genre import Genre
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

    def get_user(self, user_name: str) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter(User._User__user_name == user_name).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user
<<<<<<< HEAD
    
=======

    def get_number_of_users(self):
        number_of_users = self._session_cm.session.query(User).count()
        return number_of_users

>>>>>>> 71ecd45de23997633594200c89a43e9c1173e573
    def add_track(self, track: Track):
        with self._session_cm as scm:
            scm.session.add(track)
            scm.commit()
<<<<<<< HEAD
=======

>>>>>>> 71ecd45de23997633594200c89a43e9c1173e573
    def add_album(self, album: Album):
        with self._session_cm as scm:
            scm.session.add(album)
            scm.commit()
<<<<<<< HEAD
    def add_liked_track(self, track):
        pass
    def get_liked_tracks(self, user: User):
        pass 
=======

>>>>>>> 71ecd45de23997633594200c89a43e9c1173e573
    def get_track(self, id: int) -> Track:
        track = None
        try:
            track = self._session_cm.session.query(Track).filter(Track._Track__id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return track
<<<<<<< HEAD
    def get_filtered_tracks(self, title, type):
        pass
=======

    def get_random_track(self): # session.query(MyModel).order_by(func.rand()).first()
        track = None
        try:
            track = self._session_cm.session.query(Track).order_by(func.rand()).first()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return track
        
    def get_track_by_genre(self, target_genre: Genre) -> List[Track]:
        # if target_genre is None:
        #     tracks = self._session_cm.session.query(Track).all()
        #     return tracks
        # else:
        #     tracks = self._session_cm.session.query(Track).filter(Track._Track__genre == target_genre).all()
        #     return tracks  
        pass 
        
    def get_filtered_tracks(self, title, type) -> List[Track]:
        title = title.lower()
        filtered_tracks =[]
        if type == 'track':
            filtered_tracks = self._session_cm.session.query(Track).filter(Track._Track__title == title).all()
        elif type == 'artist':
            filtered_tracks = self._session_cm.session.query(Track).filter(Track._Track__artist == title).all()
        elif type == 'album':
            filtered_tracks = self._session_cm.session.query(Track).filter(Track._Track__album == title).all()
        elif type == 'genre':
            filtered_tracks = self._session_cm.session.query(Track).filter(title in Track._Track__genre).all() 
        else:                           
            pass
        return filtered_tracks 

    def get_number_of_tracks(self) -> int:
        number_of_tracks = self._session_cm.session.query(Track).count()
        return number_of_tracks

    def get_tracks_by_id(self, id_list):
        tracks = self._session_cm.session.query(Track).filter(Track._Track__id.in_(id_list)).all()
        return tracks

    def get_tracks_by_quantity(self, startIndex, quantity):
        number_of_tracks = self._session_cm.session.query(Track).count()
        tracks = self._session_cm.session.query(Track).all()
        if startIndex >= 0 and startIndex + quantity < number_of_tracks:
            return tracks[startIndex: startIndex + quantity]
        elif startIndex >= 0:
            return tracks[startIndex:]
        else:
            return None

    def get_number_of_pages(self, quantity):
        number_of_tracks = self._session_cm.session.query(Track).count()
        number_of_pages = math.ceil(number_of_tracks / quantity)
        return number_of_pages

>>>>>>> 71ecd45de23997633594200c89a43e9c1173e573
    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews
    def get_number_of_tracks(self):
        pass
    def get_number_of_users(self):
        pass
    def get_random_track(self):
        pass
    def get_track_by_genre(self, target_genre: Genre) -> List[Track]:
        pass

    def get_tracks_by_id(self, id_list):
        pass
    def get_tracks_by_quantity( self, startIndex, quantity):
        pass
    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def add_liked_track(self, track):
        super().add_liked_track(track)
        with self._session_cm as scm:
            scm.session.add(track)
            scm.commit()

    def get_liked_tracks(self, user):
        liked_tracks = self._session_cm.session.query(User._User__liked_tracks).all()
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
