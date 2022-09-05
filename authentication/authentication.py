from flask import Blueprint, render_template
import music.utilities.utilities as utilities
from music.domainmodel.track import Track
authentication_blueprint = Blueprint('authentication_bp', __name__)

@authentication_blueprint.route('/', methods=['GET'])
def register():
    return render_template('home/home.html',track = utilities.get_random_track())

