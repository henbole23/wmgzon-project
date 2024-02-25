from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import func

from app.forms import MusicProductForm, ProductForm, SongForm, UserEditForm
from app.models import AlbumGenre, Albums, Artists, Genres, OrderItems, Orders, Products, Songs, Users
from app.extensions import db
from app.decorators import role_required

# Initialisation of admin blueprint
admin_bp = Blueprint('admin', __name__, template_folder='templates')


# Route for admin home page

@admin_bp.route('/')
@role_required('Admin')
def admin_home():
    return render_template('admin.html')


# Route for admin product management page

@admin_bp.route('/products', methods=['GET', 'POST'])
@role_required('Admin')
def admin_products():
    """Function for admin product page which displays all products and also allows for editing and deleting products"""

    # Queries database for all products
    products = db.session.query(Products).all()
    # Initialise ProductForm class
    product_form = ProductForm()
    # If request is PUT to update a product
    if product_form.validate():
        # Checks if product already exists
        if product_form.product_id.data:
            # Edit (PUT) request for updating existing product
            product = Products.query.get(product_form.product_id.data)
            product_form.populate_obj(product)
            db.session.commit()

            flash('Product Edited Successfully', 'success')
            return redirect(url_for('admin.admin_products'))
        else:
            # Add (POST) request for new product
            product = Products(name=request.form['name'],
                               image=request.form['image'],
                               price=request.form['price'],
                               type=request.form['type'],
                               stock=request.form['stock'])
            db.session.add(product)
            db.session.commit()

            flash('Product Added Successfully', 'success')
            return redirect(url_for('admin.admin_products'))

    return render_template('adminProducts.html', products=products, product_form=product_form)


# Route for deleting products based on id

@admin_bp.route('products/delete/<int:id>', methods=['GET', 'POST'])
@role_required('Admin')
def delete_product(id):
    """Function for deleting products based on id"""

    # Queries datababase for product deletion
    product = db.session.query(Products).get(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product Deleted Successfully', 'success')

    return redirect(url_for('admin.admin_products'))


# Route for viewing product details and CRUD functionality for songs associated with an album

@admin_bp.route('/products/details/<int:id>', methods=['GET', 'POST'])
@role_required('Admin')
def admin_product_details(id):
    """Function for displaying album data for music products and CRUD functionality for songs"""

    # Queries database for product based on id
    product = Products.query.get(id)
    # Queries database to retrieve genres related to the album
    genres = Genres.query.join(AlbumGenre).filter_by(
        fk_album_id=product.music_info.album_id)
    product = db.session.query(Products).filter_by(product_id=id).first()

    # Initialises SongForm form class
    song_form = SongForm()
    if song_form.validate_on_submit():
        # Checks if song already exists
        if song_form.song_id.data:
            song = db.session.query(Songs).get(song_form.song_id.data)
            song_form.populate_obj(song)

            db.session.commit()

            flash('Song Edited Successfully', 'success')
            return redirect(url_for('admin.admin_product_details', id=id))
        else:
            song = Songs(name=song_form.name.data,
                         length=song_form.length.data,
                         fk_album_id=product.music_info.album_id)

            db.session.add(song)
            db.session.commit()

            flash('Song Added Successfully', 'success')
            return redirect(url_for('admin.admin_product_details', id=id))

    return render_template('adminProductDetails.html', product_id=id, product=product, genres=genres, song_form=song_form)


# Route for setting the product details

@admin_bp.route('/products/details/<int:id>/set', methods=['GET', 'POST'])
@role_required('Admin')
def set_product_details(id):
    # Initialise MusicProductForm class for music data
    details_form = MusicProductForm()
    # Extracts all the genres from the database for input
    details_form.genres.choices = [
        (genre.genre_id, genre.name) for genre in Genres.query.all()]

    if details_form.validate_on_submit():
        album_name = details_form.album_name.data
        year = details_form.year.data
        artist_name = details_form.artist_name.data
        bio = details_form.artist_bio.data

        artist = Artists.query.filter_by(name=artist_name).first()
        # Checks if the artist already exists in the database
        if artist == None:
            artist = Artists(name=artist_name, bio=bio)

            db.session.add(artist)
            db.session.commit()

        # Adds the album to the database
        new_album = Albums(name=album_name, year=year,
                           fk_product_id=id, fk_artist_id=artist.artist_id)

        # Updates the AlbumGenre table with genres that are associated with the album
        for genre in request.form.getlist('genres'):
            album_genre = AlbumGenre(fk_album_id=id, fk_genre_id=genre)
            db.session.add(album_genre)
            db.session.commit()

        db.session.add(new_album)
        db.session.commit()

        return redirect(url_for('admin.admin_products'))

    return render_template('adminProductDetailsSet.html', details_form=details_form)


# Route for deleting songs from albums

@admin_bp.route('products/details/delete/<int:product_id>/<int:song_id>', methods=['GET', 'POST'])
@role_required('Admin')
def delete_song(product_id, song_id):
    """Function for deleting songs from the database"""

    # Queries the database for song with correct id
    song = db.session.query(Songs).get(song_id)
    # If the song is in the database
    if song:
        # Deletes the song
        db.session.delete(song)
        db.session.commit()
        flash('Song Deleted Successfully', 'success')
    else:
        flash('Song Not Found', 'Error')

    return redirect(url_for('admin.admin_product_details', id=product_id))


# Route for managing users

@admin_bp.route('/users', methods=['GET', 'POST'])
@role_required('Admin')
def admin_users():
    """Function for loading the admin user management page"""

    # Initialises the user edit form class
    user_form = UserEditForm()
    # Queries the database for all user data
    users = db.session.query(Users).all()

    # If user edit form is submitted
    if user_form.validate_on_submit():
        # Queries the database for the user being edited
        user = db.session.query(Users).filter_by(
            username=user_form.username.data).first()
        # Updates the fields with data from the user_form
        user_form.populate_obj(user)
        db.session.commit()
        flash('User Edited Successfully', 'success')

    return render_template('adminUsers.html', user_form=user_form, users=users)


# Route for deleting users

@admin_bp.route('users/delete/<id>', methods=['GET', 'POST'])
@role_required('Admin')
def delete_user(id):
    # Queries the database for the user being deleted
    user = db.session.query(Users).get(id)
    db.session.delete(user)
    db.session.commit()
    flash('Product Deleted Successfully', 'success')

    return redirect(url_for('admin.admin_users'))


# Route for website analysis

@admin_bp.route('/analysis')
@role_required('Admin')
def admin_analysis():
    """Function for querying and displaying website data for analysis"""

    # Queries and aligns orderitem data based on quantity and returns the top 5 most popular
    most_popular_products = db.session.query(Products.name, func.sum(OrderItems.quantity).label('total_quantity')) \
        .join(OrderItems) \
        .group_by(Products.name) \
        .order_by(func.sum(OrderItems.quantity).desc()) \
        .limit(5) \
        .all()

    # Queries and aligns order data based on money made at a given time
    revenue_over_time = db.session.query(func.datetime(Orders.date_added).label('datetime'), func.sum(OrderItems.quantity * Products.price).label('revenue')).join(OrderItems, Orders.order_id == OrderItems.fk_order_id)\
        .join(Products, OrderItems.fk_product_id == Products.product_id)\
        .group_by(func.extract('hour', Orders.date_added))\
        .order_by(func.extract('hour', Orders.date_added)).all()

    print(revenue_over_time)
    # Saves the labels and values for the top 5 most popular products in a tuple
    most_popular = ([label[0] for label in most_popular_products], [
                    value[1] for value in most_popular_products])
    # Saves the labels and values for the revenue earnt over time
    revenue_time = ([label[0] for label in revenue_over_time],
                    [value[1] for value in revenue_over_time])

    return render_template('adminAnalysis.html', most_popular=most_popular, revenue_time=revenue_time)
