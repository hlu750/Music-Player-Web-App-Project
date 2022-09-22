import pytest
import os

from music.domainmodel.artist import Artist
from music.domainmodel.track import Track, Review
from music.domainmodel.genre import Genre
# from music.domainmodel.track import Review
from music.domainmodel.album import Album
from music.domainmodel.user import User
from music.adapters.csvdatareader import TrackCSVReader

from music.authentication.services import AuthenticationException
from music.track import services as track_services
from music.authentication import services as auth_services
from music.track.services import NonExistentTrackException

#cool feature tests in the other files


class TestUser:

    def test_liked_song_methods(self):
        """ Test add_liked_track() method """
        user1 = User(7232, 'pedri', 'pedri9281')
        track1 = Track(1, 'Shivers')
        track2 = Track(2, 'Heat Waves')
        track3 = Track(3, 'Bad Habit')

        user1.add_liked_track(track1)
        user1.add_liked_track(track2)
        user1.add_liked_track(track3)
        assert user1.liked_tracks == [track1, track2, track3]

        track1_copy = Track(1, 'Shivers')
        user1.add_liked_track(track1_copy)
        assert len(user1.liked_tracks) == 3

def test_can_add_liked_song(in_memory_repo):
    track_id = 2
    user_name = 'fmercury'
    prev_track, track, next_track = track_services.get_track(track_id, in_memory_repo)
    # Call the service layer to add the review.
    track_services.add_liked_track(track, user_name, in_memory_repo)
    
    # Retrieve the reviews for the track from the repository.
    liked_tracks = track_services.get_liked_tracks(user_name, in_memory_repo)

    # Check that the reviews include a review with the new review text.
    # assert (track in liked_tracks.values()) 
    # assert next(
    #     (dictionary['track'] for dictionary in liked_tracks if dictionary['track'] == track),
    #     None) is not None
    assert next((liked_track for liked_track in liked_tracks if liked_track == track), None)