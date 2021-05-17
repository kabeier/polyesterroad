from .import bp as shop
from flask import render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.blueprints.shop.models import Item, Category, Cart
from sqlalchemy import and_
import stripe
import os

@shop.route('/', methods=['GET'])
@shop.route('/index', methods=['GET'])
def index():
    if current_user.is_anonymous:
        return redirect(url_for('authentication.login'))
    items=Item.query.all()
    cats=Category.query.all()
    return(render_template('shop/index.html',items=items,cats=cats))

@shop.route('/cat', methods=['GET'])
def cat():
    cat=request.args.get('cat',type=int)
    items=Item.query.filter_by(category_id=cat)
    cats=Category.query.all()
    return(render_template('shop/cat.html',items=items,cats=cats))

@shop.route('/add_to_cart', methods=['GET'])
def add_to_cart():
    item_id=request.args.get('id',type=int)
    item=Item.query.filter_by(id=item_id).first()
    item.add_to_cart()
    flash(f'You added {item.name} to your cart','success')
    return redirect(request.referrer)

@shop.route('/mycart',methods=['GET'])
def mycart():
    return(render_template('shop/mycart.html',key=os.environ.get('STRIPE_PUBLISHABLE_KEY')))


@shop.route('/remove_item',methods=['GET','POST'])
def remove_item():
    item_id=request.args.get('id',type=int)
    Cart.remove_item(item_id)
    item=Item.query.filter_by(id=item_id).first()
    flash(f'You removed {item.name} from your cart', 'danger')

    return redirect(request.referrer)

@shop.route('/one_item', methods=['GET'])
def one_item():
    item_id=request.args.get('item_id',type=int)
    items=Item.query.filter_by(id=item_id)
    return(render_template('shop/cat.html',items=items))

@shop.route('/checkout', methods=['POST'])
def checkout():

    amount = int(current_user.cart_total_taxed()*100)

    customer = stripe.Customer.create(
        email=current_user.email,
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Black Market Charge'
    )
    current_user.empty_cart()

    return render_template('shop/checkout.html', amount=amount)
