from flask import Blueprint, jsonify, request, render_template
from backend.db import db
from models import Cart, CartItem

cart_bp = Blueprint('cart', __name__, template_folder='templates')


# Создание новой корзины
@cart_bp.route('/cart', methods=['POST'])
def create_cart():
    data = request.get_json()
    new_cart = Cart(user_id=data['user_id'])
    db.session.add(new_cart)
    db.session.commit()
    return jsonify({"message": "Корзина успешно создана!", "cart_id": new_cart.id}), 201


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


@cart_bp.route('/cart/<int:cart_id>/items', methods=['POST'])
def add_item_to_cart(cart_id):
    data = request.get_json()  # Получаем данные из JSON
    product_id = data.get('product_id')  # Извлекаем product_id из данных
    new_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=1)  # Устанавливаем количество по умолчанию
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"message": "Товар успешно добавлен в корзину!"}), 201


# Обновление количества товара в корзине
@cart_bp.route('/cart/<int:cart_id>/items/<int:item_id>', methods=['PUT'])
def update_cart_item(cart_id, item_id):
    data = request.get_json()
    item = CartItem.query.get(item_id)
    if item and item.cart_id == cart_id:
        item.update_quantity(data['quantity'])
        db.session.commit()
        return jsonify({"message": "Количество товара обновлено!"}), 200
    return jsonify({"message": "Товар не найден в корзине"}), 404


# Удаление товара из корзины
@cart_bp.route('/cart/<int:cart_id>/items/<int:item_id>', methods=['DELETE'])
def remove_cart_item(cart_id, item_id):
    item = CartItem.query.get(item_id)
    if item and item.cart_id == cart_id:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Товар успешно удален из корзины!"}), 200
    return jsonify({"message": "Товар не найден в корзине"}), 404


# Отображение корзины
@cart_bp.route('/cart_view', methods=['GET'])
def cart_view():
    return render_template('cart/cart_view.html')
