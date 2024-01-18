import sqlite3

connection = sqlite3.connect("products.db")


cursor = connection.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS ARTISTS (artist_id INTEGER PRIMARY KEY AUTOINCREMENT, artist_name VARCHAR(25) NOT NULL, bio TEXT)""");
cursor.execute("""INSERT INTO ARTISTS (artist_name,bio) VALUES ("AC/DC", "A")""") 

cursor.execute("""CREATE TABLE IF NOT EXISTS ALBUMS (album_id INTEGER PRIMARY KEY, album_name VARCHAR(25) NOT NULL, artwork TEXT NOT NULL, genre VARCHAR(25) NOT NULL, artist_id INTEGER, FOREIGN KEY(artist_id) REFERENCES artists(artist_id))""");
cursor.execute("""INSERT INTO ALBUMS (album_name,artwork,genre,artist_id) VALUES ("Back in Black", "backinblack_acdc.jpg", "Hard Rock", "1")""")

sql_query = """SELECT name FROM sqlite_master 
    WHERE type='table';"""

q2 = """SELECT * FROM ALBUMS WHERE artist_id=1"""

cursor.execute(sql_query)
print(cursor.fetchall())

connection.close()