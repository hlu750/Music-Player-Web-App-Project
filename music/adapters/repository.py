import abc
from typing import List
from music.domainmodel.track import Track
from music.domainmodel.album import  Album
from music.domainmodel.artist import Artist
from music.domainmodel.genre  import Genre
from music.domainmodel.playlist  import PlayList
from music.domainmodel.track import Review
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
    def add_album(self, album:Album):
        raise NotImplementedError
    @abc.abstractmethod
    def get_track(self, id:int):
        raise NotImplementedError
        
    @abc.abstractmethod
    def tracks(self) -> List[Track]:
        raise NotImplementedError
    @abc.abstractmethod
    def track_index(self) -> dict:
        raise NotImplementedError
        
    @abc.abstractmethod
    def get_random_track(self):
        raise NotImplementedError
        
    @abc.abstractmethod
    def get_track_by_genre(self, target_genre: Genre) -> List[Track]:
        raise NotImplementedError  

    @abc.abstractmethod
    def get_number_of_pages(self, quantity):
        raise NotImplementedError

    @abc.abstractmethod
    def get_filtered_tracks(self, title, type) -> List[Track]:
        raise NotImplementedError
    # @abc.abstractmethod
    # def add_tag(self, tag: Genre):
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_genres(self) -> List[Genre]:
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def add_review(self, review: review):
    #     """ Adds a review to the repository.

    #     If the review doesn't have bidirectional links with an track and a User, this method raises a
    #     RepositoryException and doesn't update the repository.
    #     """
    #     if review.user is None or review not in review.user.reviews:
    #         raise RepositoryException('review not correctly attached to a User')
    #     if review.track is None or review not in review.track.reviews:
    #         raise RepositoryException('review not correctly attached to an track')

    # @abc.abstractmethod
    # def get_reviews(self):
    #     """ Returns the reviews stored in the repository. """
    #     raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_tracks(self) -> int:
        """ Returns the number of tracks in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_tracks_by_id(self, id_list):
        """ Returns a list of tracks, whose ids match those in id_list, from the repository.

        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    
    # @abc.abstractmethod
    # def add_genre(self, genre: Genre):
    #     """ Adds a genre to the repository. """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def add_review(self, review: Review):
    #     """ Adds a review to the repository.

    #     If the review doesn't have bidirectional links with an track and a User, this method raises a
    #     RepositoryException and doesn't update the repository.
    #     """
    #     if review.user is None or review not in review.user.reviews:
    #         raise RepositoryException('review not correctly attached to a User')
    #     if review.track is None or review not in review.track.reviews:
    #         raise RepositoryException('review not correctly attached to an track')

    # @abc.abstractmethod
    # def get_reviews(self):
    #     """ Returns the reviews stored in the repository. """
    #     raise NotImplementedError
    @abc.abstractmethod
    def get_tracks_by_quantity(self, startIndex, quantity):
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a review to the repository.

        If the review doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.track is None:
            raise RepositoryException('review not correctly attached to a User')
    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the reviews stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_liked_track(self, track):
        print("hello? why?")
        raise NotImplementedError

    @abc.abstractmethod
    def get_liked_tracks(self, user):
        raise NotImplementedError
    
    
    
