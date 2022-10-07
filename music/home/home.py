from flask import Blueprint, render_template, url_for
import music.track.track as track_bp
import music.utilities.utilities as utilities
from music.domainmodel.model import Track
home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    track = utilities.get_random_track()
    song_url = url_for("track_blueprint.track_page", track_id = track.track_id)

    return render_template('home/home.html',track = track, song_url = song_url, refresh = url_for("home_bp.home"))

