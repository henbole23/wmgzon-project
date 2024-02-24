from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import func

from app.forms import MusicProductForm, ProductForm, SongForm, UserEditForm
from app.models import AlbumGenre, Albums, Artists, Genres, OrderItems, Products, Songs, Users
from app.extensions import db
from app.decorators import role_required

# Initialisation of  admin blueprint
admin_bp = Blueprint('admin', __name__, template_folder='templates')


@admin_bp.route('/')
# Route for admin home page
@role_required('Admin')
def admin_home():
    return render_template('admin.html')


@admin_bp.route('/products', methods=['GET', 'POST'])
# Route for admin product management page
@role_required('Admin')
def admin_products():
    products = db.session.query(Products).all()
    product_form = ProductForm()
    # If request is PUT to update a product
    if request.method == 'PUT' and product_form.validate():
        # Checks if product already exists
        product = Products.query.get_or_404(product_form.product_id.data)

        product_form.populate_obj(product)
        db.session.commit()

        db.session.add(product)
        db.session.commit()
        flash('Product Edited Successfully', 'success')
        return redirect(url_for('admin.admin_products'))
    # If request is a POST to add a new product
    elif product_form.validate_on_submit():
        product = Products(name=request.form['product_name'],
                           image=request.form['image'],
                           price=request.form['price'],
                           type=request.form['type'],
                           stock=request.form['stock'])
        db.session.add(product)
        db.session.commit()

        flash('Product Added Successfully', 'success')
        return redirect(url_for('admin.admin_products'))

    return render_template('adminProducts.html', products=products, product_form=product_form)

# Route for PUT requests to update product details


@admin
@admin_bp.route('/products/<id>', methods=['PUT'])
@role_required('Admin')
def update_product(id):
    """ Function which handles updating products"""
    product = Products.query.get_or_404(id)

    form = ProductForm(obj=product)

    if form.validate_on_submit():

        flash('Product Edited Successfully', 'success')
        return redirect(url_for('admin_products'))

    return render_template('adminProductUpdate.html', form=form)


@admin_bp.route('/products/details/<id>/set', methods=['GET', 'POST'])
@role_required('Admin')
def set_product_details(id):
    details_form = MusicProductForm()
    details_form.genres.choices = [
        (genre.genre_id, genre.name) for genre in Genres.query.all()]

    if details_form.validate_on_submit():
        artist_name = request.form['artist_name']

        artist = Artists.query.filter_by(name=artist_name).first()
        # Checks for if the artist already exists in the database
        if artist == None:
            artist = Artists(name=request.form['artist_name'],
                             bio=request.form['artist_bio'])

            db.session.add(artist)
            db.session.commit()

        # Adds the album to the database
        new_album = Albums(name=request.form['album_name'],
                           year=request.form['year'],
                           fk_product_id=id,
                           fk_artist_id=artist.artist_id)

        for genre in request.form.getlist('genres'):
            album_genre = AlbumGenre(fk_album_id=id, fk_genre_id=genre)
            db.session.add(album_genre)
            db.session.commit()

        db.session.add(new_album)
        db.session.commit()

        return redirect(url_for('admin.admin_products'))

    return render_template('adminProductDetailsSet.html', details_form=details_form)


@admin_bp.route('/products/details/<id>', methods=['GET', 'POST'])
@role_required('Admin')
def admin_product_details(id):
    product = Products.query.get(id)
    genres = Genres.query.join(AlbumGenre).filter_by(
        fk_album_id=product.music_info[0].album_id)
    product = db.session.query(Products).filter_by(product_id=id).first()

    song_form = SongForm()
    if song_form.validate_on_submit():
        # Checks if product already exists
        if 'song_id' in request.form:
            song = db.session.query(Products).get(
                request.form['song_id'])
            song.name = request.form['name']
            song.length = request.form['length']

            db.session.add(song)
            db.session.commit()
            flash('Product Edited Successfully', 'success')
            return redirect(url_for('admin.admin_products'))
        else:
            song = Songs(name=request.form['name'],
                         length=request.form['length'],
                         fk_album_id=product.music_info[0].album_id)

            db.session.add(song)
            db.session.commit()

            return redirect(url_for('admin.admin_product_details', id=id))

    return render_template('adminProductDetails.html', product_id=id, product=product, genres=genres, song_form=song_form)


@admin_bp.route('products/delete/song/<product_id>/<song_id>', methods=['DELETE'])
@role_required('Admin')
def delete_song(product_id, song_id):
    song = db.session.query(Songs).get(song_id)
    if song:
        db.session.delete(song)
        db.session.commit()
        flash('Song Deleted Successfully', 'success')
    else:
        flash('Song Not Found', 'Error')

    return redirect(url_for('admin.admin_product_details', id=product_id))


@admin_bp.route('products/delete/<id>', methods=['GET', 'POST'])
@role_required('Admin')
def delete_product(id):
    product = db.session.query(Products).get(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product Deleted Successfully', 'success')

    return redirect(url_for('admin.admin_products'))


@admin_bp.route('/users', methods=['GET', 'POST'])
@role_required('Admin')
def admin_users():
    user_form = UserEditForm()
    users = db.session.query(Users).all()

    if user_form.validate_on_submit():
        user = db.session.query(Users).filter_by(
            username=request.form['username']).first()
        user.username = request.form['username']
        user.email = request.form['email']
        user.type = request.form['type']

        db.session.add(user)
        db.session.commit()
        flash('User Edited Successfully', 'success')
        return redirect(url_for('admin.admin_users'))

    return render_template('adminUsers.html', user_form=user_form, users=users)


@admin_bp.route('users/delete/<id>', methods=['POST'])
@role_required('Admin')
def delete_user(id):
    if current_user.type != 'Admin':
        flash('USER UNAUTHORISED', 'danger')
        return redirect(url_for('home.home'))
    user = db.session.query(Users).get(id)
    db.session.delete(user)
    db.session.commit()
    flash('Product Deleted Successfully', 'success')

    return redirect(url_for('admin.admin_users'))


@admin_bp.route('/analysis')
@role_required('Admin')
def admin_analysis():
    most_popular_products = db.session.query(Products.name, func.sum(OrderItems.quantity).label('total_quantity')) \
        .join(OrderItems) \
        .group_by(Products.name) \
        .order_by(func.sum(OrderItems.quantity).desc()) \
        .limit(5) \
        .all()

    popular_labels = [product[0] for product in most_popular_products]
    popular_values = [product[1] for product in most_popular_products]
    print(popular_labels)
    print(popular_values)
    return render_template('adminAnalysis.html', popular_labels=popular_labels, popular_values=popular_values)
