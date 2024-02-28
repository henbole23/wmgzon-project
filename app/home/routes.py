from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, login_manager
from app.forms import LoginForm, RegisterForm, SearchForm

from app.models import Products, Users, Orders
from app.extensions import db, bcrypt

# Initialisation of the home blueprint
home_bp = Blueprint('home', __name__, template_folder='templates')


# Route for the landing page of the site

@home_bp.route('/')
def home():
    """Function for rendering the home page"""

    # Query to retrieve products recently added to the database which are populated in a bootstrap carousel
    recently_added = db.session.query(Products).order_by(
        Products.date_added.desc()).limit(5).all()
    # Query which retrieves all products in teh database
    products = db.session.query(Products).all()
    return render_template('index.html', products=products, recently_added=recently_added)


# Route for the account registration page

@home_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Function for rendering register page and handling registration"""

    # Initialises the register form class
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        # Queries database for users with the submitted email
        user = db.session.query(Users).filter_by(
            email=request.form['email']).first()
        # If user doesn't exist
        if user is None:
            # Creates a User object which contains register form data
            user = Users(username=register_form.username.data, password=bcrypt.generate_password_hash(
                register_form.password.data), email=register_form.email.data)
            db.session.add(user)
            db.session.commit()
            # Logs the user in to the flask_login management system
            login_user(user)
            return redirect(url_for('home.home'))
        else:
            # Notifies user that account already exists
            flash('User already exists. Please Log In', 'warning')
            return redirect(url_for('home.login'))
    else:
        for error in register_form.errors:
            print(error)
            # Notifies user of any errors relating to form
            flash(str(error), 'warning')
        print(f"Register Form VALID: {register_form.validate_on_submit()}")
    return render_template('register.html', form=register_form)


# Route for user login

@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Function for rendering the login page and handling logins"""

    # Initialises the login form class
    login_form = LoginForm()

    if login_form.validate_on_submit():
        print(f"form Valid: {login_form.validate_on_submit()}")
        # Queries database for user where username is from form entry
        user = db.session.query(Users).filter_by(
            username=login_form.username.data).first()
        # If user exists
        if user:
            # Checks whether password matches the password hash in the database
            if bcrypt.check_password_hash(user.password, login_form.password.data):
                login_user(user)
                # If user has type admin
                if user.type == "Admin":
                    return redirect(url_for('admin.admin_home'))
                # If user has type customer
                else:
                    return redirect(url_for('home.home'))
            else:
                print("Password Invalid")
                flash("Incorrect Password", 'warning')
        else:
            print("User Invalid")
            flash("User Doesn't Exist", 'danger')

    return render_template('login.html', form=login_form)


# Route for logout

@home_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    """Function which handles user logout"""

    logout_user()
    flash("You have logged out successfully", 'success')
    return redirect(url_for('home.home'))


# Route for product seach

@home_bp.route('/search', methods=['POST'])
def search():
    """Function which handles product search and rendering seach template"""

    # Initialises the search form class
    search_form = SearchForm()

    if search_form.validate_on_submit():
        # Retrieves the search data
        search_value = search_form.search_field.data
        # Queries database for products which match the product name
        matching_products = db.session.query(Products).filter(
            Products.name.like('%' + search_value + '%'))  # type: ignore
        # Orders the data by name
        matching_products = matching_products.order_by(
            Products.name).all()  # type: ignore

        return render_template('search.html', search_form=search_form, search_value=search_value, products=matching_products)
    else:
        flash("Input Required", 'warning')
        return redirect(url_for('home.home'))


# Route for account page

@home_bp.route('/account/<username>')
@login_required
def account(username):
    """Function which renders account page"""
    # Queries database for account logged in
    account = db.session.query(Users).filter_by(username=username).first()
    # Queries database for orders related to logged in account
    orders = db.session.query(Orders).filter_by(
        fk_user_id=account.user_id).all()  # type: ignore

    return render_template('account.html', orders=orders)
