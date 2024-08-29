from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from app import config
from .admin import admin_manager
from .models import db

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)

db.init_app(app=app)
login_manager = LoginManager(app=app)
migrate = Migrate(db=db, app=app, render_as_batch=True)
admin_manager.init_app(app=app)