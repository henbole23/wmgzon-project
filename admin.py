from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from sqlalchemy import func

from forms import ProductForm, UserEditForm
from models import OrderItems, Products, Users
from extensions import db

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/')
def admin():
    return render_template('admin.html')

@admin_bp.route('/products')
def admin_products():
    if current_user.type != 'Admin':
        flash('USER UNAUTHORISED', 'danger')
        return redirect(url_for('index'))
    
    products = db.session.query(Products).all()
    product_form = ProductForm()
    
    if product_form.validate_on_submit():
        # Checks if product already exists
        if 'product_id' in request.form:
            product = db.session.query(Products).get(request.form['product_id'])
            product.name = request.form['product_name'] # type: ignore
            product.image = request.form['image'] # type: ignore
            product.price = request.form['price'] # type: ignore
            product.type = request.form['type'] # type: ignore
            product.stock = request.form['stock'] # type: ignore
            
            db.session.add(product)
            db.session.commit()
            flash("Product Edited Successfully", 'success')
            return redirect(url_for('admin'))
        else:
            product = Products(name=request.form['product_name'],
                                image=request.form['image'],
                                price=request.form['price'],
                                type=request.form['type'],
                                stock=request.form['stock']) # type: ignore
            db.session.add(product)
            db.session.commit()
                        
            flash("Product Added Successfully", 'success')
            return redirect(url_for('admin'))
    return render_template('adminProducts.html', products=products, product_form=product_form)

@admin_bp.route('/products/details/<id>')
def admin_product_details(id):
    return render_template('adminProductDetails.html')

@admin_bp.route('products/delete/<id>', methods=['GET', 'POST'])
def delete_product(id):
    if current_user.type != 'Admin':
        flash('USER UNAUTHORISED', 'danger')
        return redirect(url_for('index'))
    product = db.session.query(Products).get(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product Deleted Successfully", 'success')

    return redirect(url_for('admin_products'))


@admin_bp.route('/users', methods=['GET', 'POST'])
def admin_users():
    user_form = UserEditForm()
    users = db.session.query(Users).all()
    
    if user_form.validate_on_submit():
        user = db.session.query(Users).filter_by(username=request.form['username']).first()
        user.username = request.form['username'] # type: ignore
        user.email = request.form['email'] # type: ignore
        user.type = request.form['type'] # type: ignore

        db.session.add(user)
        db.session.commit()
        flash("User Edited Successfully", 'success')
        return redirect(url_for('admin.admin_users'))
    
    return render_template('adminUsers.html', user_form=user_form, users=users)

@admin_bp.route('users/delete/<id>', methods=['GET', 'POST'])
def delete_user(id):
    if current_user.type != 'Admin':
        flash('USER UNAUTHORISED', 'danger')
        return redirect(url_for('index'))
    user = db.session.query(Users).get(id)
    db.session.delete(user)
    db.session.commit()
    flash("Product Deleted Successfully", 'success')

    return redirect(url_for('admin.admin_users'))

@admin_bp.route('/analysis')
def admin_analysis():
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
    return render_template('adminAnalysis.html', popular_labels=popular_labels, popular_values=popular_values)