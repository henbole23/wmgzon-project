from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bcrypt import Bcrypt
from forms import *
import sqlite3
import secrets

app = Flask(__name__)
token = secrets.token_urlsafe(21)
bcrypt = Bcrypt(app)
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

@app.route('/register', methods=['POST', 'GET'])
def register():
    register_form = RegisterForm()
    if request.method == 'POST':
        with sqlite3.connect("accounts.db") as db:
            cursor = db.cursor()

            add_user = """INSERT INTO USERS (user_name,password,type)
                          VALUES(?,?,?)"""

            new_user = request.form['username']

            hashed_password = bcrypt.generate_password_hash(request.form['password'])

            cursor.execute(add_user, (new_user, hashed_password, 'customer'))
            db.commit()

        return redirect(url_for('index'))
    elif request.method == 'GET':
        return render_template('register.html', form=register_form)
    else:
        flash("Field Required")
        print("Empty Fields")
        return render_template('register.html', form=register_form)


@app.route('/login', methods=['POST', 'GET']) 
def login():
    # Set the form inputs
    login_form = LoginForm()

    if request.method == 'POST':
        # If form inputs aren't valid
        # if not login_form.validate_on_submit():
        #     flash("Field Required")
        #     print("Empty Fields")
        #     return render_template('login.html', form=login_form)
        # else:
        print("VALID")
        # Connect to account database
        db = sqlite3.connect("accounts.db")
        cursor = db.cursor()

        username = request.form['username']
        hashed_password = bcrypt.generate_password_hash(request.form['password'])

        fetch_user = """SELECT *
                FROM USERS
                WHERE user_name = ?
                AND password = ?"""
        
        cursor.execute(fetch_user, (username, hashed_password))
        data = cursor.fetchone()
        print(data)
        if data:
            # returns error if data already exists in database
            print("AUTH SUCCESSFUL")
        else:
            return render_template("error.html")     
    elif request.method == 'GET':
        return render_template('login.html', form=login_form)
    else:
        flash("Field Required")
        print("Empty Fields")
        return render_template('login.html', form=login_form)


@app.route('/admin', methods=['GET'])
def database_admin():
    db = sqlite3.connect("accounts.db")
    cursor = db.cursor()

    fetch_all_users = """SELECT * FROM USERS"""

    cursor.execute(fetch_all_users)
    data = cursor.fetchall()
    print(data)
    
    db.close()

    return render_template('admin.html', users=data)
    

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
