from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user

from models import Product, Category
from backend.db import db

product_bp = Blueprint('products', __name__, template_folder="templates")
category_bp = Blueprint('categories', __name__, template_folder="templates")
main_bp = Blueprint('main', __name__, template_folder="templates")
about_bp = Blueprint('about', __name__, template_folder="templates")


@category_bp.route('/categories', methods=['POST'])
def create_category():
    data = request.get_json()
    new_category = Category(
        name=data['name']
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Категория успешно создана!"}), 201


@product_bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(
        name=data['name'],
        price=data['price'],
        image=data['image'],
        description=data['description'],
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Продукт успешно создан!"}), 201


@product_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get(category_id)
    if category:
        return jsonify({
            "id": category.id,
            "name": category.name

        }), 200
    return jsonify({"message": "Категория не найдена"}), 404


@category_bp.route('/showcase', methods=['GET'])
def get_products():
    all_products = Product.query.all()
    if current_user.is_authenticated and current_user.carts:
        cart_id = current_user.carts[0].id
    else:
        cart_id = None

    return render_template(
        'catalog/showcase.html',
        products=all_products,
        cart_id=cart_id
    )


@main_bp.route('/', methods=['GET'])
def home():
    return render_template('catalog/home.html')


@about_bp.route("/about")
def about():
    with open('static/about.txt', 'r', encoding='utf-8') as file:
        content = file.read()
        return render_template('catalog/about.html', content=content)
