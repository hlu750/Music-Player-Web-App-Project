# from this import d
from flask import Blueprint, request, render_template, redirect, url_for, session

import music.adapters.repository as repo
import music.utilities.services as services

utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_random_track():
    random_track = services.get_random_track(repo.repo_instance)
    return random_track