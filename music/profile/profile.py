from flask import Blueprint, render_template

profile_blueprint = Blueprint('profile_bp', __name__, url_prefix='/profile')

@profile_blueprint.route('/favourites', methods=['GET'])
def favourites():
    return render_template('profile/favourites.html')

@profile_blueprint.route('/playlists', methods=['GET'])
def playlists():
    return render_template('profile/playlists.html')
