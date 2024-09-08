import os, os.path as op, secrets, cloudinary
from dotenv import load_dotenv

load_dotenv()

base_dir = op.abspath(op.dirname(__file__))

class Config(object):
    SECRET_KEY = secrets.token_hex(32)
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'database', 'ebook.db')
    PAGE_SIZE = 1
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME  = '2151010220man@ou.edu.vn'
    MAIL_PASSWORD  = 'mottambayhailehai1872002'
    FLASK_ADMIN_SWATCH = 'lux'
    
    cloudinary.config(
        cloud_name = "dnmsyzmjf",
        api_key = "769711456479333",
        api_secret = "4wV-HXrE341NRq1Q7D27G74wcI8"
    )


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@localhost/ebookdb?charset=utf8mb4"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True