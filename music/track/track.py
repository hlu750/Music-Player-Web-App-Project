from flask import Blueprint, render_template


import  music.utilities.utilities as utilities
import  music.track.services as services
from music.domainmodel.track import Track

track_blueprint = Blueprint('track_blueprint', __name__, url_prefix='/browse')

@track_blueprint.route('/browse', methods=['GET'])
def track():
    track_list = (utilities.get_selected_tracks())
    return render_template('track/track.html', tracks = track_list)

