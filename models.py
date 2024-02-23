from flask_login import UserMixin
from datetime import datetime
from sqlalchemy import ForeignKey

from extensions import db

# Create User Model
class Users(db.Model, UserMixin):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(25), default="Customer", nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    orders = db.relationship('Orders', back_populates='users')

    def get_id(self):
        return self.user_id

class Products(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    music_info = db.relationship('Albums', back_populates='products', cascade='all, delete-orphan')
    order_items = db.relationship('OrderItems', back_populates='products', cascade='all, delete-orphan')
    
class AlbumGenre(db.Model):
    __tablename__ = "album_genre"
    albumgenre_id = db.Column(db.Integer, primary_key=True)
    fk_album_id = db.Column(db.Integer, db.ForeignKey("albums.album_id"), nullable=False)
    fk_genre_id = db.Column(db.Integer, db.ForeignKey("genres.genre_id"), nullable=False)

class Albums(db.Model):
   __tablename__ = "albums"
   album_id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   year = db.Column(db.Integer, nullable=False)
   fk_product_id = db.Column(db.Integer, db.ForeignKey("products.product_id"), nullable=False)
   fk_artist_id = db.Column(db.Integer, db.ForeignKey("artists.artist_id"), nullable=False)

   songs = db.relationship('Songs', back_populates='albums', cascade='all, delete-orphan')
   genres = db.relationship('AlbumGenre', backref='album_genre', cascade='all, delete-orphan')
   artists = db.relationship('Artists', back_populates='albums')
   products = db.relationship('Products', back_populates='music_info')

class Genre(db.Model):
    __tablename__ = "genres"
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    albums = db.relationship('AlbumGenre', backref='genre_album')

class Artists(db.Model):
    __tablename__ = "artists"
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(500), nullable=False)

    albums = db.relationship('Albums', back_populates='artists', cascade='all, delete-orphan')

class Songs(db.Model):
    __tablename__ = "songs"
    song_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    fk_album_id = db.Column(db.Integer, ForeignKey("albums.album_id"), nullable=False)

    albums = db.relationship('Albums', back_populates='songs')

class Orders(db.Model):
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    fk_user_id = db.Column(db.Integer, ForeignKey('users.user_id'))

    users = db.relationship('Users', back_populates='orders')
    items = db.relationship('OrderItems', back_populates='orders', cascade='all, delete-orphan')

class OrderItems(db.Model):
    __tablename__ = "orderitems"
    item_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    fk_order_id = db.Column(db.Integer, ForeignKey('orders.order_id'))
    fk_product_id = db.Column(db.Integer, ForeignKey('products.product_id'))

    orders = db.relationship('Orders', back_populates='items')
    products = db.relationship('Products', back_populates='order_items')
