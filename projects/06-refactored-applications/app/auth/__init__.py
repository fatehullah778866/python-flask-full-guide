# Auth Blueprint
# This blueprint handles authentication routes (login, register)

from flask import Blueprint

# Create blueprint
bp = Blueprint('auth', __name__)

# Import routes (must be after blueprint creation)
from app.auth import routes

