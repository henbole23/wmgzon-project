db = SQLAlchemy()
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
    login_manager.init_app(app)

    return app