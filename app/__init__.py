from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = '3487ywheenujbhreriu4ui$$&()&^^^9erjrtunbr'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/ebookdb?charset=utf8mb4" % quote(
    "123456")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 2
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True
app.config['MAIL_USERNAME'] = '2151010220man@ou.edu.vn'
app.config['MAIL_PASSWORD'] = 'mottambayhailehai1872002'

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

mail = Mail(app)
login = LoginManager(app=app)
import cloudinary

cloudinary.config(
  cloud_name = "dnmsyzmjf",
  api_key = "769711456479333",
  api_secret = "4wV-HXrE341NRq1Q7D27G74wcI8"
)