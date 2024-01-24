from flask import Flask, render_template, redirect, url_for
from forms import *
import sqlite3
import secrets

app = Flask(__name__)
token = secrets.token_urlsafe(21)
app.secret_key = token


def get_all_products():
    db = sqlite3.connect("products.db")
    cursor = db.cursor()

    fetch_albums = """SELECT ARTISTS.artist_id, ARTISTS.artist_name, ALBUMS.album_name, albums.artwork 
                     FROM ARTISTS
                     INNER JOIN ALBUMS ON ARTISTS.artist_id=ALBUMS.fk_artist_id"""

    cursor.execute(fetch_albums)
    products = cursor.fetchall()
    
    db.close()

    return products


@app.route('/')
def index():
    products = get_all_products()

    return render_template('index.html', products=products)

@app.route('/accountSignIn') # type: ignore
def account_sign_in():
    
    form = SignInForm()

    if form.validate_on_submit():
        db = sqlite3.connect("accounts.db")
        cursor = db.cursor()

        user_name = form.user_name.data
        password = form.password.data


        fetch_user = """SELECT *
                        FROM USERS
                        WHERE user_name = ?"""

        cursor.execute(fetch_user, (user_name,))

        column_names = [desc[0] for desc in cursor.description]

        user_details = cursor.fetchone()
        user_dict = dict(zip(column_names, user_details))
        print(f"USER DICT {user_dict}")

        if user_details != None and password == user_dict.password:
            print("AUTH SUCCESS")
            return redirect( url_for('index'))
        
    return render_template('accountLogin.html')

@app.route('/admin/product_database')
def database_admin():
    return render_template('databaseAdmin.html')

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

@app.route('/music/<int:album_id>') # type: ignore
def get_product_page(album_id: int):
    db = sqlite3.connect("products.db")
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


if __name__ == '__main__':
    app.run(debug=True)
