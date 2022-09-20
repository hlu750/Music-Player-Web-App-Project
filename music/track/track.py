from email.policy import default
from flask import Blueprint, render_template, request, render_template, redirect, url_for, session
from urllib import request
from flask import Blueprint, render_template, request, url_for

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

import music.adapters.repository as repo
import music.utilities.utilities as utilities
import music.track.services as services

from music.authentication.authentication import login_required
from music.authentication.services import get_user

import  music.utilities.utilities as utilities
import  music.track.services as services
from music.domainmodel.track import Track
from music.domainmodel.user import User


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

@track_blueprint.route('/track/<int:track_id>', methods=['GET', 'POST'])
def track_page(track_id):
    song_page = request.args.get('page')
    if song_page is None:
        song_page = 0
    track = utilities.get_ordered_tracks(int(song_page), 1)
    if track is not None:
        song_page = int(song_page)
        next_track_url = None
        prev_track_url = None
        next_track_url = url_for('track_blueprint.track_page', track_id, page = song_page + 1)
        prev_track_url = url_for('track_blueprint.track_page', track_id, page = song_page - 1)
        number_of_pages = utilities.get_number_of_pages()
        if song_page + 1> number_of_pages:
            next_track_url = None
            prev_track_url = url_for('track_blueprint.track_page', track_id, page = song_page - 1)
        elif song_page == 0:
            next_track_url = url_for('track_blueprint.track_page', track_id, page = song_page + 1)
            prev_track_url = None
        
        track_to_show_reviews = request.args.get('view_reviews_for')
    
        if track_to_show_reviews == None:
            # No view-reviews query parameter, so set to a non-existent track id.
            track_to_show_reviews = -1
        elif track_to_show_reviews is not None:
            # Convert track_to_show_reviews from string to int.
            track_to_show_reviews = int(track_to_show_reviews)

        view_review_url = url_for('track_blueprint.track')
        add_review_url = url_for('track_blueprint.review_on_track')

        return render_template('track/track_page.html', 
        title='Track', track = track, track_id = track_id,
        show_reviews_for_track=track_to_show_reviews,
        view_review_url=view_review_url,
        add_review_url=add_review_url,
        next_track_url = next_track_url, 
        prev_track_url = prev_track_url
        )

    else:
        print('No tracks found')
            
    

            


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

@track_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_track():
    user_name = session['user_name']
    print("initial username:",user_name)
    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with an track id, when subsequently called with a HTTP POST request, the track id remains in the
    # form.
    form = reviewForm()

    if form.validate_on_submit():
        track_id = int(form.track_id.data)
        services.add_review(track_id, form.review.data, user_name, repo.repo_instance)

        track = services.get_track(track_id, repo.repo_instance)
        print(track)
        # Cause the web browser to display the page of all tracks that have the same date as the reviewed track,
        # and display all reviews, including the new review.
        return redirect(url_for('track_blueprint.track_page', track_id=track_id,view_reviews_for=track_id))

    if request.method == 'GET':
        if request.args.get('track') == None:
            track_id = 2
        else:
            track_id = int(request.args.get('track'))
        form.track_id.data = track_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the track id of the track being reviewed from the form.
        track_id = int(form.track_id.data)

    # For a GET or an unsuccessful POST, retrieve the track to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    track = services.get_track(track_id, repo.repo_instance)
    user: User = get_user(user_name, repo.repo_instance)
    return render_template(
        'track/review_on_track.html',
        title='Edit track',
        track=track, user=user,
        form=form,
        handler_url=url_for('track_blueprint.review_on_track'),
        selected_track=utilities.get_selected_track(track_id)
    )

class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class reviewForm(FlaskForm):
    review = TextAreaField('review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    track_id = HiddenField("track id")
    submit = SubmitField('Submit')

@track_blueprint.route('/track/<int:track_id>/like', methods=['GET', 'POST'])
@login_required
def like_track(track_id):
    user_name = session['user_name']
    user: User = get_user(user_name, repo.repo_instance)
    
    track = utilities.get_selected_track(track_id)
    user.add_liked_track(track_id)

    like_track_url = url_for('track_blueprint.like_track')

    return render_template('profile/favourites.html', 
    title='Track', track = track, user = user,
    like_track_url = like_track_url
    )