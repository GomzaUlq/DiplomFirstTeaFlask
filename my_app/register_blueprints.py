from routers.user import user_bp
from routers.catalog import category_bp, product_bp, main_bp, about_bp
from routers.cart import cart_bp
from routers.states import states_bp


def register_blueprints(app):
    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(states_bp)
