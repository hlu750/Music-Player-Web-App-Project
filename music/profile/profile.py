from flask import Blueprint, render_template
from music.authentication import authentication, services
from flask import Blueprint, render_template, request, render_template, redirect, url_for, session

import music.adapters.repository as repo
from music.adapters.memory_repository import MemoryRepository
import music.utilities.utilities as utilities
import music.track.services as services

from music.authentication.authentication import login_required
# from music.authentication.services import get_user

import  music.utilities.utilities as utilities
import  music.track.services as services
from music.domainmodel.track import Track
from music.domainmodel.user import User


profile_blueprint = Blueprint('profile_bp', __name__, url_prefix='/profile')

@profile_blueprint.route('/playlists', methods=['GET'])
@login_required
def playlists():
    return render_template('profile/playlists.html')

@profile_blueprint.route('/favourites', methods=['GET', 'POST'])
@login_required
def favourites():
    user_name = session['user_name']
    print(user_name)
    user : User = MemoryRepository.get_user(user_name)
    tracks = user.liked_tracks()

    like_track_url = url_for('track_blueprint.like_track')

    return render_template('profile/favourites.html', 
    title='Track', tracks = tracks, user = user,
    like_track_url = like_track_url
    )
    