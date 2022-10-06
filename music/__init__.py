"""Initialize Flask app."""

from pathlib import Path

from flask import Flask, render_template

# TODO: Access to the tracks should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
# from music.domainmodel.track import Track
from music.domainmodel.model import Track
from music.adapters import memory_repository, database_repository, repository_populate
from music.adapters.memory_repository import MemoryRepository
from music.adapters.orm import metadata, map_model_to_tables
import music.adapters.repository as repo
# TODO: Access to the tracks should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool
def create_some_track():
    some_track = Track(1, "Heat Waves")
    some_track.track_duration = 250
    some_track.track_url = 'https://spotify/track/1'
    return some_track


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object('config.Config')
    data_path = Path('music') / 'adapters' / 'data'
    # print(data_path)
    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    if app.config['REPOSITORY'] == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo.repo_instance = MemoryRepository()
        # fill the content of the repository from the provided csv files (has to be done every time we start app!)
        database_mode = False
        repository_populate.populate(data_path, repo.repo_instance, database_mode)
    elif app.config['REPOSITORY'] == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']
        print("helloo")
        # We create a comparatively simple SQLite database, which is based on a single file (see .env for URI).
        # For example the file database could be located locally and relative to the application in covid-19.db,
        # leading to a URI of "sqlite:///covid-19.db".
        # Note that create_engine does not establish any actual DB connection directly!
        database_echo = app.config['SQLALCHEMY_ECHO']
        # Please do not change the settings for connect_args and poolclass!
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=database_echo)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = database_repository.SqlAlchemyRepository(session_factory)

        if app.config['TESTING'] == 'True' or len(database_engine.table_names()) == 0:
                print("REPOPULATING DATABASE...")
                # For testing, or first-time use of the web application, reinitialise the database.
                clear_mappers()
                metadata.create_all(database_engine)  # Conditionally create database tables.
                for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                    database_engine.execute(table.delete())

                # Generate mappings that map domain model classes to the database tables.
                print("pls")
                map_model_to_tables()
                print("bn")
                database_mode = True
                repository_populate.populate(data_path, repo.repo_instance, database_mode)
                print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            print("pls")
            map_model_to_tables()
            # print("omg")

    # album_file = "raw_albums_excerpt.csv"
    # track_file = "raw_tracks_excerpt.csv"
    # repo.repo_instance = MemoryRepository()
    # populate(data_path,album_file,track_file, repo.repo_instance)
    app.debug = True
    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)
    
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

        from .profile import profile
        app.register_blueprint(profile.profile_blueprint)

        from .track import track
        app.register_blueprint(track.track_blueprint)

        @app.before_request
        def before_flask_http_request_function():
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.reset_session()

        # Register a tear-down method that will be called after each request has been processed.
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if isinstance(repo.repo_instance, database_repository.SqlAlchemyRepository):
                repo.repo_instance.close_session()

    return app
