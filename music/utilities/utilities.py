# from this import d
from flask import Blueprint, request, render_template, redirect, url_for, session

import music.adapters.repository as repo
import music.utilities.services as services
GLOBAL_INDEX = 1
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_random_track():
    random_track = services.get_random_track(repo.repo_instance)
    return random_track

def get_selected_tracks(quantity=20):
    tracks = services.get_random_tracks(quantity, repo.repo_instance)
    return tracks

def get_ordered_tracks(startIndex, quantity=20):

    tracks = services.get_ordered_tracks(startIndex * 20, quantity, repo.repo_instance)
    return tracks 
