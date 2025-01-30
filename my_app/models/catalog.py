from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from backend.db import db


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String, unique=True, index=True)
    products = relationship('Product', back_populates='category')

    category_id = db.Column(db.Integer, ForeignKey('categories.id', ondelete='CASCADE'))

    @classmethod
    def create(cls, name):
        if not name:
            raise ValueError("Name cannot be empty.")
        existing_category = cls.query.filter_by(name=name).first()
        if existing_category:
            raise ValueError(f"Category with name '{name}' already exists.")
        new_category = cls(name=name)
        db.session.add(new_category)
        db.session.commit()
        return new_category

    @classmethod
    def remove(cls, category_id):
        category = cls.query.get(category_id)
        if category:
            db.session.delete(category)
            db.session.commit()
            return True
        return False


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String, index=True)
    category_id = db.Column(db.Integer, ForeignKey("categories.id"))
    price = db.Column(db.Integer)
    image = db.Column(db.String)
    description = db.Column(db.String(1000), nullable=True)
    category = relationship("Category", back_populates="products")
    cart_items = relationship('CartItem', back_populates='product', lazy=True)

    @classmethod
    def create(cls, name, category_id, price, image, description=None):
        new_product = cls(name=name, category_id=category_id, price=price, image=image,
                          description=description)
        db.session.add(new_product)
        db.session.commit()
        return new_product

    @classmethod
    def remove(cls, product_id):
        product = cls.query.get(product_id)
        if product:
            db.session.delete(product)
            db.session.commit()
            return True
        return False
