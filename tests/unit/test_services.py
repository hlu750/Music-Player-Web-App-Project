from datetime import date

import pytest

from music.authentication.services import AuthenticationException
from music.track import services as track_services
from music.authentication import services as auth_services
from music.track.services import NonExistentTrackException
from music.domainmodel.track import Track, Review
from music.domainmodel.user import User
from music.track.services import get_recommended_tracks

#cool feature
# def test_can_get_recommended_tracks(in_memory_repo):
#     track = Track(7, 'Song for testing')
#     in_memory_repo.add_liked_track(track)
#     print("test")
#     recommended_tracks, random_track = get_recommended_tracks('fmercury', in_memory_repo)
#     print("test end")
#     assert recommended_tracks is not None


def test_can_add_user(in_memory_repo):
    new_user_name = 'jzzzz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    user_name = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(user_name, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


# def test_can_add_review(in_memory_repo):
#     track_id = 2
#     review_text = 'This song is great!'
#     user_name = 'fmercury'

#     # Call the service layer to add the review.
#     track_services.add_review(track_id, review_text, user_name, in_memory_repo)
#     print("hm")
#     # Retrieve the reviews for the track from the repository.
#     reviews_as_dict = track_services.get_reviews_for_track(track_id, in_memory_repo)
#     print("hmm")
#     # Check that the reviews include a review with the new review text.
#     assert next(
#         (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
#         None) is not None


def test_cannot_add_review_for_non_existent_track(in_memory_repo):
    track_id = 7
    review_text = "Huh - what's that?"
    user_name = 'fmercury'

    # Call the service layer to attempt to add the review.
    with pytest.raises(track_services.NonExistentTrackException):
        track_services.add_review(track_id, review_text, user_name, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    track_id = 3
    review_text = 'The loonies are stripping the supermarkets bare!'
    user_name = 'gmichael'

    # Call the service layer to attempt to add the review.
    with pytest.raises(track_services.UnknownUserException):
        track_services.add_review(track_id, review_text, user_name, in_memory_repo)


def test_can_get_track(in_memory_repo):
    track_id = 2
    prev_track, track, next_track = track_services.get_track(track_id, in_memory_repo)
    prev_track2, track2, next_track2 = track_services.get_track(track_id, in_memory_repo)

    assert track2 == track


# def test_get_reviews_for_track(in_memory_repo):
#     track_id = 2
#     review_text = 'This song is great!'
#     user_name = 'fmercury'
#     track_services.add_review(track_id, review_text, user_name, in_memory_repo)
    
#     # Retrieve the reviews for the track from the repository.
#     reviews_as_dict = track_services.get_reviews_for_track(track_id, in_memory_repo)

#     # Check that 2 reviews were returned for track with id 1.
#     assert len(reviews_as_dict) == 1

#     # Check that the reviews relate to the track whose id is 1.
#     track_ids = [review['track_id'] for review in reviews_as_dict]
#     assert 2 in track_ids


def test_get_reviews_for_non_existent_track(in_memory_repo):
    with pytest.raises(NonExistentTrackException):
        reviews_as_dict = track_services.get_reviews_for_track(7, in_memory_repo)


def test_get_reviews_for_track_without_reviews(in_memory_repo):
    reviews_as_dict = track_services.get_reviews_for_track(2, in_memory_repo)
    assert len(reviews_as_dict) == 0

