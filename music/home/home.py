from flask import Blueprint, render_template
import music.utilities.utilities as utilities
from music.domainmodel.track import Track
home_blueprint = Blueprint('home_bp', __name__)
def create_some_track():
    some_track = Track(1, "Heat Waves")
    some_track.track_duration = 250
    some_track.track_url = 'https://spotify/track/1'
    return some_track
@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('home/home.html',track = create_some_track() )

