from urllib import request
from flask import Blueprint, render_template, request, url_for


import  music.utilities.utilities as utilities
import  music.track.services as services
from music.domainmodel.track import Track

track_blueprint = Blueprint('track_blueprint', __name__, url_prefix='/browse')

@track_blueprint.route('/page', methods=['GET'])
def track():
    song_page = request.args.get('page')
    print(song_page)
    if song_page is None:
        song_page = 0
    # track_list = (utilities.get_ordered_tracks())
    tracks = utilities.get_ordered_tracks(int(song_page))
    next_tracks_url = None
    prev_tracks_url = None
    next_tracks_url = url_for('track_blueprint.track', page = int(song_page) + 1 )
    # print(next_tracks_url)
    
    if int(song_page) >0 :
         prev_tracks_url = url_for('track_blueprint.track', page = int(song_page) - 1 )
    return render_template('track/track.html', tracks = tracks, 
    next_tracks_url = next_tracks_url, 
    prev_tracks_url = prev_tracks_url)

