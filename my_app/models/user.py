from werkzeug.security import generate_password_hash, check_password_hash
from backend.db import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    first_name = db.Column(db.String(30))
    email = db.Column(db.String(120))
    password_hash = db.Column(db.String(128))
    slug = db.Column(db.String, unique=True, index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)
