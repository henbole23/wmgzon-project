from flask import Blueprint, render_template

from models import Products
from extensions import db

home_bp = Blueprint('home', __name__, template_folder='templates')


@home_bp.route('/')
def index():
    recently_added = db.session.query(Products).order_by(Products.date_added.desc()).limit(5).all()
    products = db.session.query(Products).all()
    return render_template('index.html', products=products, recently_added=recently_added)