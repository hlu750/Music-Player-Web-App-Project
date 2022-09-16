# from typing import List, Iterable

# from music.adapters.repository import AbstractRepository
# from music.domainmodel.review import Review
# from music.domainmodel.track import Track
# from music.domainmodel.genre import Genre

# class NonExistenttrackException(Exception):
#     pass


# class UnknownUserException(Exception):
#     pass


# def add_review(track_id: int, review_text: str, user_name: str, repo: AbstractRepository):
#     # Check that the track exists.
#     track = repo.get_track(track_id)
#     if track is None:
#         raise NonExistenttrackException

#     user = repo.get_user(user_name)
#     if user is None:
#         raise UnknownUserException

#     # Create review.
#     review = Review(track, review_text, user_name)

#     # Update the repository.
#     repo.add_review(review)


# def get_track(track_id: int, repo: AbstractRepository):
#     track = repo.get_track(track_id)

#     if track is None:
#         raise NonExistenttrackException

#     return track_to_dict(track)


# def get_first_track(repo: AbstractRepository):

#     track = repo.get_first_track()

#     return track_to_dict(track)


# def get_last_track(repo: AbstractRepository):

#     track = repo.get_last_track()
#     return track_to_dict(track)


# def get_tracks_by_date(date, repo: AbstractRepository):
#     # Returns tracks for the target date (empty if no matches), the date of the previous track (might be null), the date of the next track (might be null)

#     tracks = repo.get_tracks_by_date(target_date=date)

#     tracks_dto = list()
#     prev_date = next_date = None

#     if len(tracks) > 0:
#         prev_date = repo.get_date_of_previous_track(tracks[0])
#         next_date = repo.get_date_of_next_track(tracks[0])

#         # Convert tracks to dictionary form.
#         tracks_dto = tracks_to_dict(tracks)

#     return tracks_dto, prev_date, next_date


# def get_track_ids_for_tag(tag_name, repo: AbstractRepository):
#     track_ids = repo.get_track_ids_for_tag(tag_name)

#     return track_ids


# def get_tracks_by_id(id_list, repo: AbstractRepository):
#     tracks = repo.get_tracks_by_id(id_list)

#     # Convert tracks to dictionary form.
#     tracks_as_dict = tracks_to_dict(tracks)

#     return tracks_as_dict


# def get_reviews_for_track(track_id, repo: AbstractRepository):
#     track = repo.get_track(track_id)

#     if track is None:
#         raise NonExistenttrackException

#     return reviews_to_dict(track.reviews)


# # ============================================
# # Functions to convert model entities to dicts
# # ============================================

# def track_to_dict(track: track):
#     track_dict = {
#         'id': track.id,
#         'date': track.date,
#         'title': track.title,
#         'first_paragraph': track.first_paragraph,
#         'hyperlink': track.hyperlink,
#         'image_hyperlink': track.image_hyperlink,
#         'reviews': reviews_to_dict(track.reviews),
#         'tags': tags_to_dict(track.tags)
#     }
#     return track_dict


# def tracks_to_dict(tracks: Iterable[track]):
#     return [track_to_dict(track) for track in tracks]


# def review_to_dict(review: review):
#     review_dict = {
#         'user_name': review.user.user_name,
#         'track_id': review.track.id,
#         'review_text': review.review,
#         'timestamp': review.timestamp
#     }
#     return review_dict


# def reviews_to_dict(reviews: Iterable[review]):
#     return [review_to_dict(review) for review in reviews]


# def tag_to_dict(tag: Tag):
#     tag_dict = {
#         'name': tag.tag_name,
#         'tagged_tracks': [track.id for track in tag.tagged_tracks]
#     }
#     return tag_dict


# def tags_to_dict(tags: Iterable[Tag]):
#     return [tag_to_dict(tag) for tag in tags]


# # ============================================
# # Functions to convert dicts to model entities
# # ============================================

# def dict_to_track(dict):
#     track = track(dict.id, dict.date, dict.title, dict.first_para, dict.hyperlink)
#     # Note there's no reviews or tags.
#     return track
