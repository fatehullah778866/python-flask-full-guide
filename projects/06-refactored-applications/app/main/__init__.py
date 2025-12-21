# Main Blueprint
# This blueprint handles the main pages (home, about)

from flask import Blueprint

# Create blueprint
# 'main' is the name, __name__ is the module
bp = Blueprint('main', __name__)

# Import routes (must be after blueprint creation)
from app.main import routes

