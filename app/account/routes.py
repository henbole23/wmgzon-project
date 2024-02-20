from flask import Blueprint



account_bp = Blueprint('account_bp', __name__, template_folder='templates', static_folder='static')

@account_bp.route('/') 
def account_home():
    return render

@account_bp.route('/products')
def account_product_manager():
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
            return redirect(url_for('account'))
        else:
            product = Products(name=request.form['name'],
                                image=request.form['image'],
                                price=request.form['price'],
                                type=request.form['type']) # type: ignore
            db.session.add(product)
            db.session.commit()
            flash("Product Added Successfully")
            return redirect(url_for('account'))
    return render_template('account.html', products=products, form=form)
