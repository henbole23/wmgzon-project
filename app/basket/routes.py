from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from app.forms import CheckoutForm

from app.models import OrderItems, Orders, Products
from app.extensions import db

basket_bp = Blueprint('basket', __name__, template_folder='templates')


@basket_bp.route('/')
def view_basket():
    basket_data = session.get('basket', [])
    print(basket_data)
    basket_ids = [id['product_id'] for id in basket_data if 'product_id' in id]
    product_data = db.session.query(Products).filter(
        Products.product_id.in_(basket_ids)).all()

    data = zip(product_data, basket_data)
    print(data)
    return render_template('basket.html', data=data, data_check=basket_data, total_price=totalPriceCalc(basket_data, product_data))


@basket_bp.route('/add_to_basket', methods=['POST', 'GET'])
def add_to_basket():
    product_id = request.form['product_id']
    quantity = int(request.form['quantity'])
    format = request.form['options']
    item = {'product_id': product_id, 'quantity': quantity, 'format': format}
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

    return redirect(url_for('basket.view_basket'))


@basket_bp.route('/remove_from_basket', methods=['POST'])
def remove_from_basket():
    product_id = request.form['product_id']

    basket = session.get('basket', [])

    basket = [item for item in basket if item.get('product_id') != product_id]
    session['basket'] = basket
    return redirect(url_for('basket.view_basket'))


@basket_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    form = CheckoutForm()

    # if form.validate_on_submit():
    if request.method == 'POST':
        basket_data = session.get('basket', [])
        order = Orders(fk_user_id=current_user.user_id)
        db.session.add(order)
        db.session.commit()

        for data in basket_data:
            product = db.session.query(Products).filter(
                Products.product_id == data['product_id']).first()
            print(product)
            product.stock -= data['quantity']
            db.session.add(product)
            db.session.commit()
            order_items = OrderItems(
                quantity=data['quantity'], format=data['format'], fk_order_id=order.order_id, fk_product_id=data['product_id'])
            db.session.add(order_items)

        db.session.commit()
        del session['basket']
        flash(f"Order {order.order_id} Submitted Successfully", 'success')
        return redirect(url_for('home.home'))

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
