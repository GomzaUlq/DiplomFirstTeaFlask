from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from backend.db import db


class Cart(db.Model):
    __tablename__ = 'carts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    products = relationship('CartItem', backref='cart', lazy=True)

    def total_quantity(self):
        return sum(item.quantity for item in self.products)


class CartItem(db.Model):
    __tablename__ = 'cart_items'

    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, ForeignKey('carts.id'), nullable=False)
    product_id = db.Column(db.Integer, ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    product = relationship('Product', backref='cart_items', lazy=True)

    def update_quantity(self, new_quantity):
        if new_quantity > 0:
            self.quantity = new_quantity
        else:
            raise ValueError("Quantity must be greater than zero.")


