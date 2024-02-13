from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
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
    
artist_album = db.Table('ARTISTALBUM',
                          db.Column('artist_id', db.Integer, db.ForeignKey('ARTISTS.artist_id')),
                          db.Column('album_id', db.Integer, db.ForeignKey('ALBUMS.album_id'))
                          )

artist_song = db.Table('ARTISTSONG',
                          db.Column('artist_id', db.Integer, db.ForeignKey('ARTISTS.artist_id')),
                          db.Column('song_id', db.Integer, db.ForeignKey('SONGS.song_id'))
                          )

album_song = db.Table('ALBUMSONG',
                          db.Column('album_id', db.Integer, db.ForeignKey('ALBUMS.album_id'), primary_key=True),
                          db.Column('song_id', db.Integer, db.ForeignKey('SONGS.song_id'), primary_key=True)
                          )

class Artists(db.Model):
    __tablename__ = "ARTISTS"
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(500))
    artist_albums = db.relationship('Albums', secondary=artist_album, back_populates='album_artists')
    artist_songs = db.relationship('Songs', secondary=artist_song, back_populates='song_artists')

class Albums(db.Model):
   __tablename__ = "ALBUMS"
   album_id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   artwork = db.Column(db.String(100), nullable=False)
   genre = db.Column(db.String(25))
   year = db.Column(db.Integer, nullable=False)
   album_artists = db.relationship('Artists', secondary=artist_album, back_populates='artist_albums')
   album_songs = db.relationship('Songs', secondary=album_song, back_populates='song_albums')

class Songs(db.Model):
   __tablename__ = "SONGS"
   song_id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   length = db.Column(db.Integer, nullable=False)
   song_artists = db.relationship('Artists', secondary=artist_song, back_populates='artist_songs')
   song_albums = db.relationship('Albums', secondary=album_song, back_populates='album_songs')
#    fk_album_id = db.Column(db.Integer, db.ForeignKey("ALBUMS.album_id"), nullable=False)

class Format(db.Model):
    __tablename__ = "FORMATS"
    format_id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)

class Order(db.Model):
    __tablename__ = "ORDERS"
    order_id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey("USERS.user_id"), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

class OrderItem(db.Model):
    __tablename__ = "ORDERITEMS"
    orderitem_id = db.Column(db.Integer, primary_key=True)
    fk_order_id = db.Column(db.Integer, db.ForeignKey("ORDERS.order_id"), nullable=False)
    fk_album_id = db.Column(db.Integer, db.ForeignKey("ALBUMS.album_id"), nullable=False)
    fk_format_id = db.Column(db.Integer, db.ForeignKey("FORMATS.format_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

# def get_all_products():
#     db = sqlite3.connect("wmgzon.db")
#     cursor = db.cursor()

#     fetch_albums = """SELECT ARTISTS.artist_id, ARTISTS.artist_name, ALBUMS.album_name, albums.artwork FROM ARTISTS
#                       INNER JOIN ALBUMS ON ARTISTS.artist_id=ALBUMS.fk_artist_id"""

#     cursor.execute(fetch_albums)
#     products = cursor.fetchall()
    
#     db.close()

#     return products

def get_user_details(user, password):
    with sqlite3.connect("wmgzon.db") as db:
        cursor = db.cursor()
        fetch_user = """SELECT * FROM USERS WHERE user_name = ? AND password = ?"""

        cursor.execute(fetch_user, [user, password])
        user = cursor.fetchone()

    return user

@app.route('/')
def index():
    # albums = db.session.query(db.select(Albums)).all()
    albums = Albums.query.all()
    print(albums)
    return render_template('index.html', products=albums)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = Users.query.filter_by(email=request.form['email']).first()
        if user is None:
            username = request.form['username']
            user = Users(username=username,
                         password=bcrypt.generate_password_hash(request.form['password']),
                         email=request.form['email']) # type: ignore
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('index'))
    
    print(f"FORM VALID: {register_form.validate_on_submit()}")
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
