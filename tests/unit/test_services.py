from datetime import date

import pytest

from music.authentication.services import AuthenticationException
from music.track import services as track_services
from music.authentication import services as auth_services
from music.track.services import NonExistentTrackException

#cool feature
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
    assert next(
        (dictionary['liked_track'] for dictionary in liked_tracks if dictionary['liked_track'] == track),
        None) is not None

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


def test_can_add_review(in_memory_repo):
    track_id = 2
    review_text = 'This song is great!'
    user_name = 'fmercury'

    # Call the service layer to add the review.
    track_services.add_review(track_id, review_text, user_name, in_memory_repo)

    # Retrieve the reviews for the track from the repository.
    reviews_as_dict = track_services.get_reviews_for_track(track_id, in_memory_repo)

    # Check that the reviews include a review with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


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

    track_as_dict = track_services.get_track(track_id, in_memory_repo)

    assert track_as_dict['id'] == track_id
    assert track_as_dict['date'] == date.fromisoformat('2020-02-29')
    assert track_as_dict['title'] == 'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary'
    #assert track_as_dict['first_para'] == 'US President Trump tweeted on Saturday night (US time) that he has asked the Centres for Disease Control and Prevention to issue a ""strong Travel Advisory"" but that a quarantine on the New York region"" will not be necessary.'
    assert track_as_dict['hyperlink'] == 'https://www.nzherald.co.nz/world/news/track.cfm?c_id=2&objectid=12320699'
    assert track_as_dict['image_hyperlink'] == 'https://www.nzherald.co.nz/resizer/159Vi4ELuH2fpLrv1SCwYLulzoM=/620x349/smart/filters:quality(70)/arc-anglerfish-syd-prod-nzme.s3.amazonaws.com/public/XQOAY2IY6ZEIZNSW2E3UMG2M4U.jpg'
    assert len(track_as_dict['reviews']) == 0

    tag_names = [dictionary['name'] for dictionary in track_as_dict['tags']]
    assert 'World' in tag_names
    assert 'Health' in tag_names
    assert 'Politics' in tag_names


def test_cannot_get_track_with_non_existent_id(in_memory_repo):
    track_id = 7

    # Call the service layer to attempt to retrieve the track.
    with pytest.raises(track_services.NonExistenttrackException):
        track_services.get_track(track_id, in_memory_repo)


# def test_get_first_track(in_memory_repo):
#     track_as_dict = track_services.get_first_track(in_memory_repo)

#     assert track_as_dict['id'] == 1


# def test_get_last_track(in_memory_repo):
#     track_as_dict = track_services.get_last_track(in_memory_repo)

#     assert track_as_dict['id'] == 6


# def test_get_tracks_by_date_with_one_date(in_memory_repo):
#     target_date = date.fromisoformat('2020-02-28')

#     tracks_as_dict, prev_date, next_date = track_services.get_tracks_by_date(target_date, in_memory_repo)

#     assert len(tracks_as_dict) == 1
#     assert tracks_as_dict[0]['id'] == 1

#     assert prev_date is None
#     assert next_date == date.fromisoformat('2020-02-29')


# def test_get_tracks_by_date_with_multiple_dates(in_memory_repo):
#     target_date = date.fromisoformat('2020-03-01')

#     tracks_as_dict, prev_date, next_date = news_services.get_tracks_by_date(target_date, in_memory_repo)

#     # Check that there are 3 tracks dated 2020-03-01.
#     assert len(tracks_as_dict) == 3

#     # Check that the track ids for the the tracks returned are 3, 4 and 5.
#     track_ids = [track['id'] for track in tracks_as_dict]
#     assert set([3, 4, 5]).issubset(track_ids)

#     # Check that the dates of tracks surrounding the target_date are 2020-02-29 and 2020-03-05.
#     assert prev_date == date.fromisoformat('2020-02-29')
#     assert next_date == date.fromisoformat('2020-03-05')


# def test_get_tracks_by_date_with_non_existent_date(in_memory_repo):
#     target_date = date.fromisoformat('2020-03-06')

#     tracks_as_dict, prev_date, next_date = news_services.get_tracks_by_date(target_date, in_memory_repo)

#     # Check that there are no tracks dated 2020-03-06.
#     assert len(tracks_as_dict) == 0


def test_get_tracks_by_id(in_memory_repo):
    target_track_ids = [5, 6, 7, 8]
    tracks_as_dict = track_services.get_tracks_by_id(target_track_ids, in_memory_repo)

    # Check that 2 tracks were returned from the query.
    assert len(tracks_as_dict) == 2

    # Check that the track ids returned were 5 and 6.
    track_ids = [track['id'] for track in tracks_as_dict]
    assert set([5, 6]).issubset(track_ids)


def test_get_reviews_for_track(in_memory_repo):
    reviews_as_dict = track_services.get_reviews_for_track(1, in_memory_repo)

    # Check that 2 reviews were returned for track with id 1.
    assert len(reviews_as_dict) == 2

    # Check that the reviews relate to the track whose id is 1.
    track_ids = [review['track_id'] for review in reviews_as_dict]
    track_ids = set(track_ids)
    assert 1 in track_ids and len(track_ids) == 1


def test_get_reviews_for_non_existent_track(in_memory_repo):
    with pytest.raises(NonExistentTrackException):
        reviews_as_dict = track_services.get_reviews_for_track(7, in_memory_repo)


def test_get_reviews_for_track_without_reviews(in_memory_repo):
    reviews_as_dict = track_services.get_reviews_for_track(2, in_memory_repo)
    assert len(reviews_as_dict) == 0

