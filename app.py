from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

db = sqlite3.connect("products.db")
cursor = db.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS ARTISTS (artist_id INTEGER PRIMARY KEY AUTOINCREMENT, artist_name VARCHAR(25) NOT NULL, bio TEXT)""");
cursor.execute("""INSERT INTO ARTISTS (artist_name,bio) VALUES ("AC/DC", "A")""") 

cursor.execute("""CREATE TABLE IF NOT EXISTS ALBUMS (album_id INTEGER PRIMARY KEY, album_name VARCHAR(25) NOT NULL, artwork TEXT NOT NULL, genre VARCHAR(25) NOT NULL, artist_id INTEGER, FOREIGN KEY(artist_id) REFERENCES artists(artist_id))""");
cursor.execute("""INSERT INTO ALBUMS (album_name,artwork,genre,artist_id) VALUES ("Back in Black", "backinblack_acdc.jpg", "Hard Rock", "1")""")

db.close()

@app.route('/')
def index():
    db = sqlite3.connect("products.db")
    cursor = db.cursor()

    cursor.execute('SELECT * FROM ALBUMS')
    products = cursor.fetchall()
    
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
