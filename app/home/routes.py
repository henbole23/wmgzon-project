from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user, login_manager
from app.forms import LoginForm, RegisterForm, SearchForm

from app.models import Products, Users, Orders
from app.extensions import db, bcrypt

home_bp = Blueprint('home', __name__, template_folder='templates')


@home_bp.route('/')
def home():
    recently_added = db.session.query(Products).order_by(
        Products.date_added.desc()).limit(5).all()
    products = db.session.query(Products).all()
    return render_template('index.html', products=products, recently_added=recently_added)


@home_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        user = db.session.query(Users).filter_by(
            email=request.form['email']).first()
        if user is None:
            user = Users(username=request.form['username'],
                         password=bcrypt.generate_password_hash(
                             request.form['password']),
                         email=request.form['email'])  # type: ignore
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('home.home'))
        else:
            flash('User already exists. Please Log In', 'warning')
            return redirect(url_for('home.login'))
    else:
        for error in register_form.errors:
            print(error)
            flash(str(error), 'warning')
        print(f"Register Form VALID: {register_form.validate_on_submit()}")
    return render_template('register.html', form=register_form)


@home_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        print(f"form Valid: {login_form.validate_on_submit()}")
        user = db.session.query(Users).filter_by(
            username=request.form['username']).first()
        if user:
            print("User Valid")
            if bcrypt.check_password_hash(user.password, request.form['password']):
                print("Password Valid")
                login_user(user)
                if user.type == "Admin":
                    return redirect(url_for('admin.admin'))
                else:
                    return redirect(url_for('home.home'))
            else:
                print("Password Invalid")
                flash("Incorrect Password", 'warning')
        else:
            print("User Invalid")
            flash("User Doesn't Exist", 'danger')
    return render_template('login.html', form=login_form)


@home_bp.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    flash("You have logged out successfully", 'success')
    return redirect(url_for('home.home'))


@home_bp.route('/search', methods=['POST'])
def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        search_value = request.form['search_field']
        matching_products = db.session.query(Products).filter(
            Products.name.like('%' + search_value + '%'))  # type: ignore
        matching_products = matching_products.order_by(Products.name).all()

        return render_template('search.html', search_form=search_form, search_value=search_value, products=matching_products)
    else:
        flash("Input Required", 'warning')
        return redirect(url_for('home.home'))


@home_bp.route('/account/<username>')
@login_required
def account(username):
    account = db.session.query(Users).filter_by(username=username).first()
    orders = db.session.query(Orders).filter_by(
        fk_user_id=account.user_id).all()
    print(orders)
    return render_template('account.html', orders=orders)
