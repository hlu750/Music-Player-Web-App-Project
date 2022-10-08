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
from music.domainmodel.model import Track, User
# from music.domainmodel.user import User

from music.authentication.services import get_user

profile_blueprint = Blueprint('profile_bp', __name__, url_prefix='/profile')

@profile_blueprint.route('/recommended_tracks', methods=['GET', 'POST'])
@login_required
def recommended_tracks():
    user_name = session['user_name']
    liked_tracks = services.get_liked_tracks_list(user_name, repo.repo_instance)
    if liked_tracks:
        
        # print(request.args.get('track_id'))
        if request.args.get('track_id') and  int(request.args.get('track_id')) in [track.track_id for track in liked_tracks]:
            random_track = services.get_track(int(request.args.get('track_id')), repo.repo_instance)[1]
        else:
            random_track = services.get_first_liked_track(user_name, repo.repo_instance)
        recommended_tracks = services.get_recommended_tracks(user_name, repo.repo_instance, random_track)
        stripped_recommended_tracks  = [] 
        [stripped_recommended_tracks.append(track) for track in recommended_tracks if track not in stripped_recommended_tracks]
        if recommended_tracks is None:
            recommended_tracks = []
        prev_track, next_track= services.get_next_and_prev_liked_tracks(user_name, repo, random_track)
        prev_track_url = url_for('profile_bp.recommended_tracks',track_id  = prev_track.track_id) if prev_track else None 
        next_track_url = url_for('profile_bp.recommended_tracks',track_id  = next_track.track_id) if next_track else None 
        # print(prev_track_url)
        # print(next_track_url)
        # print("Random Track", random_track)
        return render_template('profile/recommended.html',selected_track = random_track,tracks = stripped_recommended_tracks, prev_tracks_url = prev_track_url, next_tracks_url = next_track_url)
    else:
        return render_template('profile/recommended.html', selected_track = None,tracks = None)

from music.track.services import get_liked_tracks

@profile_blueprint.route('/favourites', methods=['GET', 'POST'])
@login_required
def favourites():
    user_name = session['user_name']
    # print(user_name)
    user : User = get_user(user_name, repo.repo_instance)
    print("user?")
    print(user)
    # tracks = user.liked_tracks()
    # liked_tracks = request.args.get('tracks')
    print("ooo")
    # print(liked_tracks)
    print("right:")
    
    tracks = get_liked_tracks(user_name, repo.repo_instance)
    # print(services.get_liked_tracks(user_name, repo.repo_instance))
    # tracks = services.get_liked_tracks(user_name, repo.repo_instance)
    print(tracks)
    like_track_url = url_for('track_blueprint.like_track')

    return render_template('profile/favourites.html', 
    title='Track', tracks = tracks, user = user,
    like_track_url = like_track_url
    )
