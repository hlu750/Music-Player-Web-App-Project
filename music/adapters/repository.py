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
    def get_number_of_users(self):
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

    # @abc.abstractmethod
    # def add_comment(self, comment: Comment):
    #     """ Adds a Comment to the repository.

    #     If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
    #     RepositoryException and doesn't update the repository.
    #     """
    #     if comment.user is None or comment not in comment.user.comments:
    #         raise RepositoryException('Comment not correctly attached to a User')
    #     if comment.article is None or comment not in comment.article.comments:
    #         raise RepositoryException('Comment not correctly attached to an Article')

    # @abc.abstractmethod
    # def get_comments(self):
    #     """ Returns the Comments stored in the repository. """
    #     raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_tracks(self) -> int:
        """ Returns the number of Articles in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_id(self, id_list):
        """ Returns a list of Articles, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError