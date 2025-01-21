import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///./shop.db')
    SECRET_KEY = os.environ.get("SECRET_KEY", "148u1hufw9h2r")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

