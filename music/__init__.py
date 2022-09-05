"""Initialize Flask app."""

from flask import Flask, render_template

# TODO: Access to the tracks should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
from music.domainmodel.track import Track
from music.adapters.memory_repository import MemoryRepository, populate
import music.adapters.repository as repo
# TODO: Access to the tracks should be implemented via the repository pattern and using blueprints, so this can not
#  stay here!
def create_some_track():
    some_track = Track(1, "Heat Waves")
    some_track.track_duration = 250
    some_track.track_url = 'https://spotify/track/1'
    return some_track


def create_app():
    app = Flask(__name__)
    album_file = "raw_albums_excerpt.csv"
    track_file = "raw_tracks_excerpt.csv"
    repo.repo_instance = MemoryRepository()
    populate(album_file,track_file, repo.repo_instance)
    app.debug = True
    with app.app_context():
        from .home import home
        app.register_blueprint(home.home_blueprint)
    # @app.route('/')
    # def home():
        # some_track = create_some_track()
        # Use Jinja to customize a predefined html page rendering the layout for showing a single track.
        # return render_template('simple_track.html', track=some_track)
        # return render_template('layout.html')
    
        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

    return app
