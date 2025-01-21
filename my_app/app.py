from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from backend.db import db
from flask import Flask
from backend.config import Config
from flask_migrate import Migrate
from models.cart import Cart, CartItem
from models.user import User
from models.catalog import Product, Category
from models.states import State
from routers.user import user_bp, login_manager
from routers.catalog import category_bp, product_bp, main_bp, about_bp
from routers.cart import cart_bp
from routers.states import states_bp

migrate = Migrate()


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)
    admin = Admin(app, name='My Admin', template_mode='bootstrap3')

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(State, db.session))
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = '/'

    with app.app_context():
        app.register_blueprint(user_bp)
        app.register_blueprint(category_bp)
        app.register_blueprint(product_bp)
        app.register_blueprint(cart_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(about_bp)
        app.register_blueprint(states_bp)

        db.create_all()

    return app


my_app = create_app()

if __name__ == "__main__":
    my_app.run(debug=True)
