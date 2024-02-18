from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_bcrypt import Bcrypt
from flask_session import Session
from datetime import datetime, timedelta
from forms import LoginForm, RegisterForm, ProductForm, CheckoutForm
import secrets

# Create Flask Instance
app = Flask(__name__)
# Add Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///wmgzon.db"

app.config["SECRET_KEY"] = secrets.token_urlsafe(16)

bcrypt = Bcrypt(app)
# Initialise the Database
db = SQLAlchemy(app)

# Initialise Sessions
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
Session(app)



# Flask_Login Config
login_manager = LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create User Model
class Users(db.Model, UserMixin):
    __tablename__ = "USERS"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    type = db.Column(db.String(25), default="Customer", nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def get_id(self):
           return (self.user_id)

class Products(db.Model):
    __tablename__ = "PRODUCTS"
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String, nullable=False)

class BasketItems(db.Model):
    __tablename__ = "BASKETITEMS"
    item_id = db.Column(db.Integer, primary_key=True)
    fk_product_id = db.Column(db.Integer, db.ForeignKey("PRODUCTS.product_id"), nullable=False)
    fk_user_id = db.Column(db.Integer, db.ForeignKey("USERS.user_id"), nullable=False)

@app.route('/')
def index():
    products = db.session.query(Products).all()

    return render_template('index.html', products=products)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    products = db.session.query(Products).all()
    form=ProductForm()
    if form.validate_on_submit():
        if 'product_id' in request.form:
            product = db.session.query(Products).get(request.form['product_id'])
            product.name = request.form['name'] # type: ignore
            product.image = request.form['image'] # type: ignore
            product.price = request.form['price'] # type: ignore
            product.type = request.form['type'] # type: ignore

            db.session.commit()
            flash("Product Edited Successfully")
            return redirect(url_for('admin'))
        else:
            product = Products(name=request.form['name'],
                                image=request.form['image'],
                                price=request.form['price'],
                                type=request.form['type']) # type: ignore
            db.session.add(product)
            db.session.commit()
            flash("Product Added Successfully")
            return redirect(url_for('admin'))
    return render_template('admin.html', products=products, form=form)


@app.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete_product(id):
    product = db.session.query(Products).get(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product Deleted Successfully")

    return redirect(url_for('admin'))
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = Users.query.filter_by(email=request.form['email']).first()
        if user is None:
            user = Users(username=request.form['username'],
                         password=bcrypt.generate_password_hash(request.form['password']),
                         email=request.form['email']) # type: ignore
            db.session.add(user)
            db.session.commit()

            return redirect(url_for('index'))
    
    print(f"FORM VALID: {register_form.validate_on_submit()}")
    return render_template('register.html', form=register_form)
    # else:
    #     flash("Field Required")
    #     print("Empty Fields")
    #     return render_template('register.html', form=register_form)


@app.route('/login', methods=['GET', 'POST']) 
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print(f"Form Valid: {login_form.validate_on_submit()}")
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
                flash("Incorrect Password")
        else:
            print("User Invalid")
            flash("User Doesn't Exist")
    return render_template('login.html', form=login_form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully")
    return redirect(url_for('index'))

@app.route('/music/<int:product_id>')
def get_product_page(product_id: int):
    product = db.session.query(Products).filter(Products.product_id == product_id).first()
    if product:
        return render_template('productPage.html', product=product)
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

    basket_ids = [id['product_id'] for id in basket_data if 'product_id' in id]
    product_data = db.session.query(Products).filter(Products.product_id.in_(basket_ids)).all()

    

    data = zip(product_data, basket_data)
    print(data)
    return render_template('basket.html', data=data, data_check=basket_data, total_price=totalPriceCalc(basket_data, product_data))

@app.route('/checkout')
def checkout():
    form = CheckoutForm()
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

@app.route('/music')
def music():
    products = db.session.query(Products).filter_by(type="music")
    return render_template('categoryPage.html', page_name="Music", products=products)

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
