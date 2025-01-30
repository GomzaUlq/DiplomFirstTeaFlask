import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///shop.db')
    SECRET_KEY = os.environ.get("SECRET_KEY", "589c25264247e0bc896e41f1dbf590d3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

