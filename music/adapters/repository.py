import abc
from typing import List
from music.domainmodel.track import Track
from music.domainmodel.album import  Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre  import Genre
from music.domainmodel.playlist  import PlayList
from music.domainmodel.review import Review
from music.domainmodel.user import User 




repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user:User):
        raise NotImplementedError
    
    @abc.abstractmethod
    def get_user(self, user_name):
        raise NotImplementedError

    @abc.abstractmethod
    def add_track(self, track:Track):
        raise NotImplementedError

    @abc.abstractmethod
    def get_track(self, id:int):
        raise NotImplementedError
        
    @abc.abstractmethod
    def get_random_track(self):
        raise NotImplementedError
        
    @abc.abstractmethod
    def get_track_by_genre(self, target_genre: Genre) -> List[Track]:
        raise NotImplementedError    