from flask import render_template, redirect, url_for, request, flash, Blueprint
from ..models import Products
from ..__init__ import db

admin_bp = Blueprint('admin_bp', __name__, template_folder='templates', static_folder='static')

@admin_bp.route('/') 
def admin_home():
    return render_template('home.html')

@admin_bp.route('/products')
def admin_product_manager():
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
