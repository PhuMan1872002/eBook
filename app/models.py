import enum
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean, Enum, DateTime, Text
from datetime import datetime

db = SQLAlchemy()


class RoleEnum(enum.Enum):
    USER = 1
    ADMIN = 2
    EMPLOYEE = 3


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True)
    date_created = Column(DateTime, default=datetime.now())


class User(BaseModel, UserMixin):
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    avatar = Column(Text, default=None)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER)

    def __str__(self):
        return self.username


class Category(BaseModel):
    name = Column(String(50), nullable=True)
    books = relationship('Book', backref='category', lazy=True)

    def __str__(self):
        return self.name


book_tag = db.Table('book_tag',
                    Column('book_id', ForeignKey('book.id'), nullable=False, primary_key=True),
                    Column('tag_id', ForeignKey('tag.id'), nullable=False, primary_key=True))


class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return f"#{self.name}"


class Book(BaseModel):
    title = Column(String(80), unique=True)
    price = Column(Float, default=0.00)
    image = Column(Text, default="https://placehold.co/200x200")
    description = Column(Text)
    category_id = Column(Integer, ForeignKey(Category.id))
    tags = relationship('Tag', secondary='book_tag', backref='books', lazy=True)

    def __str__(self):
        return self.title