from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from app.forms import CheckoutForm

from app.models import OrderItems, Orders, Products
from app.extensions import db

# Initialisation of basket blueprint
basket_bp = Blueprint('basket', __name__, template_folder='templates')


# Route for basket page

@basket_bp.route('/')
def view_basket():
    """Function which reads the session data and populates the basket page with basket data"""

    # Gets basket data from session
    basket_data = session.get('basket', [])
    # Creates an array of product ids that are in the basket
    basket_ids = [id['product_id'] for id in basket_data if 'product_id' in id]
    # Queries database for the data of products in the basket
    product_data = db.session.query(Products).filter(
        Products.product_id.in_(basket_ids)).all()
    # Connects the product data to the products in basket
    data = zip(product_data, basket_data)

    return render_template('basket.html', data=data, data_check=basket_data, total_price=totalPriceCalc(basket_data, product_data))


# Route for adding items to basket

@basket_bp.route('/add_to_basket', methods=['POST', 'GET'])
def add_to_basket():
    """Function which adds items to the basket session"""

    # Retrieves the product id from the form
    product_id = request.form['product_id']
    # Retrieves the quantity of the product from the form
    quantity = int(request.form['quantity'])
    # Retrieves the the format of the chosen item
    format = request.form['options']
    # Collates the form data in a dictionary
    item = {'product_id': product_id, 'quantity': quantity, 'format': format}

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


# Route for removing items from basket

@basket_bp.route('/remove_from_basket', methods=['POST'])
def remove_from_basket():
    """Function for removing items from basket"""

    # Retrieves the product id from the form
    product_id = request.form['product_id']

    # Retrieves the basket data from session
    basket = session.get('basket', [])
    # Removes the item from the basket based on product id
    basket = [item for item in basket if item.get('product_id') != product_id]
    # Sets the basket again without the removed item
    session['basket'] = basket
    return redirect(url_for('basket.view_basket'))


# Route for checking out basket

@basket_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Function for handling and submitting checkout"""
    # Initialises the CheckoutForm class
    form = CheckoutForm()

    # Uses request.method over validate_on_submit since form currently isn't active
    if request.method == 'POST':
        # Retrieves basket data
        basket_data = session.get('basket', [])
        # Creates an Order object and assigns it to the current user
        order = Orders(fk_user_id=current_user.user_id)
        db.session.add(order)
        db.session.commit()

        # Loops through the products in the basket
        for data in basket_data:
            # Queries the database for the current product in the basket loop
            product = db.session.query(Products).filter(
                Products.product_id == data['product_id']).first()

            # Decreases the stock of the current product in the basket loop
            product.stock -= data['quantity']
            # Adds the product to the database with less stock
            db.session.add(product)
            db.session.commit()
            # Creates an OrderItem object for the curren product in the basket loop
            order_items = OrderItems(quantity=data['quantity'], format=data['format'],
                                     fk_order_id=order.order_id, fk_product_id=data['product_id'])
            db.session.add(order_items)

        db.session.commit()
        # Deletes the data in the basket session
        del session['basket']
        flash(f"Order {order.order_id} Submitted Successfully", 'success')
        return redirect(url_for('home.home'))

    else:
        print(form.errors)

    return render_template('checkout.html', form=form)


def totalPriceCalc(basket_data, product_data):
    """Function for calculating the total price of items"""

    total = 0

    # Loops through the products in basket
    for product in basket_data:
        id = int(product['product_id'])
        quantity = product['quantity']

        # Loops through all the products that could be in the basket
        for product_item in product_data:
            # If the product id is the same as the id for the product in basket
            if product_item.product_id == id:
                total += product_item.price * quantity

    # Returns the total to 2 decimal places
    return round(total, 2)
