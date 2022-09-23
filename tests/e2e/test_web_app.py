import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code 
    assert response_code == 200
    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == '/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    # response = client.post(
    #     '/authentication/register',
    #     data={'user_name': user_name, 'password': password}
    # )
    # assert message in response.data
    pass

def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    # print(status_code)
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == '/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Random' in response.data


def test_login_required_to_review(client):
    response = client.post('/browse/review')
    assert response.headers['Location'] == '/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the review page.
    response = client.get('/review?track=2')

    response = client.post(
        '/review',
        data={'review': 'Who needs quarantine?', 'track_id': 2}
    )
    assert response.headers['Location'] == 'browse/track/2&view_reviews_for=2'


@pytest.mark.parametrize(('review', 'messages'), (
        ('Who thinks Trump is a f***wit?', (b'Your review must not contain profanity')),
        ('Hey', (b'Your review is too short')),
        ('ass', (b'Your review is too short', b'Your review must not contain profanity')),
))
def test_review_with_invalid_input(client, auth, review, messages):
    # Login a user.
    auth.login()

    # Attempt to review on an track.
    response = client.post(
        '/review',
        data={'review': review, 'track_id': 2}
    )
    # Check that supplying invalid review text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_tracks_with_review(client):
    # Check that we can retrieve the tracks page.
    response = client.get('/browse/track/view_reviews_for=2')
    assert response.status_code == 200

    # Check that all reviews for specified track are included on the page.
    assert b'Oh no, COVID-19 has hit New Zealand' in response.data
    assert b'Yeah Freddie, bad news' in response.data


def test_tracks_with_genre(client):
    # Check that we can retrieve the tracks page.
    response = client.get('/tracks_by_genre?genre=Pop')
    assert response.status_code == 200

    # Check that all tracks genreged with 'Health' are included on the page.
    assert b'tracks genreged by Health' in response.data
    assert b'Coronavirus: First case of virus in New Zealand' in response.data
    assert b'Covid 19 coronavirus: US deaths double in two days, Trump says quarantine not necessary' in response.data
