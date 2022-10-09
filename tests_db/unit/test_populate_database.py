from sqlalchemy import select, inspect

from music.adapters.orm import metadata

def test_database_populate_inspect_table_names(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['albums', 'artists', 'genres', 'reviews', 'track_genres', 'tracks', 'user_tracks', 'users']

def test_database_populate_select_all_genres(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_genres_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        # query for records in table genres
        select_statement = select([metadata.tables[name_of_genres_table]])
        result = connection.execute(select_statement)

        all_genre_names = []
        for row in result:
            all_genre_names.append(row['genre_name'])

        assert all_genre_names == ['Avant-Garde', 'Jazz', 'Pop', 'Folk', 'Hip-Hop', 'Punk', 'Post-Rock', 'Field Recordings', 'Noise', '	Loud-Rock', 'Psych-Rock', 'Experimental Pop', 'Singer-Songwriter']

def test_database_populate_select_all_users(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[7]

    with database_engine.connect() as connection:
        # query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])

        assert all_users == ['thorke', 'fmercury']

def test_database_populate_select_all_reviews(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[3]

    with database_engine.connect() as connection:
        # query for records in table reviews
        select_statement = select([metadata.tables[name_of_reviews_table]])
        result = connection.execute(select_statement)

        all_reviews = []
        for row in result:  
            all_reviews.append((row['id'], row['user_id'], row['track_id'], row['review']))

        assert all_reviews == [(1, 2, 2, 'Good song'),
                                (2, 1, 2, 'Annoying'),
                                (3, 2, 2, 'My favourite!')]

def test_database_populate_select_all_tracks(database_engine):

    # Get table information
    inspector = inspect(database_engine)
    name_of_tracks_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        # query for records in table tracks
        select_statement = select([metadata.tables[name_of_tracks_table]])
        result = connection.execute(select_statement)

        all_tracks = []
        for row in result:
            all_tracks.append((row['id'], row['title']))

        nr_tracks = len(all_tracks)
        assert nr_tracks == 6

        assert all_tracks[0] == (2, 'Food')


