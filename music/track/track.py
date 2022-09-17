from email.policy import default
from flask import Blueprint, render_template, request, render_template, redirect, url_for, session
from urllib import request
from flask import Blueprint, render_template, request, url_for

# from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

import music.adapters.repository as repo
import music.utilities.utilities as utilities
import music.track.services as services

from music.authentication.authentication import login_required

import  music.utilities.utilities as utilities
import  music.track.services as services
from music.domainmodel.track import Track

track_blueprint = Blueprint('track_blueprint', __name__, url_prefix='/browse')

@track_blueprint.route('/', methods=['GET', 'POST'])
def track():
    form = SearchForm()
  
    if not form.validate_on_submit():
    
        song_page = request.args.get('page')
    # print(request.args)
        if song_page is None:
            song_page = 0
        # track_list = (utilities.get_ordered_tracks())
        tracks = utilities.get_ordered_tracks(int(song_page))
        # print(tracks)
        if tracks is not None:
            song_page = int(song_page)
            next_tracks_url = None
            prev_tracks_url = None
            next_tracks_url = url_for('track_blueprint.track', page = song_page + 1 )
            prev_tracks_url = url_for('track_blueprint.track', page = song_page - 1 )
            number_of_pages = utilities.get_number_of_pages()
            # print(number_of_pages)
            if song_page + 1> number_of_pages:
                next_tracks_url = None
                prev_tracks_url =url_for('track_blueprint.track', page = song_page - 1)
            elif song_page == 0:
                next_tracks_url = url_for('track_blueprint.track', page = song_page + 1)
                prev_tracks_url = None
        

            return render_template('track/track.html', tracks = tracks, 
            next_tracks_url = next_tracks_url, 
            prev_tracks_url = prev_tracks_url, form = form)
        else:
            print('No tracks found')
            
    else:
        return redirect(url_for('track_blueprint.filter_track', title = form.title.data, type = form.select.data))
@track_blueprint.route('/track/<title>&<type>', methods=['GET', 'POST'])
def filter_track(title, type):
    # print(title)
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('track_blueprint.filter_track', title = form.title.data, type = form.select.data))
    else:
        
        
        filtered_tracks = utilities.get_filtered_tracks(title.lower(), type.lower())
        # print(filtered_tracks)
        if filtered_tracks is not None:
                return render_template('track/track.html', tracks = filtered_tracks, 
                next_tracks_url = None, 
                prev_tracks_url = None, form = form)
        else:
            print('No tracks found')
            return redirect(url_for('track_blueprint.track'))
# <!-- <a href="{{ url_for('track_blueprint.track_page', track_id = track.track_id ) }}" style="text-decoration:none; color: #F2F2F2;"></a> -->

 # <!-- <div class="col-sm"><a href="{{ url_for('track_blueprint.track_page', track_id = track.track_id ) }}" style="text-decoration:none; color: #F2F2F2;">{{track.title}}</a></div> -->
    
class SearchForm(FlaskForm):
    choices = [ ('Select Type', 'Select Type'),  
                ('Track','Track'),
                ('Album', 'Album'),
                ('Artist', 'Artist'),
                ('Genre', 'Genre')]
    title = StringField("Title", default = "Enter a track title", validators=[DataRequired(message="Enter a non-empty title")])
    select = SelectField('Search for music:', choices=choices)
    submit = SubmitField("Submit")