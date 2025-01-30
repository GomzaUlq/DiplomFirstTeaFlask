from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_login import current_user

from backend.db import db
from models import Cart, CartItem, Product
from routers.forms import CheckoutForm

cart_bp = Blueprint('cart', __name__, template_folder='templates')


@cart_bp.before_request
def ensure_cart_exists():
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            new_cart = Cart(user_id=current_user.id)
            db.session.add(new_cart)
            db.session.commit()


@cart_bp.route('/cart', methods=['GET'])
def get_current_cart():
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first_or_404()
        return jsonify({
            "id": cart.id,
            "user_id": cart.user_id,
            "total_quantity": cart.total_quantity(),
            "products": [{"product_id": item.product_id, "quantity": item.quantity} for item in cart.items]
        }), 200
    return jsonify({"message": "Неавторизованный доступ"}), 401


# Получение информации о корзине
@cart_bp.route('/cart/<int:cart_id>', methods=['GET'])
def get_cart(cart_id):
    cart = Cart.query.get(cart_id)
    if cart:
        return jsonify({
            "id": cart.id,
            "user_id": cart.user_id,
            "total_quantity": cart.total_quantity(),
            "products": [{"product_id": item.product_id, "quantity": item.quantity} for item in cart.products]
        }), 200
    return jsonify({"message": "Корзина не найдена"}), 404


@cart_bp.route('/test', methods=['POST'])
def test_route():
    data = request.get_json()  # Извлекаем JSON-данные
    if not data:
        return jsonify(message="No data provided"), 400
    return jsonify(message="Test successful"), 200


@cart_bp.route('/cart/<int:cart_id>/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(cart_id, product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": f"Product with ID {product_id} does not exist."}), 404
    cart = Cart.query.get(cart_id)
    if not cart:
        return jsonify({"error": f"Cart with ID {cart_id} does not exist."}), 404
    existing_item = CartItem.query.filter_by(cart_id=cart_id, product_id=product_id).first()
    if existing_item:
        # Обновляем количество товара в корзине
        existing_item.quantity += 1
        db.session.commit()
        return jsonify({"message": f"{product.name} updated in the cart.", "quantity": existing_item.quantity}), 200
    else:
        new_item = CartItem(
            cart_id=cart_id,
            product_id=product_id,
            quantity=1
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({"message": f"{product.name} added to the cart.", "quantity": 1}), 201


@cart_bp.route('/cart/update_cart_item/<int:item_id>', methods=['POST'])
def update_cart_item(item_id):
    if current_user.is_authenticated:
        data = request.get_json()
        item = CartItem.query.get(item_id)
        if item and item.cart.user_id == current_user.id:
            quantity = int(data['quantity'])  # Получаем количество из формы
            item.update_quantity(quantity)
            db.session.commit()
            return jsonify({"message": "Количество товара обновлено!"}), 200
        return jsonify({"message": "Товар не найден в корзине"}), 404
    return jsonify({"message": "Неавторизованный доступ"}), 401


@cart_bp.route('/cart/remove_cart_item/<int:item_id>', methods=['POST'])
def remove_cart_item(item_id):
    if current_user.is_authenticated:
        item = CartItem.query.get(item_id)
        if item and item.cart.user_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
            return jsonify({"message": "Товар успешно удален из корзины!"}), 200
        return jsonify({"message": "Товар не найден в корзине"}), 404
    return jsonify({"message": "Неавторизованный доступ"}), 401


@cart_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    form = CheckoutForm()

    if form.validate_on_submit():  # Проверка CSRF включена автоматически
        address = form.address.data
        phone = form.phone.data

        if current_user.is_authenticated:
            CartItem.query.filter_by(cart_id=current_user.carts[0].id).delete()
            db.session.commit()

        flash('Заказ создан успешно!', 'success')
        return redirect(url_for('main.home'))

    # Получаем товары из корзины для отображения на странице оформления заказа
    items = CartItem.query.filter_by(cart_id=current_user.carts[0].id).all() if current_user.is_authenticated else []

    return render_template('cart/checkout.html', items=items, form=form)


@cart_bp.route('/cart_view', methods=['GET'])
def cart_view():
    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first_or_404()
        items = cart.items
        return render_template('cart/cart_view.html', cart=cart, items=items)
    return redirect(url_for('auth.login'))
