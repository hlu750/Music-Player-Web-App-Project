from flask import Blueprint, render_template, url_for
import music.track.track as track_bp
import music.utilities.utilities as utilities
from music.domainmodel.track import Track
home_blueprint = Blueprint('home_bp', __name__)
# def create_some_track():
#     some_track = Track(1, "Heat Waves")
#     some_track.track_duration = 250
#     some_track.track_url = 'https://spotify/track/1'
#     return some_track
@home_blueprint.route('/', methods=['GET'])
def home():
    track = utilities.get_random_track()
    song_url = url_for("track_blueprint.track_page", track_id = track.track_id)

    return render_template('home/home.html',track = track, song_url = song_url, refresh = url_for("home_bp.home"))

