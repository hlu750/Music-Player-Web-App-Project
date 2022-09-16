from flask import Blueprint, render_template, request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import music.adapters.repository as repo
import music.utilities.utilities as utilities
import music.track.services as services

from music.authentication.authentication import login_required

import  music.utilities.utilities as utilities
import  music.track.services as services
from music.domainmodel.track import Track

track_blueprint = Blueprint('track_blueprint', __name__, url_prefix='/browse')

@track_blueprint.route('/browse', methods=['GET'])
def track():
    track_list = (utilities.get_selected_tracks())
    return render_template('track/track.html', tracks = track_list)

# def track_page():
#     track = (utilities.get_selected_track())
#     return render_template('track/track_page.html', tracks = track)

# @track_blueprint.route('/tracks_by_date', methods=['GET'])
# def tracks_by_date():
#     # Read query parameters.
#     target_date = request.args.get('date')
#     track_to_show_reviews = request.args.get('view_reviews_for')

#     # Fetch the first and last tracks in the series.
#     first_track = services.get_first_track(repo.repo_instance)
#     last_track = services.get_last_track(repo.repo_instance)

#     if target_date is None:
#         # No date query parameter, so return tracks from day 1 of the series.
#         target_date = first_track['date']
#     else:
#         # Convert target_date from string to date.
#         target_date = date.fromisoformat(target_date)

#     if track_to_show_reviews is None:
#         # No view-reviews query parameter, so set to a non-existent track id.
#         track_to_show_reviews = -1
#     else:
#         # Convert track_to_show_reviews from string to int.
#         track_to_show_reviews = int(track_to_show_reviews)

#     # Fetch track(s) for the target date. This call also returns the previous and next dates for tracks immediately
#     # before and after the target date.
#     tracks, previous_date, next_date = services.get_tracks_by_date(target_date, repo.repo_instance)

#     first_track_url = None
#     last_track_url = None
#     next_track_url = None
#     prev_track_url = None

#     if len(tracks) > 0:
#         # There's at least one track for the target date.
#         if previous_date is not None:
#             # There are tracks on a previous date, so generate URLs for the 'previous' and 'first' navigation buttons.
#             prev_track_url = url_for('track_blueprint.tracks_by_date', date=previous_date.isoformat())
#             first_track_url = url_for('track_blueprint.tracks_by_date', date=first_track['date'].isoformat())

#         # There are tracks on a subsequent date, so generate URLs for the 'next' and 'last' navigation buttons.
#         if next_date is not None:
#             next_track_url = url_for('track_blueprint.tracks_by_date', date=next_date.isoformat())
#             last_track_url = url_for('track_blueprint.tracks_by_date', date=last_track['date'].isoformat())

#         # Construct urls for viewing track reviews and adding reviews.
#         for track in tracks:
#             track['view_review_url'] = url_for('track_blueprint.tracks_by_date', date=target_date, view_reviews_for=track['id'])
#             track['add_review_url'] = url_for('track_blueprint.review_on_track', track=track['id'])

#         # Generate the weblueprintage to display the tracks.
#         return render_template(
#             'track/tracks.html',
#             title='tracks',
#             tracks_title=target_date.strftime('%A %B %e %Y'),
#             tracks=tracks,
#             selected_tracks=utilities.get_selected_tracks(len(tracks) * 2),
#             genre_urls=utilities.get_genres_and_urls(),
#             first_track_url=first_track_url,
#             last_track_url=last_track_url,
#             prev_track_url=prev_track_url,
#             next_track_url=next_track_url,
#             show_reviews_for_track=track_to_show_reviews
#         )

#     # No tracks to show, so return the homepage.
#     return redirect(url_for('home_blueprint.home'))


# @track_blueprint.route('/tracks_by_genre', methods=['GET'])
# def tracks_by_genre():
#     tracks_per_page = 30

#     # Read query parameters.
#     genre_name = request.args.get('genre')
#     cursor = request.args.get('cursor')
#     track_to_show_reviews = request.args.get('view_reviews_for')

#     if track_to_show_reviews is None:
#         # No view-reviews query parameter, so set to a non-existent track id.
#         track_to_show_reviews = -1
#     else:
#         # Convert track_to_show_reviews from string to int.
#         track_to_show_reviews = int(track_to_show_reviews)

#     if cursor is None:
#         # No cursor query parameter, so initialise cursor to start at the beginning.
#         cursor = 0
#     else:
#         # Convert cursor from string to int.
#         cursor = int(cursor)

#     # Retrieve track ids for tracks that are genreged with genre_name.
#     track_ids = services.get_track_ids_for_genre(genre_name, repo.repo_instance)

#     # Retrieve the batch of tracks to display on the Web page.
#     tracks = services.get_tracks_by_id(track_ids[cursor:cursor + tracks_per_page], repo.repo_instance)

#     first_track_url = None
#     last_track_url = None
#     next_track_url = None
#     prev_track_url = None

#     if cursor > 0:
#         # There are preceding tracks, so generate URLs for the 'previous' and 'first' navigation buttons.
#         prev_track_url = url_for('track_blueprint.tracks_by_genre', genre=genre_name, cursor=cursor - tracks_per_page)
#         first_track_url = url_for('track_blueprint.tracks_by_genre', genre=genre_name)

#     if cursor + tracks_per_page < len(track_ids):
#         # There are further tracks, so generate URLs for the 'next' and 'last' navigation buttons.
#         next_track_url = url_for('track_blueprint.tracks_by_genre', genre=genre_name, cursor=cursor + tracks_per_page)

#         last_cursor = tracks_per_page * int(len(track_ids) / tracks_per_page)
#         if len(track_ids) % tracks_per_page == 0:
#             last_cursor -= tracks_per_page
#         last_track_url = url_for('track_blueprint.tracks_by_genre', genre=genre_name, cursor=last_cursor)

#     # Construct urls for viewing track reviews and adding reviews.
#     for track in tracks:
#         track['view_review_url'] = url_for('track_blueprint.tracks_by_genre', genre=genre_name, cursor=cursor, view_reviews_for=track['id'])
#         track['add_review_url'] = url_for('track_blueprint.review_on_track', track=track['id'])

#     # Generate the weblueprintage to display the tracks.
#     return render_template(
#         'track/tracks.html',
#         title='tracks',
#         tracks_title='tracks genreged by ' + genre_name,
#         tracks=tracks,
#         selected_tracks=utilities.get_selected_tracks(len(tracks) * 2),
#         genre_urls=utilities.get_genres_and_urls(),
#         first_track_url=first_track_url,
#         last_track_url=last_track_url,
#         prev_track_url=prev_track_url,
#         next_track_url=next_track_url,
#         show_reviews_for_track=track_to_show_reviews
#     )


# @track_blueprint.route('/review', methods=['GET', 'POST'])
# @login_required
# def review_on_track():
#     # Obtain the user name of the currently logged in user.
#     user_name = session['user_name']

#     # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
#     # the form with an track id, when subsequently called with a HTTP POST request, the track id remains in the
#     # form.
#     form = reviewForm()

#     if form.validate_on_submit():
#         # Successful POST, i.e. the review text has passed data validation.
#         # Extract the track id, representing the reviewed track, from the form.
#         track_id = int(form.track_id.data)

#         # Use the service layer to store the new review.
#         services.add_review(track_id, form.review.data, user_name, repo.repo_instance)

#         # Retrieve the track in dict form.
#         track = services.get_track(track_id, repo.repo_instance)

#         # Cause the web browser to display the page of all tracks that have the same date as the reviewed track,
#         # and display all reviews, including the new review.
#         return redirect(url_for('track_blueprint.tracks_by_date', date=track['date'], view_reviews_for=track_id))

#     if request.method == 'GET':
#         # Request is a HTTP GET to display the form.
#         # Extract the track id, representing the track to review, from a query parameter of the GET request.
#         track_id = int(request.args.get('track'))

#         # Store the track id in the form.
#         form.track_id.data = track_id
#     else:
#         # Request is a HTTP POST where form validation has failed.
#         # Extract the track id of the track being reviewed from the form.
#         track_id = int(form.track_id.data)

#     # For a GET or an unsuccessful POST, retrieve the track to review in dict form, and return a Web page that allows
#     # the user to enter a review. The generated Web page includes a form object.
#     track = services.get_track(track_id, repo.repo_instance)
#     return render_template(
#         'track/review_on_track.html',
#         title='Edit track',
#         track=track,
#         form=form,
#         handler_url=url_for('track_blueprint.review_on_track'),
#         selected_tracks=utilities.get_selected_tracks(),
#         genre_urls=utilities.get_genres_and_urls()
#     )


# class ProfanityFree:
#     def __init__(self, message=None):
#         if not message:
#             message = u'Field must not contain profanity'
#         self.message = message

#     def __call__(self, form, field):
#         if profanity.contains_profanity(field.data):
#             raise ValidationError(self.message)


# class reviewForm(FlaskForm):
#     review = TextAreaField('review', [
#         DataRequired(),
#         Length(min=4, message='Your review is too short'),
#         ProfanityFree(message='Your review must not contain profanity')])
#     track_id = HiddenField("track id")
#     submit = SubmitField('Submit')
