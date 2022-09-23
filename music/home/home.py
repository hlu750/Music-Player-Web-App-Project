from flask import Blueprint, render_template
import music.utilities.utilities as utilities
from music.domainmodel.track import Track
home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template('home/home.html',track = utilities.get_random_track())

