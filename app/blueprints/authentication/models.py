from app import db
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin
from app.blueprints.shop.models import Cart, Item
from collections import Counter
from sqlalchemy.sql import func
from pprint import pprint


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, index=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    cart = db.relationship('Cart', cascade='all, delete-orphan', backref='user', lazy=True)
    
    c_cart_items=[]

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def hash_password(self, original_password):
        self.password = generate_password_hash(original_password)

    def check_hashed_password(self, original_password):
        return check_password_hash(self.password, original_password)

    def from_dict(self, data):
        for field in ['first_name', 'last_name', 'email']:
            if field in data:
                setattr(self, field, data[field])

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def my_cart(self):
        my_cart = Cart.query.filter_by(user_id=self.id)
        return my_cart

    def my_cart_items(self):
        if len(self.c_cart_items)==Cart.query.filter(Cart.user_id==self.id).count():
            return self.c_cart_items
        my_items=[]
        items=db.session.query(Item.id).join(Cart,Cart.item_id==Item.id).filter(Cart.user_id==self.id).all()
        all_items=Item.query.all()
        for citem in items:
            for item in all_items:
                if citem[0]==item.id:
                    my_items.append(item)
        self.c_cart_items=my_items[:]
        return self.c_cart_items

    def my_cart_items_unique(self):
        items=Item.query.join(Cart,Cart.item_id==Item.id).filter(Cart.user_id==self.id).all()
        return items

    def cart_item_quanties(self):
        cnt=Counter(self.my_cart_items())
        return cnt

    def cart_total_taxed(self):
        total=0.00
        for item in self.my_cart_items():
            total+=item.price+item.tax
        return total

    def cart_total(self):
        total=0.00
        for item in self.my_cart_items():
            total+=item.price
        return total

    def cart_total_tax(self):
        total=0.00
        for item in self.my_cart_items():
            total+=item.tax
        return total

    
    def cart_item_count(self):
        return(len(self.my_cart_items()))

    def empty_cart(self):
        ct=Cart.query.filter_by(user_id=self.id).all()
        for item in ct:
            item.remove()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))