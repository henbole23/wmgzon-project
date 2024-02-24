from flask import Flask, flash, redirect, url_for
from flask_session import Session
from datetime import timedelta
import secrets


from app.extensions import db, bcrypt, login_manager

from app.admin.routes import admin_bp
from app.forms import SearchForm
from app.home.routes import home_bp
from app.basket.routes import basket_bp
from app.categories.routes import category_bp
from app.models import Users


def create_app(database="sqlite:///wmgzon.db"):
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(basket_bp, url_prefix='/basket')
    app.register_blueprint(category_bp, url_prefix='/category')

    app.config["SQLALCHEMY_DATABASE_URI"] = database
    app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
    app.config["SESSION_PERMANENT"] = True
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    Session(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @app.context_processor
    def base():
        search_form = SearchForm()
        return dict(form=search_form)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.query(Users).filter_by(user_id=int(user_id)).first()

    @login_manager.unauthorized_handler
    def unauthorised_user():
        flash('Please Log In First', 'warning')
        return redirect(url_for('home.login'))

    return app
