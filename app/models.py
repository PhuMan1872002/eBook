from app import db
from sqlalchemy import Column, String, Integer, Boolean

class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), unique=True)
    active = Column(Boolean, default=True)
    