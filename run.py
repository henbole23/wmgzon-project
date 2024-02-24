from app import create_app
from app.extensions import db

# Initialisation of the app
app = create_app()


if __name__ == '__main__':
    # Creates the database if it doesn't already exist
    with app.app_context():
        db.create_all()

    # Runs the app
    app.run(debug=True)
