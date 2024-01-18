from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

db = sqlite3.connect("products.db")
cursor = db.cursor()


@app.route('/')
def index():
    db = sqlite3.connect("products.db")
    cursor = db.cursor()

    album_fetch = """SELECT ARTISTS.artist_id, ARTISTS.artist_name, ALBUMS.album_name, albums.artwork 
                     FROM ARTISTS
                     INNER JOIN ALBUMS ON ARTISTS.artist_id=ALBUMS.artist_id"""

    cursor.execute(album_fetch)
    products = cursor.fetchall()
    for product in products:
        print(product)
    db.close()

    return render_template('index.html', products=products)

@app.route('/accountSignIn')
def account_sign_in():
    return render_template('login.html')

@app.route('/admin/product_database')
def database_admin():
    return render_template('databaseAdmin.html')

@app.route('/basket')
def basket():
    return render_template('index.html')



@app.route('/carparts')
def car_parts():
    return "CARPARTS"

@app.route('/animals')
def animals():
    return "ANIMALS"

@app.route('/sports')
def sports():
    return "SPORTS"

@app.route('/books')
def books():
    return "BOOKS"

@app.route('/phones')
def phones():
    return "PHONES"

@app.route('/music')
def music():
    return render_template('index.html')

@app.route('/music/example')
def get_product_page():
    return render_template('productPage.html')


if __name__ == '__main__':
    app.run(debug=True)
