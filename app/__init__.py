from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_session import Session
from datetime import timedelta
from .models import metadata
import secrets

db = SQLAlchemy(metadata=metadata)
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app():
    # Create Flask Instance
    app = Flask(__name__)
    # Add Database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wmgzon.db"
    # Sets secret key for various authentication such as forms
    app.config["SECRET_KEY"] = secrets.token_urlsafe(16)


    # Initialise Sessions
    app.config["SESSION_PERMANENT"] = True
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
    Session(app)


    # Initialise bcrypt encyption for passwords
    db.init_app(app)
    # Initialise the Database
    bcrypt.init_app(app)
    # Initialise login manager
    login_manager.init_app(app)

    from .admin import routes

    app.register_blueprint(routes.admin_bp, url_prefix='/admin')

    # Establishes the database if doesn't already exist
    with app.app_context():
        db.create_all()

    return app
