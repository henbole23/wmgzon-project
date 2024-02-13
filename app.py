from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from datetime import datetime
from forms import *
import sqlite3
import secrets



# Create Flask Instance
app = Flask(__name__)
# Add Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wmgzon.db"

app.config["SECRET_KEY"] = secrets.token_urlsafe(16)

bcrypt = Bcrypt(app)
# Initialise the Database
db = SQLAlchemy(app)

# Flask_Login Config
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create User Model
class Users(db.Model, UserMixin):
    __tablename__ = "USERS"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(25), default="Customer")
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def get_id(self):
           return (self.user_id)

class Artists(db.Model):
    __tablename__ = "ARTISTS"
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(500))

class Albums(db.Model):
   __tablename__ = "ALBUMS"
   album_id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   artwork = db.Column(db.String(100), nullable=False)
   genre = db.Column(db.String(25))
   year = db.Column(db.Integer, nullable=False)
   fk_artist_id = db.Column(db.Integer, db.ForeignKey("ARTISTS.artist_id"), nullable=False)

class Songs(db.Model):
   __tablename__ = "SONGS"
   song_id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   length = db.Column(db.Integer, nullable=False)
   fk_album_id = db.Column(db.Integer, db.ForeignKey("ALBUMS.album_id"), nullable=False)
   fk_artist_id = db.Column(db.Integer, db.ForeignKey("ARTISTS.artist_id"), nullable=False)

    

def get_all_products():
    db = sqlite3.connect("wmgzon.db")
    cursor = db.cursor()

    fetch_albums = """SELECT ARTISTS.artist_id, ARTISTS.artist_name, ALBUMS.album_name, albums.artwork FROM ARTISTS
                      INNER JOIN ALBUMS ON ARTISTS.artist_id=ALBUMS.fk_artist_id"""

    cursor.execute(fetch_albums)
    products = cursor.fetchall()
    
    db.close()

    return products

def get_user_details(user, password):
    with sqlite3.connect("wmgzon.db") as db:
        cursor = db.cursor()
        fetch_user = """SELECT * FROM USERS WHERE user_name = ? AND password = ?"""

        cursor.execute(fetch_user, [user, password])
        user = cursor.fetchone()

    return user

@app.route('/')
def index():
    return render_template('index.html', products=get_all_products())

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if request.method == 'POST' and register_form.validate_on_submit():
        user = Users.query.filter_by(email=request.form['email']).first()
        if user is None:
            username = request.form['username']
            user = Users(username=username,
                         password=bcrypt.generate_password_hash(request.form['password']),
                         email=request.form['email']) # type: ignore
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('index'))
    
    
    return render_template('register.html', form=register_form)
    # else:
    #     flash("Field Required")
    #     print("Empty Fields")
    #     return render_template('register.html', form=register_form)


@app.route('/login', methods=['GET', 'POST']) 
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit():
        print(f"Form Valid: {login_form.validate_on_submit()}")
        user = Users.query.filter_by(username=request.form['username']).first()
        if user:
            print("User Valid")
            if bcrypt.check_password_hash(user.password, request.form['password']):
                print("Password Valid")
                login_user(user)
                flash("Login Successful")
                if user.type == "Admin":
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('index'))
            else:
                print("Password Invalid")
                flash("Incorrect Password")
        else:
            print("User Invalid")
            flash("User Doesn't Exist")
    return render_template('login.html', form=login_form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully")
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET'])
def admin():
    users = Users.query.all()
    albums = Albums.query.all()
    return render_template('admin.html', users=users, albums=albums)

@app.route('/music/<int:album_id>') # type: ignore
def get_product_page(album_id: int):
    db = sqlite3.connect("wmgzon.db")
    cursor = db.cursor()

    album_fetch = """SELECT ARTISTS.artist_id, ARTISTS.artist_name, ALBUMS.album_name, albums.artwork, ARTISTS.bio
                     FROM ARTISTS
                     INNER JOIN ALBUMS ON ARTISTS.artist_id=ALBUMS.fk_artist_id
                     WHERE album_id = ?"""

    cursor.execute(album_fetch, (album_id,))
    album = cursor.fetchone()
    db.close()

    if album:
        return render_template('productPage.html', product=album)
    else:
        return 'Product not found', 404

@app.route('/basket')
def basket():
    return render_template('index.html')

@app.route('/carparts')
def car_parts():
    return render_template('comingSoon.html', page_name="Car Parts")

@app.route('/animals')
def animals():
    return render_template('comingSoon.html', page_name="Animals")

@app.route('/sports')
def sports():
    return render_template('comingSoon.html', page_name="Sports")

@app.route('/books')
def books():
    return render_template('comingSoon.html', page_name="Books")

@app.route('/phones')
def phones():
    return render_template('comingSoon.html', page_name="Phones")

@app.route('/music')
def music():
    return render_template('comingSoon.html', page_name="Music")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
