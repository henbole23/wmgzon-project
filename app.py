from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/accountSignIn')
def account_sign_in():
    return render_template('index.html')

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


if __name__ == '__main__':
    app.run(debug=True)
