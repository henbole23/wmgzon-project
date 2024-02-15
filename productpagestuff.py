artist_album = db.Table('ARTISTALBUM',
                          db.Column('artist_name', db.String, db.ForeignKey('ARTISTS.name')),
                          db.Column('album_name', db.String, db.ForeignKey('ALBUMS.name'))
                          )

artist_song = db.Table('ARTISTSONG',
                          db.Column('artist_name', db.String, db.ForeignKey('ARTISTS.name')),
                          db.Column('song_name', db.String, db.ForeignKey('SONGS.name'))
                          )

album_song = db.Table('ALBUMSONG',
                          db.Column('album_name', db.String, db.ForeignKey('ALBUMS.name')),
                          db.Column('song_name', db.String, db.ForeignKey('SONGS.name'))
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
   genre = db.Column(db.Integer, db.ForeignKey("GENRES.genre_id"), nullable=False)
   year = db.Column(db.Integer, nullable=False)
   album_artists = db.relationship('Artists', secondary=artist_album, back_populates='artist_albums')
   album_songs = db.relationship('Songs', secondary=album_song, back_populates='song_albums')
   album_product = db.relationship('Products', )

class Genres(db.Model):
    __tablename__ = "GENRES"
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), nullable=False)

class Songs(db.Model):
   __tablename__ = "SONGS"
   song_id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   length = db.Column(db.Integer, nullable=False)
   song_artists = db.relationship('Artists', secondary=artist_song, back_populates='artist_songs')
   song_albums = db.relationship('Albums', secondary=album_song, back_populates='album_songs')

product_type = db.Table('PRODUCTTYPE',
                          db.Column('product_type', db.String, db.ForeignKey('ALBUMS.name')),
                          db.Column('song_name', db.String, db.ForeignKey('SONGS.name'))
                          )









class Format(db.Model):
    __tablename__ = "FORMATS"
    format_id = db.Column(db.Integer, primary_key=True)
    format = db.Column(db.String(50), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product_id'), nullable=False)

class Order(db.Model):
    __tablename__ = "ORDERS"
    order_id = db.Column(db.Integer, primary_key=True)
    fk_user_id = db.Column(db.Integer, db.ForeignKey("USERS.user_id"), nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.utcnow)

class OrderItem(db.Model):
    __tablename__ = "ORDERITEMS"
    orderitem_id = db.Column(db.Integer, primary_key=True)
    fk_order_id = db.Column(db.Integer, db.ForeignKey("ORDERS.order_id"), nullable=False)
    fk_product_id = db.Column(db.Integer, db.ForeignKey("ALBUMS.album_id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)