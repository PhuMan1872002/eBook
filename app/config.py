import os, os.path as op, secrets
from dotenv import load_dotenv

load_dotenv()

base_dir = op.abspath(op.dirname(__file__))

class Config(object):
    SECRET_KEY = secrets.token_hex(32)
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'database', 'ebook.db')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost/ebookdb?charset=utf8mb4"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True