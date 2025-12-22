# Main Blueprint
# Handles main pages (home, about, profiles)

from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes

