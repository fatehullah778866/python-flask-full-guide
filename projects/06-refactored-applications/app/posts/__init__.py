# Posts Blueprint
# This blueprint handles all blog post related routes

from flask import Blueprint

# Create blueprint
bp = Blueprint('posts', __name__)

# Import routes (must be after blueprint creation)
from app.posts import routes

