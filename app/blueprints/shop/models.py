from app import db
from datetime import datetime as dt
from flask_login import current_user
from sqlalchemy import and_




class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    products = db.relationship('Item', cascade='all, delete-orphan', backref='category',lazy=True)

    def __repr__(self):
        return f'<Category: {self.id} | {self.name}>'

    def from_dict(self, data):
        for field in ['name']:
            if field in data:
                setattr(self, field, data[field])


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.ForeignKey('item.id'))
    user_id = db.Column(db.ForeignKey('user.id'))


    def from_dict(self, data):
        for field in ['item_id','user_id']:
            if field in data:
                setattr(self, field, data[field])

    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()
    
    def add_item(self, item):
        if current_user.is_anonymous:
            return 0#change this later
        data={
            'item_id': item.id,
            'user_id': current_user.id
        }
        self.from_dict(data)
        self.save()

    def remove_item(item_id):
        if current_user.is_anonymous:
            return 0#change this later
        Cart.query.filter(and_(Cart.user_id==current_user.id,Cart.item_id==item_id)).first().remove()
    

    def __repr__(self):
        return f'<Cart: {self.id} | {self.user_id}...>'

class Item(db.Model):
    def make_tax(context):
        return round(context.get_current_parameters()['price']*.07,2)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.Text)
    price= db.Column(db.Float)
    img = db.Column(db.String)
    category_id = db.Column(db.ForeignKey('category.id'))
    tax=db.Column(db.Float,default=make_tax, onupdate=make_tax)
    created_on = db.Column(db.DateTime, index=True, default=dt.utcnow)
    
    def __repr__(self):
        return f'<Item: {self.id} | {self.name}...>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.id==other.id:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.name, self.id))
                   
    def save(self):
        db.session.add(self)
        db.session.commit()

    def remove(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, data):
        for field in ['name', 'description', 'price', 'img', 'category_id']:
            if field in data:
                setattr(self, field, data[field])
    
    def add_to_cart(self):
        cart=Cart()
        cart.add_item(self)
        
    
    def to_dict(self):
        data = {
            id: self.id,
            name: self.name,
            description: self.description,
            price: self.price,
            img: self.img,
            category_id: self.category_id,
            tax: self.tax,
            created_on: self.created_on
        }
        return data