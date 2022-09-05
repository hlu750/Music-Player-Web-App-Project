from flask import Blueprint, render_template


import  music.utilities.utilities as utilities
import  music.track.services as services
from music.domainmodel.track import Track

track_blueprint = Blueprint('track_blueprint', __name__, url_prefix='/browse')

@track_blueprint.route('/browse', methods=['GET'])
def track():
    return render_template('track/track.html', tracks = utilities.get_selected_tracks())

