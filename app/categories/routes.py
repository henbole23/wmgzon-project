from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import desc, func

from app.forms import FilterForm, SortForm
from app.models import AlbumGenre, Albums, Artists, Genres, OrderItems, Products
from app.extensions import db

category_bp = Blueprint('categories', __name__, template_folder='templates')


@category_bp.route('/music', methods=['GET', 'POST'])
def music():
    filter_form = FilterForm()

    filter_form.artist.choices = [(str(artist.artist_id), artist.name)
                                  for artist in db.session.query(Artists.artist_id, Artists.name).all()]
    filter_form.artist.choices.insert(0, ('no_filter', 'No Filter'))

    filter_form.genre.choices = [(str(genre.genre_id), genre.name)
                                 for genre in db.session.query(Genres.genre_id, Genres.name).all()]
    filter_form.genre.choices.insert(0, ('no_filter', 'No Filter'))

    popular_products = Products.query.join(OrderItems, Products.product_id == OrderItems.fk_product_id) \
        .group_by(Products.product_id)\
        .order_by(func.sum(OrderItems.quantity).desc()) \
        .limit(10).all()

    products = db.session.query(Products).join(Albums).join(Artists).join(
        AlbumGenre).join(Genres).filter(Products.type == 'music')

    if filter_form.validate_on_submit():
        print(request.form['artist'])
        return redirect(url_for('categories.music_filters', artist=request.form['artist'], genre=request.form['genre']))

    products = products.all()

    return render_template('categoryPage.html', page_name="music", products=products, popular_products=popular_products, filter_form=filter_form)


@category_bp.route('/filters')
def music_filters():
    products = Products.query.filter_by(type='music').join(Albums).join(Artists).join(
        AlbumGenre).join(Genres)
    print(request.args)
    genre = request.args.get('genre')
    artist = request.args.get('artist')
    if artist != 'no_filter':
        # Do artist filtering
        products = products.filter(
            Artists.artist_id == artist)
    if genre != 'no_filter':
        # Do genre filtering
        print(request.args.get('genre'))
        products = products.filter(
            Genres.genre_id == genre)
    products = products.all()

    return render_template('musicFilters.html', products=products, genre=genre, artist=artist)


@category_bp.route('/<int:product_id>')
def get_product_page(product_id: int):
    product = db.session.query(Products).filter(
        Products.product_id == product_id).first()
    album = db.session.query(Albums).filter(
        Albums.fk_product_id == product.product_id).first()
    if product:
        return render_template('productPage.html', product=product, album=album)
    else:
        return 'Product not found', 404


@category_bp.route('/animals')
def animals():
    return render_template('categoryPage.html', page_name="Animals")


@category_bp.route('/books')
def books():
    return render_template('categoryPage.html', page_name="Books")


@category_bp.route('/carparts')
def car_parts():
    return render_template('categoryPage.html', page_name="Car Parts")


@category_bp.route('/phones')
def phones():
    return render_template('categoryPage.html', page_name="Phones")


@category_bp.route('/sports')
def sports():
    return render_template('categoryPage.html', page_name="Sports")
