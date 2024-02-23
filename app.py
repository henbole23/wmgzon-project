from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from flask_session import Session
from sqlalchemy import desc, func
from datetime import timedelta
from forms import LoginForm, RegisterForm, ProductForm, CheckoutForm,  SearchForm, MusicProductForm, SongForm, FilterForm, SortForm
import secrets


from extensions import db, bcrypt, login_manager
from models import Users, Products, Albums, Songs, Artists, Orders, OrderItems, Genre, AlbumGenre

from admin import admin_bp
from home import home_bp
def create_app():
    app = Flask(__name__)
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wmgzon.db"
    app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
    app.config["SESSION_PERMANENT"] = True
    app.config["SESSION_TYPE"] = "filesystem"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

    Session(app)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
        
    return app


app = create_app()

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Users).get(int(user_id))

@app.context_processor
def base():
    search_form = SearchForm()
    return dict(form=search_form)

@app.route('/search', methods=['POST'])
def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_value = request.form['search_field']
        matching_products = db.session.query(Products).filter(Products.name.like('%' + search_value + '%'))
        matching_products = matching_products.order_by(Products.name).all()

        return render_template('search.html', search_form=search_form, search_value=search_value, products=matching_products)
    else:
        flash("Input Required", 'warning')
        return redirect(url_for('index'))



# @app.route('/admin', methods=['GET', 'POST'])
# @login_required
# def admin():
#     if current_user.type != 'Admin':
#         flash('USER UNAUTHORISED', 'danger')
#         return redirect(url_for('index'))
    
#     products = db.session.query(Products).all()
#     product_form = ProductForm()
    
#     if product_form.validate_on_submit():
#         # Checks if product already exists
#         if 'product_id' in request.form:
#             product = db.session.query(Products).get(request.form['product_id'])
#             product.name = request.form['product_name'] # type: ignore
#             product.image = request.form['image'] # type: ignore
#             product.price = request.form['price'] # type: ignore
#             product.type = request.form['type'] # type: ignore
#             product.stock = request.form['stock'] # type: ignore
            
#             db.session.add(product)
#             db.session.commit()
#             flash("Product Edited Successfully", 'success')
#             return redirect(url_for('admin'))
#         else:
#             product = Products(name=request.form['product_name'],
#                                 image=request.form['image'],
#                                 price=request.form['price'],
#                                 type=request.form['type'],
#                                 stock=request.form['stock']) # type: ignore
#             db.session.add(product)
#             db.session.commit()
                        
#             flash("Product Added Successfully", 'success')
#             return redirect(url_for('admin'))
#     return render_template('admin.html', products=products, product_form=product_form)

@app.route('/admin/analysis')
@login_required
def product_analysis():
    if current_user.type != 'Admin':
        flash('USER UNAUTHORISED', 'danger')
        return redirect(url_for('index'))
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
    return render_template('productAnalysis.html', popular_labels=popular_labels, popular_values=popular_values)

@app.route('/product_details/<id>', methods=['GET', 'POST'])
@login_required
def product_details(id):
    if current_user.type != 'Admin':
        flash('USER UNAUTHORISED', 'danger')
        return redirect(url_for('index'))
    product = db.session.query(Products).get(id)
    details_form = MusicProductForm()
    details_form.genres.choices = [(genre.genre_id, genre.name) for genre in db.session.query(Genre).all()]
    song_form = SongForm()
    
    # if song_form.validate_on_submit():
    #     song = Songs(name=request.form['name'],
    #                  length=request.form['length'],
    #                  fk_album_id=product.music_info[0].album_id) #type: ignore
        
    #     db.session.add(song)
    #     db.session.commit()
        
    #     return redirect(url_for('product_details', id=id))
    
    if details_form.validate_on_submit():
        album = db.session.query(Albums).filter(Albums.fk_product_id == id).first()
        artist = db.session.query(Artists).filter(Artists.name == request.form['artist_name']).first()
        # If artist currently isn't in database
        if artist is None:
            artist = Artists(name=request.form['artist_name'],
                             bio=request.form['artist_bio']) # type: ignore
            db.session.add(artist)
            db.commit()
        
        album = Albums(name=request.form['album_name'],
                        year=request.form['year'],
                        fk_artist_id=artist.artist_id,
                        fk_product_id=id) # type: ignore
        
        db.session.add(album)
        db.session.commit()
        
        for genre in request.form.getlist('genres'):
            link = AlbumGenre(fk_album_id=album.album_id, fk_genre_id=genre)
            
            db.session.add(link)
            db.session.commit()
        
        
        flash("Product Details Added Successfully", 'success')
        return redirect(url_for('admin'))
    else:
        print(details_form.errors)

    return render_template('productDetails.html',product_id=id, product=product, details_form=details_form, song_form=song_form)


@app.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    if current_user.type != 'Admin':
        flash('USER UNAUTHORISED', 'danger')
        return redirect(url_for('index'))
    product = db.session.query(Products).get(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product Deleted Successfully", 'success')

    return redirect(url_for('admin'))

@app.route('/account/<username>')
@login_required
def account(username):
    account = db.session.query(Users).filter_by(username=username).first()
    orders = db.session.query(Orders).filter_by(fk_user_id=account.user_id).all()
    print(orders)
    return render_template('account.html', orders=orders)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = db.session.query(Users).filter_by(email=request.form['email']).first()
        if user is None:
            user = Users(username=request.form['username'],
                         password=bcrypt.generate_password_hash(request.form['password']),
                         email=request.form['email']) # type: ignore
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
    
    print(f"filter_form VALID: {register_form.validate_on_submit()}")
    return render_template('register.html', form=register_form)


@app.route('/login', methods=['GET', 'POST']) 
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print(f"form Valid: {login_form.validate_on_submit()}")
        user = Users.query.filter_by(username=request.form['username']).first()
        if user:
            print("User Valid")
            if bcrypt.check_password_hash(user.password, request.form['password']):
                print("Password Valid")
                login_user(user)
                if user.type == "Admin":
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('index'))
            else:
                print("Password Invalid")
                flash("Incorrect Password", 'warning')
        else:
            print("User Invalid")
            flash("User Doesn't Exist", 'danger')
    return render_template('login.html', form=login_form)

@login_manager.unauthorized_handler
def unauthorised_user():
    flash('Please Log In First', 'warning')
    return redirect(url_for('login'))

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully", 'success')
    return redirect(url_for('index'))

@app.route('/music/<int:product_id>')
def get_product_page(product_id: int):
    product = db.session.query(Products).filter(Products.product_id == product_id).first()
    album = db.session.query(Albums).filter(Albums.fk_product_id == product.product_id).first()
    if product:
        return render_template('productPage.html', product=product, album=album)
    else:
        return 'Product not found', 404

@app.route('/add_to_basket', methods=['POST', 'GET'])
def add_to_basket():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    item = {'product_id': product_id, 'quantity': quantity}
    print(product_id)
    # Creates basket and adds item if basket not already exist
    if 'basket' not in session:
        session['basket'] = [item]
    else:
        # Adds product to basket
        if not any(product_id in product['product_id'] for product in session['basket']):
            session['basket'].append(item)
        # Updates quantity of item already in basket
        else:
            for product in session['basket']:
                if product['product_id'] == item['product_id']:
                    product['quantity'] += quantity

    return redirect(url_for('view_basket'))

@app.route('/remove_from_basket', methods=['POST'])
def remove_from_basket():
    product_id = request.form['product_id']

    basket = session.get('basket', [])

    basket = [item for item in basket if item.get('product_id') != product_id]
    session['basket'] = basket
    return redirect(url_for('view_basket'))

@app.route('/basket')
def view_basket():
    basket_data = session.get('basket', [])
    print(basket_data)
    basket_ids = [id['product_id'] for id in basket_data if 'product_id' in id]
    product_data = db.session.query(Products).filter(Products.product_id.in_(basket_ids)).all()

    data = zip(product_data, basket_data)
    print(data)
    return render_template('basket.html', data=data, data_check=basket_data, total_price=totalPriceCalc(basket_data, product_data))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()

    # if form.validate_on_submit():
    if request.method == 'POST':
        basket_data = session.get('basket', [])
        order = Orders(fk_user_id=current_user.user_id) # type: ignore
        db.session.add(order)
        db.session.commit()
        
        for data in basket_data:
            product = db.session.query(Products).filter(Products.product_id == data['product_id']).first()
            print(product)
            product.stock -= data['quantity'] # type: ignore
            db.session.add(product)
            db.session.commit()
            order_items = OrderItems(quantity=data['quantity'], fk_order_id=order.order_id, fk_product_id=data['product_id']) # type: ignore 
            db.session.add(order_items)
        
        db.session.commit()
        del session['basket']
        flash(f"Order {order.order_id} Submitted Successfully", 'success')
        return render_template('index.html', show_modal=True)

    else:
        print(form.errors)
        
        
    return render_template('checkout.html', form=form)

def totalPriceCalc(basket_data, product_data):
    total = 0

    for product in basket_data:
        id = int(product['product_id'])
        quantity = product['quantity']

        for product_item in product_data:
            if product_item.product_id == id:
                total += product_item.price * quantity

    return round(total, 2)

@app.route('/animals')
def animals():
    return render_template('categoryPage.html', page_name="Animals")

@app.route('/books')
def books():
    return render_template('categoryPage.html', page_name="Books")

@app.route('/carparts')
def car_parts():
    return render_template('categoryPage.html', page_name="Car Parts")

@app.route('/music', methods=['GET', 'POST'])
def music():
    filter_form = FilterForm()
    sort_form = SortForm()
    if 'music_filters' not in session:
        session['music_filters'] = {''}
    if 'music_sort' not in session:
        session['music_filters'] = {}
    
    filter_form.artist.choices = [(str(artist.artist_id), artist.name) for artist in db.session.query(Artists.artist_id, Artists.name).all()]
    filter_form.genre.choices = [(str(genre.genre_id), genre.name) for genre in db.session.query(Genre.genre_id, Genre.name).all()]

    popular_products = db.session.query(Products).join(OrderItems, Products.product_id == OrderItems.fk_product_id) \
                                                 .group_by(Products.product_id)\
                                                 .order_by(func.sum(OrderItems.quantity).desc()) \
                                                 .limit(10).all()

    products = db.session.query(Products).join(Albums).join(Artists).join(AlbumGenre).join(Genre).filter(Products.type == 'music')
    if request.method == 'POST':
        if filter_form.validate_on_submit():
            if filter_form.artist.data:
                products = products.filter(Artists.artist_id == request.form['artist'])
                session['music_filters']['artist'] = request.form['artist']
            if filter_form.genre.data:
                session['music_filters']['genre'] = request.form['genre']
                products = products.filter(Genre.genre_id == request.form['genre'])
                
        if request.form.get('sort') == 'ascend':
            products = products.order_by(Albums.year)
        else:
            products = products.order_by(desc(Albums.year))
        print(filter_form.errors)
    
    products = products.all()
    
    return render_template('categoryPage.html', page_name="music", products=products, popular_products=popular_products, filter_form=filter_form, sort_form=sort_form)

@app.route('/phones')
def phones():
    return render_template('categoryPage.html', page_name="Phones")

@app.route('/sports')
def sports():
    return render_template('categoryPage.html', page_name="Sports")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
