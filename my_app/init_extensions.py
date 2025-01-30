from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from backend.db import db
from flask_migrate import Migrate
from models.cart import Cart, CartItem
from models.user import User
from models.catalog import Product, Category
from models.states import State
from routers.user import login_manager

admin = Admin(name='My Admin', template_mode='bootstrap3')
migrate = Migrate()


def init_db(app):
    db.init_app(app)


def init_migrate(app):
    migrate.init_app(app, db)


def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = 'user_bp.show_login'
    login_manager.login_message_category = 'warning'


def init_admin(app):
    admin.init_app(app)
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Product, db.session))
    admin.add_view(ModelView(Category, db.session))
    admin.add_view(ModelView(State, db.session))
