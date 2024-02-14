from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wmgzon23.db"

db = SQLAlchemy(app)

class Example(db.model):
    user_id = db.Column(db.Integer, primary_key=True)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
