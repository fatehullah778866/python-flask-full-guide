# Application Entry Point
# This is the file you run to start the application

from app import create_app, db
from app.config import DevelopmentConfig

# Create application using factory
app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Start the Flask development server
    app.run(debug=True)

