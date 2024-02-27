from flask_login import UserMixin
from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Float
from app.extensions import db


class Users(db.Model, UserMixin):
    """Initialises the Users table where the app's user accounts are stored"""
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(25), default="Customer", nullable=False)
    date_added = db.Column(
        db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    orders = db.relationship('Orders', back_populates='users')

    def __init__(self, username, password, email, type="Customer"):
        self.username = username
        self.password = password
        self.email = email
        self.type = type

    def get_id(self):
        return str(self.user_id)


class Products(db.Model):
    """Initialises the Products table where the all products are stored regardless of category"""
    __tablename__ = "products"
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String, nullable=False)
    price = db.Column(Float, nullable=False)
    type = db.Column(db.String, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    date_added = db.Column(
        db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    music_info = db.relationship(
        'Albums', back_populates='products', uselist=False, cascade='all, delete-orphan')
    order_items = db.relationship(
        'OrderItems', back_populates='products', cascade='all, delete-orphan')

    def __init__(self, name, image, price, type, stock):
        self.name = name
        self.image = image
        self.price = price
        self.type = type
        self.stock = stock


class AlbumGenre(db.Model):
    """Initialises the AlbumGenre bridging table which connects the album genre many-to-many relationship"""
    __tablename__ = "album_genre"
    fk_album_id = db.Column(db.Integer, db.ForeignKey(
        "albums.album_id"), nullable=False, primary_key=True)
    fk_genre_id = db.Column(db.Integer, db.ForeignKey(
        "genres.genre_id"), nullable=False, primary_key=True)

    def __init__(self, fk_album_id, fk_genre_id):
        self.fk_album_id = fk_album_id
        self.fk_genre_id = fk_genre_id


class Albums(db.Model):
    """Initialises the Albums table which belongs to the music category"""
    __tablename__ = "albums"
    album_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    fk_product_id = db.Column(db.Integer, db.ForeignKey(
        "products.product_id"), nullable=False)
    fk_artist_id = db.Column(db.Integer, db.ForeignKey(
        "artists.artist_id"), nullable=False)
    songs = db.relationship(
        'Songs', back_populates='albums', cascade='all, delete-orphan')
    genres = db.relationship(
        'AlbumGenre', backref='album_genre', cascade='all, delete-orphan')
    artists = db.relationship(
        'Artists', uselist=False, back_populates='albums')
    products = db.relationship('Products', back_populates='music_info')

    def __init__(self, name, year, fk_product_id, fk_artist_id):
        self.name = name
        self.year = year
        self.fk_product_id = fk_product_id
        self.fk_artist_id = fk_artist_id


class Genres(db.Model):
    """Initialises the Genres table which belongs to the music category"""
    __tablename__ = "genres"
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    albums = db.relationship('AlbumGenre', backref='genre_album')

    def __init__(self, name):
        self.name = name


class Artists(db.Model):
    """Initialises the Artists table which belongs to the music category"""
    __tablename__ = "artists"
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(500), nullable=False)
    albums = db.relationship(
        'Albums', back_populates='artists', cascade='all, delete-orphan')

    def __init__(self, name, bio):
        self.name = name
        self.bio = bio


class Songs(db.Model):
    """Initialises the Songs table which belongs to the music category"""
    __tablename__ = "songs"
    song_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    fk_album_id = db.Column(db.Integer, ForeignKey(
        "albums.album_id"), nullable=False)
    albums = db.relationship('Albums', back_populates='songs')

    def __init__(self, name, length, fk_album_id):
        self.name = name
        self.length = length
        self.fk_album_id = fk_album_id


class Orders(db.Model):
    """Initialises the Orders table where user orders are stored"""
    __tablename__ = "orders"
    order_id = db.Column(db.Integer, primary_key=True)
    date_added = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    fk_user_id = db.Column(db.Integer, ForeignKey('users.user_id'))

    users = db.relationship('Users', back_populates='orders')
    items = db.relationship(
        'OrderItems', back_populates='orders', cascade='all, delete-orphan')

    def __init__(self, fk_user_id):
        self.fk_user_id = fk_user_id


class OrderItems(db.Model):
    """Initialises the OrderItems table which is where items belonging to the Orders are stored"""
    __tablename__ = "orderitems"
    item_id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    format = db.Column(db.Integer, nullable=False)
    fk_order_id = db.Column(db.Integer, ForeignKey('orders.order_id'))
    fk_product_id = db.Column(db.Integer, ForeignKey('products.product_id'))

    orders = db.relationship('Orders', back_populates='items')
    products = db.relationship('Products', back_populates='order_items')

    def __init__(self, quantity, format, fk_order_id, fk_product_id):
        self.quantity = quantity
        self.format = format
        self.fk_order_id = fk_order_id
        self.fk_product_id = fk_product_id
