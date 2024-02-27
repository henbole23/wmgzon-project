from flask import Blueprint, redirect, render_template, request, url_for
from sqlalchemy import func

from app.forms import FilterForm
from app.models import AlbumGenre, Albums, Artists, Genres, OrderItems, Products
from app.extensions import db

# Initialisation of the category blueprint
category_bp = Blueprint('categories', __name__, template_folder='templates')


# Route for music category

@category_bp.route('/music', methods=['GET', 'POST'])
def music():
    """Function for rendering the music category page"""

    # Initialises the filter form class
    filter_form = FilterForm()

    # Sets the options for the artists filter
    filter_form.artist.choices = [(str(artist.artist_id), artist.name)
                                  for artist in db.session.query(Artists.artist_id, Artists.name).all()]
    # Adds a no filter option for the artist filter
    filter_form.artist.choices.insert(0, ('no_filter', 'No Filter'))

    # Sets the options for the genre filter
    filter_form.genre.choices = [(str(genre.genre_id), genre.name)
                                 for genre in db.session.query(Genres.genre_id, Genres.name).all()]
    # Adds a no filter option for the genre filter
    filter_form.genre.choices.insert(0, ('no_filter', 'No Filter'))

    if filter_form.validate_on_submit():
        return redirect(url_for('categories.music_filters', artist=filter_form.artist.data, genre=filter_form.genre.data))

    # Queries database for the top 10 most popular products determined by quantity sold
    popular_products = Products.query.join(OrderItems, Products.product_id == OrderItems.fk_product_id) \
        .group_by(Products.product_id)\
        .order_by(func.sum(OrderItems.quantity).desc()) \
        .limit(10).all()

    # Sets query for collating the music products and their related data
    products = db.session.query(Products).join(Albums).join(Artists).join(
        AlbumGenre).join(Genres).filter(Products.type == 'music')

    # Queries the database
    products = products.all()

    return render_template('categoryPage.html', page_name="music", products=products, popular_products=popular_products, filter_form=filter_form)


# Route for the filtered products page

@category_bp.route('/filters')
def music_filters():
    """Function for rendering the filter page for music products"""

    # Queries database for music products and their relevant data
    products = Products.query.filter_by(type='music').join(Albums).join(Artists).join(
        AlbumGenre).join(Genres)
    # Retrieves the chosen genre for filtering
    genre = request.args.get('genre')
    # Retireves the chosen artist for filtering
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


# Route for individual product page

@category_bp.route('/<int:product_id>')
def get_product_page(product_id: int):
    """Function for rendering individual product page"""

    # Queries database for product based on id
    product = db.session.query(Products).filter(
        Products.product_id == product_id).first()
    # Queries database for album based on id
    album = db.session.query(Albums).filter(
        Albums.fk_product_id == product.product_id).first()
    # If product exists
    if product:
        return render_template('productPage.html', product=product, album=album)
    else:
        return 'Product not found', 404


# Route for animals category

@category_bp.route('/animals')
def animals():
    """Function for rendering the animals category page"""
    return render_template('categoryPage.html', page_name="Animals")


# Route for books category

@category_bp.route('/books')
def books():
    """Function for rendering the books category page"""
    return render_template('categoryPage.html', page_name="Books")


# Route for car parts category

@category_bp.route('/carparts')
def car_parts():
    """Function for rendering the carparts category page"""
    return render_template('categoryPage.html', page_name="Car Parts")


# Route for phones category

@category_bp.route('/phones')
def phones():
    """Function for rendering the phones category page"""
    return render_template('categoryPage.html', page_name="Phones")

# Route for sports category


@category_bp.route('/sports')
def sports():
    """Function for rendering the sports category page"""
    return render_template('categoryPage.html', page_name="Sports")
