from flask import Flask
from flask_wtf import CSRFProtect
from backend.config import Config
from backend.db import db
from models.cart import Cart, CartItem
from models.user import User
from models.catalog import Product, Category
from models.states import State
from register_blueprints import register_blueprints
from init_extensions import init_db, init_login_manager, init_admin, init_migrate

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
csrf = CSRFProtect()


def create_app():
    with app.app_context():
        init_db(app)
        init_login_manager(app)
        init_admin(app)
        csrf.init_app(app)
        init_migrate(app)

        register_blueprints(app)

        db.create_all()

    return app


my_app = create_app()

if __name__ == "__main__":
    my_app.run(debug=True)
